#!/usr/bin/env python3
"""
Helper script to add medium and hard difficulties to all parameterized skills.
Appends the new specs before the registry section.
"""

# Define the specs to add (skill_name, base_params, medium_params, hard_params)
specs_to_add = [
    # Roots-based skills (r1, r2)
    ("ROOTS_FACTORED", "roots_factored", [-15, 15], [-30, 30], [-45, 45],
     "Find the roots of y = (x {sign_r1}{r1})(x {sign_r2}{r2})."),

    ("SOLVE_BY_FORMULA", "solve_by_formula", [-15, 15], [-30, 30], [-45, 45],
     "Solve using the quadratic formula: x^2 {sign_b}{b}x {sign_c}{c} = 0."),

    ("INTERCEPTS", "intercepts", [-15, 15], [-30, 30], [-45, 45],
     "Find the x-intercepts of y = (x {sign_r1}{r1})(x {sign_r2}{r2})."),

    # Vertex-based skills (h, k)
    ("GRAPH_VERTEX", "graph_vertex", [-10, 10], [-20, 20], [-30, 30],
     "What is the vertex of y = (x {sign_h}{h})^2 {sign_k}{k}?"),

    ("AXIS_SYMMETRY", "axis_symmetry", [-10, 10], [-20, 20], [-30, 30],
     "Find the axis of symmetry for y = (x {sign_h}{h})^2 {sign_k}{k}."),

    # Standard form skills (a, b, c)
    ("STANDARD_VERTEX", "standard_vertex", None, None, None,
     "Find the vertex of y = {a}x^2 {sign_b}{b}x {sign_c}{c}."),

    ("DISCRIMINANT", "discriminant", None, None, None,
     "For {a_fmt}x^2 {sign_b}{b}x {sign_c}{c} = 0, what is the discriminant?"),

    # Complete square (b only)
    ("COMPLETE_SQUARE", "complete_square", None, None, None,
     "Complete the square for x^2 {sign_b}{b}x."),
]

print("# Medium and Hard difficulty specs")
print()

# Generate medium/hard for each skill
for spec_name, skill_base, easy_range, med_range, hard_range, template in specs_to_add:
    skill_name_parts = skill_base.split('_')
    skill_id = f"quad.{'.'.join(skill_name_parts)}"

    # Medium
    print(f"{spec_name}_MEDIUM = ParameterSpec(")
    print(f'    template_id="{skill_id}",')
    print(f'    difficulty="medium",')
    print(f'    stem_template="{template}",')
    print(f"    constraints=[")

    if easy_range:  # Root-based or vertex-based
        if 'r1' in template:  # Root-based
            print(f"        ParameterConstraint(param_name='r1', param_type='int', min_value={med_range[0]}, max_value={med_range[1]}, exclude={{0}}),")
            print(f"        ParameterConstraint(param_name='r2', param_type='int', min_value={med_range[0]}, max_value={med_range[1]}, exclude={{0}}),")
        else:  # Vertex-based (h, k)
            print(f"        ParameterConstraint(param_name='h', param_type='int', min_value={med_range[0]}, max_value={med_range[1]}, exclude={{0}}),")
            print(f"        ParameterConstraint(param_name='k', param_type='int', min_value={med_range[0]}, max_value={med_range[1]}, exclude={{0}}),")
    elif 'standard_vertex' in skill_base or 'discriminant' in skill_base:  # Standard form
        print(f"        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1, 2, -2]),")
        print(f"        ParameterConstraint(param_name='b', param_type='int', min_value=-20, max_value=20, exclude={{0}}),")
        print(f"        ParameterConstraint(param_name='c', param_type='int', min_value=-20, max_value=20" + (", exclude={0}" if 'discriminant' in skill_base else "") + "),")
    else:  # Complete square
        print(f"        ParameterConstraint(param_name='b', param_type='choice', choices=list(range(-20, 22, 2))),")

    print(f"    ],")
    print(f"    solver={skill_base}_easy_solver,")
    print(f"    distractor_generator={skill_base}_easy_distractors")
    print(f")")
    print()

    # Hard
    print(f"{spec_name}_HARD = ParameterSpec(")
    print(f'    template_id="{skill_id}",')
    print(f'    difficulty="hard",')
    print(f'    stem_template="{template}",')
    print(f"    constraints=[")

    if hard_range:  # Root-based or vertex-based
        if 'r1' in template:  # Root-based
            print(f"        ParameterConstraint(param_name='r1', param_type='int', min_value={hard_range[0]}, max_value={hard_range[1]}, exclude={{0}}),")
            print(f"        ParameterConstraint(param_name='r2', param_type='int', min_value={hard_range[0]}, max_value={hard_range[1]}, exclude={{0}}),")
        else:  # Vertex-based (h, k)
            print(f"        ParameterConstraint(param_name='h', param_type='int', min_value={hard_range[0]}, max_value={hard_range[1]}, exclude={{0}}),")
            print(f"        ParameterConstraint(param_name='k', param_type='int', min_value={hard_range[0]}, max_value={hard_range[1]}, exclude={{0}}),")
    elif 'standard_vertex' in skill_base or 'discriminant' in skill_base:  # Standard form
        print(f"        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1, 2, -2, 3, -3]),")
        print(f"        ParameterConstraint(param_name='b', param_type='int', min_value=-30, max_value=30, exclude={{0}}),")
        print(f"        ParameterConstraint(param_name='c', param_type='int', min_value=-30, max_value=30" + (", exclude={0}" if 'discriminant' in skill_base else "") + "),")
    else:  # Complete square
        print(f"        ParameterConstraint(param_name='b', param_type='choice', choices=list(range(-30, 32, 2))),")

    print(f"    ],")
    print(f"    solver={skill_base}_easy_solver,")
    print(f"    distractor_generator={skill_base}_easy_distractors")
    print(f")")
    print()
