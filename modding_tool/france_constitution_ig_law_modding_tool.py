laws = ["law_executive","law_parliamentary","law_council_elective","law_representative_democracy", "law_consensus_democracy", "law_direct_democracy", "law_unitary", "law_devolved", "law_federalized", "law_free_market", "law_interventionism", "law_socialization"]


for law in laws :
    print("france_constitution_ig_stance_value_{law}_value = {{\n    value = 1\n    if = {{ limit = {{ law_stance = {{law = law_type:{law} value = strongly_approve}}}}\n        add = 5\n    }}\n    else_if = {{ limit = {{ law_stance = {{law = law_type:{law}  value = approve}}}}\n        add = 3\n    }}\n    else_if = {{ limit = {{ law_stance = {{law = law_type:{law}  value = disapprove}}}}\n        subtract = 1\n    }}\n    else_if = {{ limit = {{ law_stance = {{law = law_type:{law}  value = strongly_disapprove}}}}\n        subtract = 3\n    }}\n}}".format(law = law))
    print("france_constitution_gaullist_stance_on_{law}_value = {{ \n       value = 0\n       add = ig:ig_patriots.france_constitution_ig_stance_{law}_value_weighted\n       add = ig:ig_capitalists.france_constitution_ig_stance_{law}_value_weighted\n       add = ig:ig_entrepreneurs.france_constitution_ig_stance_{law}_value_weighted\n       add = ig:ig_securocrats.france_constitution_ig_stance_{law}_value_weighted\n       divide = france_constitution_gaullist_clout\n}}".format(law = law))
    print("france_constitution_moralist_stance_on_{law}_value = {{\n    value = 0\n    add = ig:ig_moralists.france_constitution_ig_stance_{law}_value_weighted\n    add = ig:ig_elites.france_constitution_ig_stance_{law}_value_weighted\n    add = ig:ig_ruralists.france_constitution_ig_stance_{law}_value_weighted\n    divide = france_constitution_moralist_clout\n}}".format(law = law))
    print("france_constitution_socialist_stance_on_{law}_value = {{\n    value = 0\n    add = ig:ig_urbanists.france_constitution_ig_stance_{law}_value_weighted\n    add = ig:ig_intelligentsia.france_constitution_ig_stance_{law}_value_weighted\n    divide = france_constitution_socialist_clout\n}}".format(law = law))


"""
france_constitution_communist_stance_on_{law}_value = {{\n    value = 0\n    add = ig:ig_bureaucrats.france_constitution_ig_stance_{law}_value_weighted\n    add = ig:ig_laborists.france_constitution_ig_stance_{law}_value_weighted\n    divide = france_constitution_communist_clout\n}}
"""