from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.parsing.propositional_parser import parse_string
from src.core.proof import Proof, Sequent, InferenceRule
from src.core.sentence import Gamma
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-proof', methods=['POST'])
def check_proof():
    try:
        data = request.json
        proof_lines = data.get('proof', '').strip().split('\n')

        if not proof_lines or proof_lines == ['']:
            return jsonify({
                'valid': False,
                'error': 'Empty proof provided',
                'line': 0
            })

        proof = Proof()
        results = []

        for i, line in enumerate(proof_lines):
            line = line.strip()
            if not line:
                continue

            try:
                # Parse the line format: "assumptions |- conclusion :rule"
                if '|-' not in line:
                    results.append({
                        'line': i + 1,
                        'valid': False,
                        'error': 'Invalid format. Expected: assumptions |- conclusion :rule'
                    })
                    continue

                parts = line.split('|-')
                if len(parts) != 2:
                    results.append({
                        'line': i + 1,
                        'valid': False,
                        'error': 'Invalid format. Expected single |- separator'
                    })
                    continue

                assumptions_str = parts[0].strip()
                conclusion_rule = parts[1].strip()

                if ':' not in conclusion_rule:
                    results.append({
                        'line': i + 1,
                        'valid': False,
                        'error': 'Missing inference rule. Expected :RULE at end'
                    })
                    continue

                conclusion_str, rule_str = conclusion_rule.rsplit(':', 1)
                conclusion_str = conclusion_str.strip()
                rule_str = rule_str.strip()

                assumptions_str = assumptions_str.strip('[]')
                assumptions_str = assumptions_str.strip()

                # Parse assumptions
                if assumptions_str == '':
                    gamma = Gamma()
                else:
                    # Split by comma
                    assumption_strs = [s.strip() for s in assumptions_str.split(',') if s.strip()]
                    assumptions = [parse_string(s) for s in assumption_strs]
                    gamma = Gamma(assumptions)

                # Parse conclusion
                conclusion = parse_string(conclusion_str)

                # Parse rule
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
                    results.append({
                        'line': i + 1,
                        'valid': False,
                        'error': f'Unknown inference rule: {rule_str}'
                    })
                    continue

                rule = rule_map[rule_str]
                sequent = Sequent(gamma, conclusion, rule)

                # Check if sequent is valid
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
                        'error': f'Invalid inference for rule {rule_str}'
                    })

            except Exception as e:
                results.append({
                    'line': i + 1,
                    'valid': False,
                    'error': f'Parse error: {str(e)}'
                })

        # Check if all lines are valid
        all_valid = all(result['valid'] for result in results)

        return jsonify({
            'valid': all_valid,
            'results': results,
            'total_lines': len(results)
        })

    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)