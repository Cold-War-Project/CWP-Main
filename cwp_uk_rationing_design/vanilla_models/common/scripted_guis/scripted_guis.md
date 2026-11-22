# Structure
	scripted_gui_key = {
		scope = < string >			# What scope type this SGUI is available to
		is_shown = { trigger }		# Determines whether the SGUI is shown / available to a player
		is_valid = { trigger }		# Determines whether the SGUI can be used by a player
		effect = { effect }			# Determines what will happen when the SGUI element is activated
		saved_scopes = { scopes }	# List of strings corresponding to scopes you want event targets for in triggers / effects
		notification_key = < key >	# Notification key when this SGUI is activated (default jomini_scripted_gui_confirm)
		confirm_title = {}			# Confirmation window title for this SGUI
		confirm_text = {}			# Confirmation window text for this SGUI
		ai_is_valid = { trigger }	# Whether this SGUI is available to the AI or not (default false)
		ai_chance = { }				# The chance that the AI will activate this SGUI (script value between 1 and 100)
		ai_frequency = {}			# Named value determining how frequently the AI will evaluate this SGUI (in months)
	}


### Using SGUIs to build lists in loc
## 	Achtung!
# 1. We are not actually executing an effect here, instead we are building a tooltip that we can then pass into localization
# 2. You can also pass scopes back and forth between script and loc although be careful to not end up stuck in a recursive loop!
# 3. Use this to build dynamic lists anywhere in localization you like granted its probably best used in panels like Journal Entries or Event desc or in tooltips
# 4. Keep in mind that this is UI work so it will refresh every frame as long as its visible, for performance reasons you may wish to actually build and update your list somewhere else (like in a JE pulse) and only pass those values into your tooltip here
# Q: Then why didnt you do that?
# A: Do you want your list or not?!
# 5. Use "[GetScriptedGui('SGUI_KEY').ExecuteTooltip(GuiScope.SetRoot(ROOT.GetCountry.MakeScope).End)]" for example in loc to build your tooltip

	my_je_sgui = {
		scope = country

		effect = {
			if = {
				limit = {
					any_scope_state = {
						devastation > 0
					}
				}
				every_scope_state = {
					limit = {
						devastation > 0
					}
					custom_tooltip = "LIST_ENTRY_KEY" # for each print a line
				}
			}
			else = {
				custom_tooltip = "LIST_EMPTY_STATE_KEY" # empty state, if we have one
			}
		}
	}
