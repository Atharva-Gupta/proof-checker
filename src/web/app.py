from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS
from src.parsing.propositional_parser import parse_string
from src.core.proof import Proof, Sequent, InferenceRule
from src.core.fitch_style import FitchSubProof
from src.core.sentence import Gamma
from src.core.errors import ParseError
import traceback
import sys

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def line2conclusion(line):
    """
    Parse the following format: "conclusion :RULE". This will appear in both sequent-style and
    fitch-style proofs.
    """
    if ':' not in line:
        raise ParseError('Invalid format. Missing inference rule.' \
                         'Expected format: [assumption_1, assumption_2, ...] |- conclusion :RULE')

    conclusion_str, rule_str = line.rsplit(':', 1)
    conclusion_str = conclusion_str.strip()
    rule_str = rule_str.strip()

    conclusion = parse_string(conclusion_str)

    rule_map = {
        'AX': InferenceRule.axiom,
        'AI': InferenceRule.and_intro,
        'AE': InferenceRule.and_elim,
        'OI': InferenceRule.or_intro,
        'OE': InferenceRule.or_elim,
        'II': InferenceRule.implies_intro,
        'IE': InferenceRule.implies_elim,
        'NI': InferenceRule.not_intro,
        'NE': InferenceRule.not_elim,
        'TI': InferenceRule.true_intro,
        'FE': InferenceRule.false_elim,
        'EX': InferenceRule.expand,
        'IP': InferenceRule.contra
    }

    if rule_str not in rule_map:
        raise ParseError(f'{rule_str} is not one of the valid rules of inference!')

    return conclusion, rule_map[rule_str]

def line2sequent(line):
    """
    Parse the line format: "[assumption_1, assumption_2, ...] |- conclusion :RULE"
    """
    if '|-' not in line:
        raise ParseError('Invalid format. Missing a turnstile |- separator.' \
                         'Expected format: [assumption_1, assumption_2, ...] |- conclusion :RULE')

    parts = line.split('|-')
    if len(parts) != 2:
        raise ParseError('Invalid format. Expected single turnstile |- separator.' \
                         'Expected format: [assumption_1, assumption_2, ...] |- conclusion :RULE')

    assumptions_str = parts[0].strip()
    conclusion_rule = parts[1].strip()

    assumptions_str = assumptions_str.strip('[]')
    assumptions_str = assumptions_str.strip()

    if assumptions_str == '':
        gamma = Gamma()
    else:
        assumption_strs = [s.strip() for s in assumptions_str.split(',') if s.strip()]
        assumptions = [parse_string(s) for s in assumption_strs]
        gamma = Gamma(assumptions)

    conclusion, rule = line2conclusion(conclusion_rule)

    return Sequent(gamma, conclusion, rule)

@app.route('/check-sequent-proof', methods=['POST'])
def check_sequent_proof():
    try:
        data = request.json
        proof_lines = data.get('proof', '').strip().split('\n')
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

    proof = Proof()
    results = []

    for i, line in enumerate(proof_lines):
        line = line.strip()
        if not line:
            continue

        try:
            sequent = line2sequent(line)
        except ParseError as e:
            results.append({
                'line': i + 1,
                'valid': False,
                'error': e.args[0]
            })
            continue

        if proof.add_sequent(sequent):
            results.append({
                'line': i + 1,
                'valid': True,
                'sequent': str(sequent)
            })
        else:
            results.append({
                'line': i + 1,
                'valid': False,
                'error': f'Invalid inference for rule {sequent.rule}'
            })

    all_valid = all(result['valid'] for result in results)

    return jsonify({
        'valid': all_valid,
        'results': results,
        'total_lines': len(results)
    })

@app.route('/check-fitch-proof', methods=['POST'])
def check_fitch_proof():
    try:
        data = request.json
        proof_lines = data.get('proof', '').strip().split('\n')
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

    fs = FitchSubProof()
    results = []
    space_count = 0

    for i, line in enumerate(proof_lines):
        if line == "--":
            fs = fs.outer_proof
            space_count -= 1
            continue

        line = line.rstrip()
        if not line:
            continue

        ind = 0
        while line[ind] == " ":
            ind += 1

        if ind < space_count:
            fs = fs.outer_proof
        elif ind > space_count:
            fs = fs.add_subproof()

        space_count = ind

        try:
            conclusion, rule = line2conclusion(line[ind:])
        except ParseError as e:
            results.append({
                'line': i + 1,
                'valid': False,
                'error': e.args[0]
            })
            continue

        if rule == InferenceRule.axiom:
            val = fs.add_assumption(conclusion)
        else:
            val = fs.add_conclusion(conclusion, rule)

        if val:
            results.append({
                'line': i + 1,
                'valid': True,
                'sequent': "hi"
            })
        else:
            results.append({
                'line': i + 1,
                'valid': False,
                'error': f'Invalid inference for rule {rule}'
            })

    all_valid = all(result['valid'] for result in results)

    return jsonify({
        'valid': all_valid,
        'results': results,
        'total_lines': len(results)
    })

if __name__ == '__main__':
    app.run(debug=True)