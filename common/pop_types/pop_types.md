    example = {														# profession name
        texture = "gfx/interface/icons/pops_icons/example.dds"			# profession icon
        color = { 12 251 123 }											# profession color
		working_adult_ratio = 0.25										# the proportion of this profession that tends to be part of the Workforce
        start_quality_of_life = 10										# basic quality of life
        wage_weight = 3													# importance of the pop's wage
        paid_private_wage = yes/no										# whether this pop type receives wages in a non government funded building (default no)
        literacy_target = 0.80											# wage for dependents
        consumption_mult = 1											# goods consumption multiplier (default = 1)
        dependent_wage = 0.5											# per year
        unemployment = yes												# can pop be unemployed
        unemployment_wealth = 5											# unemployed pops whose wealth drops to or below this level switches to this profession
        
        # 50% - 100% politically engaged
        political_engagement_base = 0.5									# basic political engagement
        political_engagement_literacy_factor = 1.0						# literacy to political engagement 
        
        political_engagement_mult = { value = 1	}						# scripted value to escalate dynamic terrain value
        
        qualifications = {}												# Qualifications scripted values list
    
        portrait_age = { value = 30 }									# Age for portrait
        portrait_pose = { value = 0 }									# Pose for portrait
        portrait_is_female = { always = yes }							# Is portrait female or male
    }

 Notes:
 - Localization expects there to be a <POP_TYPE>_QUALIFICATIONS_DESC loc key defined. For example "ENGINEERS_QUALIFICATIONS_DESC"
