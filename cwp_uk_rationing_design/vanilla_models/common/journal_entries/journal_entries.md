    journal_entry_key = {
        # root = context-based scope. either owning country, a specific country, or no scope
        # scope:journal_entry = this Journal Entry (journalentry scope)
        # scope:target = target value, with which this Journal Entry was added using `add_journal_entry` effect

        # the name is taken from loc key <journal_entry_key>
        # a concluded Journal Entry is shown in the journal's concluded tab, where the name is localized without any scope context
        # if the name relies on scoped data (ROOT, SCOPE, variables), also add loc key <journal_entry_key>_concluded - a static alternate name used for the concluded entry instead

        # optional journal entry group as specified in common/journal_entry_groups
        # the default context comes from the group
        group = <journal_entry_group>

        # optional, none/country - overrides the group's context, so one group can hold both global and country JEs
        context = <context>

        # optional DLC this journal entry belongs to, as specified in common/dlc_metadata
        # marks the entry with that DLC's badge in the journal entry panel - it does not gate
        # availability, use the `has_dlc_feature` trigger for that
        # takes a single DLC or a list; with a list the badge shows the most recent DLC the player has enabled,
        # or the most recent one listed if the player has none of them
        dlc = <dlc_metadata>
        dlc = { <dlc_metadata> <dlc_metadata> }

        # optional image that shows in the journal entry widget near the description, default = NDefines::GUI::JOURNAL_ENTRY_ICON_DEFAULT (set in /defines/00_interfaces.txt)
        icon = "gfx/interface/icons/event_icons/event_industry.dds"

        # optional trigger which determines if a journal entry can be shown when not active, default = no
        # is ignored when JE is added through `add_journal_entry` effect
        # root = owning country or no scope
        is_shown_when_inactive = {
            c:GBR = root
        }

        # whether a country should become involved when a contextless JE activates
        # root = specific country
        should_be_involved = {
        }

        # whether this JE should be visible to a country that is not involved in a contextles JE, also additionally determines who can see it when it's not active
        # root = specific country
        should_show_when_not_involved = {
        }

        # one or more scripted buttons. See common/scripted_buttons/scripted_buttons.md for more info
        scripted_button = scripted_button_key

        # optional trigger - when both this and is_shown_when_inactive is true, the JE is Activated, default = yes
        # is ignored when JE is added through `add_journal_entry` effect
        # root = owning country or no scope
        possible = {
            c:USA ?= {
                owns_entire_state_region = scope:target
            }
        }

        # optional trigger for country-context JEs - checked while the JE is inactive, before is_shown_when_inactive and possible
        # when true, the JE instance is permanently removed for this country without firing any effects, and its triggers are never evaluated again
        # only `add_journal_entry` can give the country this JE afterwards; `has_inactive_journal_entry` returns no for a removed JE
        # also removes a deactivated JE (see can_deactivate), including one originally added through `add_journal_entry`
        # keep this to cheap, permanent identity checks - a country matching it must never become relevant to the JE later
        # root = owning country
        disable_evaluation = {
            NOT = { this = c:PAT }
            NOT = { has_potential_to_form_country = PAT }
        }

        # effect which happens when a journal entry is activated by having its `is_shown_when_inactive` and `possible` triggers become true or when JE is added through `add_journal_entry` effect
        # root = owning country or no scope
        immediate = {
            c:USA ?= {
                # saved scopes can be used in any events triggered from the Journal Entry, as well as in the loc for the Journal Entry itself
                # To use saved scopes in loc: JournalEntry.GetTopScope.sCountry('saved_scope_name') or SCOPE.sCountry('saved_scope_name')
                save_scope_as = god_bless_america
                set_variable = {
                    name = freedom
                    value = 1
                }
            }

            set_variable = test_variable

            # all events in these on_actions can refer to scope:god_bless_america
            trigger_event = {
                id = test_event.1
                days = 0
                popup = yes
            }
        }

        # as immediate, but fired individually for each involved country in a contextless JE
        # root = specific country
        immediate_all_involved = {
        }

        # Journal Entry Map Mode (Optional)
        # Root Scope = State
        # map_color = {} # returns a color and paints the state
        # map_color_second = {} # returns a color and paints the state in stripes
        # map_tooltip = {} # this is a fake effect block, it serves to print the tooltip when hovering the map and is constructed like any other effect but doesnt actually fire off one, feel free to make liberal use of custom_tooltip_no_bullet here

        map_color = {
            value = "golden" # named color

            # OR

            value = { 32 112 165 } # any color code

            # OR

            lerp = {
                min_color = "grey" # color
                max_color = "red" # color
                factor = turmoil # value between 0.0 and 1.0
            }
        }

        map_color_second = {
            # same as above
        }

        map_tooltip = {
            if = {
                limit = {
                    owner ?= {
                        c:JAP ?= this
                    }
                    has_variable = cached_daimyo_loyalty
                }
                custom_tooltip_no_bullet = "MY_TOOLTIP"
            }
            else = {
                custom_tooltip = "MY_OTHER_TOOLTIP"
            }
        }

        # Zero or more outcomes. The journal entry can conclude through any of them.
        # Each non-timeout outcome's `trigger` is checked; when one becomes true the JE concludes
        # through that outcome and its `effect` runs. Outcomes are presented in the journal entry
        # panel in the order they are declared here.
        # This replaces the old complete/on_complete, fail/on_fail, invalid/on_invalid and
        # timeout/on_timeout blocks - each of those is now just an outcome with the appropriate fields/flags.
        # root = owning country or no scope
        outcome = {
            # key for the header shown for this outcome in the journal entry panel (the "how to reach this outcome" header)
            # required for all non-hidden outcomes
            # use je_standard_completion_header/je_standard_failure_header for the standard completion/failure look, or any custom key for flavor
            header = je_standard_completion_header

            # key for the header shown above this outcome's effect description (the "what happens" header)
            # required for all non-hidden outcomes
            # use je_standard_on_completion_header/je_standard_on_failure_header for the standard on completion/failure look, or any custom key for flavor
            effect_header = je_standard_on_completion_header

            # key for the flavor text shown once the journal entry has concluded through this outcome
            # required for all outcomes
            conclusion_desc = journal_entry_key_completed_desc

            # optional color used to tint this outcome's header in the panel
            # gold_positive is the standard positive/completion color, blue_negative the standard negative/failure color
            color = "gold_positive"

            # outcome flags, any combination of:
            #   hidden          - the outcome is not shown in the journal entry panel (use for silent conclusions)
            #   timeout         - this outcome is used when the JE times out (see the JE-level `timeout` below).
            #                     a timeout outcome has no `trigger`. At most one timeout outcome is allowed
            #   invalid_outcome - concluding through this outcome silently invalidates the JE. Must also be `hidden`.
            #                     At most one invalid outcome is allowed
            #   fails_subgoal   - concluding through this outcome should also fail the tracked subgoal
            #   historical      - this outcome is the one that happened historically. It is marked as such in the
            #                     journal entry panel and on the concluded entry, and may have an associated web link registered in code
            flags = {}

            # trigger which, when true, concludes the journal entry through this outcome
            # required for every non-timeout outcome
            # root = owning country or no scope
            trigger = {}

            # effect which is executed when this outcome's `trigger` becomes true
            # root = owning country or no scope
            effect = {}

            # effect fired individually for each involved country in a contextless JE
            # only valid in contextless journal entries
            # root = specific country
            effect_all_involved = {}

            # dynamically updated text describing potential event outcomes for this conclusion
            # multiple such entries can be added to an outcome
            # root = owning country or no scope
            event_outcome_desc = {}

            # alternative to event_outcome_desc using the effect system to automatically generate tooltips
            # note that the effects here are only used for description purposes and will not actually happen
            # root = owning country or no scope
            event_outcome_effect_desc = {}
        }

        # Use this to add custom gui widgets defined in a .gui file. The widget should have the specified name and will be placed in the anchor point defined by the container name. The corresponding container name anchor point exists in the journal_entry.gui. custom_widget_container_1, custom_widget_container_2 etc.
        # Custom widgets are only shown while the entry is active. A concluded entry's page shows its name (<journal_entry_key>_concluded if defined) and the outcome's conclusion_desc instead.
        widget = {
            gui = "gui/custom_widgets.gui"
            name = "widget_name_1"
            container = "custom_widget_container_1"
        }

        The ingame GUI hierarchy looks something like this:
        - JE Icon / custom_widget_container_je_icon (will replace the other)
        - custom_widget_container_1
        - JE Timeout
        - JE Status
        - custom_widget_container_2
        - scripted_buttons
        - custom_widget_container_3
        - scripted_progress_bars
        - custom_widget_container_4
        - JE Description
        - custom_widget_container_5
        - JE Involved Countries
        - custom_widget_container_6
        - JE Progress / Outcomes / Timeout
        - custom_widget_container_7

        # fires when a country becomes involved after activation of a contextless JE, ie not as a result of the should_be_involved trigger
        # root = specific country
        on_become_involved_after_activation = {
        }

        # fires when a country stops being involved in a contextless JE
        # root = specific country
        on_no_longer_involved = {
        }

        # dynamically updated text, which describes the reason for the Journal Entry
        # To use in loc or UI: [JournalEntry.GetReason]
        # If this is not specified, GetReason will instead return loc from key <journal_entry_key>_reason
        # value can be a localization key or first_valid + triggered_desc script
        # root = owning country, or the country viewing the Journal Entry for contextless JEs
        reason = {
            first_valid = {
                triggered_desc = {
                    desc = journal_entry_key_reason_net
                    trigger = {
                        c:NET ?= this
                    }
                }
                desc = journal_entry_key_reason_fallback
            }
        }

        # dynamically updated text, which describes the current status of the Journal Entry
        # To use in loc or UI: [JournalEntry.GetStatusDesc]
        # If this is not specified, GetStatusDesc will instead return loc from key <journal_entry_key>_status
        # root = owning country or no scope
        status_desc = {
            first_valid = {
                triggered_desc = {
                    desc = journal_entry_key_status_1
                    trigger = {
                        has_variable = mining_strike
                    }
                }
                triggered_desc = {
                    desc = journal_entry_key_status_2
                    trigger = {
                        has_variable = industrial_strike
                    }
                }
                triggered_desc = {
                    desc = journal_entry_key_status_2
                    trigger = {
                        has_variable = railway_strike
                    }
                }
            }
        }

        # dynamically updated text, which describes potential event outcomes when JE is activated
        # multiple such entries can be added to a JE
        # root = owning country or no scope
        event_outcome_activated_desc = {
            first_valid = {
                triggered_desc = {
                    desc = holstein_is_annexed
                    trigger = {
                        exists = c:SCH
                    }
                }
            }
        }

        # alternative to  event_outcome_activated_desc using the effect system to automatically generate tooltips
        # note that the effects here are only used for description purposes and will not actually happen
        # root = owning country or no scope
        event_outcome_activated_effect_desc = {
            header = option_gain_money
            effect = {
                add_treasury = 1000
            }
        }

        # the number of days before this journal entry forcibly times out, concluding through its `timeout` outcome,
        # which can be framed as success, failure, or neutral. If left blank or set to zero, will not time out.
        # When set, the JE must have an outcome with flags = { timeout }
        timeout = 720

        # zero or more static modifiers that will be applied to the Journal Entry when it activates, where they will propagate to the country
        # for contextless JEs, these propagate to all involved countries
        modifiers_while_active = {

        }

        # zero or more blocks, each applying a static modifier while the Journal Entry is active with its effects multiplied by a script value
        # the value is re-evaluated while the Journal Entry is active (on its update frequency) and the modifier effects follow it
        # propagates to the country like modifiers_while_active (all involved countries for contextless JEs)
        # value root = same as the Journal Entry scope (owning country or no scope)
        scaling_modifiers_while_active = {
            modifier = some_static_modifier_key
            value = {
                value = var:my_variable
                min = 0
            }
        }

        # on_action which is triggered every first day of the week
        # root = owning country or no scope
        on_weekly_pulse = {
            random_events = {
                100 = 0
                10 = test_event.2
                10 = test_event.3
                10 = test_event.4
            }
        }

        # on_action which is triggered every first day of the month
        # root = owning country or no scope
        on_monthly_pulse = {
            events = {
                test_event.5
            }
        }

        # on_action which is triggered every first day of the year
        # root = owning country or no scope
        on_yearly_pulse = {
            effect = {
                scope:god_bless_america = {
                    change_variable = {
                        name = freedom
                        add = 1
                    }
                }
            }
        }

        # a script value computing the goal completion metric
        # root = owning country or no scope
        current_value = {
            value = gdp
        }

        # when the journal entry is activated current_value and goal_add_value are evaluated and added together to determine the goal value
        # root = owning country or no scope
        goal_add_value = {
            value = gdp
            multiply = 0.25
        }

        # the highest weighted active journal entry appears in the goal tracker on the main screen
        weight = 200

        # yes/no, default = no. Marks this journal entry as the important one in its group, giving it a larger highlighted button in the journal panel (via JournalEntry.IsHighlighted). Flagging several entries in one group highlights all of them
        highlight = yes

        # yes/no, determines if this journal entry should be transfered if the player switches country through a revolution or by releasing a subject. Note that external dependencies such as country variables etc are not automatically inherited
        transferable = no

        # yes/no, determines if this journal entry is allowed to be inherited by a victorious revolution. Revolutions also get all variables from the defeated parent country, so most JEs *should* be inherited in this way
        # NOTE: transferable = yes will always mean that revolution inheritance is blocked as these JEs should stay with the player at all times
        can_revolution_inherit = yes

        # optional trigger, progress text is shown if this is defined and true
        # root = owning country or no scope
        is_progressing = {
            exists = scope:target
            scope:target = { is_under_construction = yes }
        }

        # yes/no, if yes, a progress bar is shown
        progressbar = yes

        # scripted progress bars the name and definition of the bar is placed under game/scripted_progress_bars
        scripted_progress_bar = name_of_scripted_bar

        # yes/no, if yes, the Journal Entry can return to an inactive state if its possible trigger reverts to false
        # if no or unspecified, an activated Journal Entry cannot return to being inactive even if it is no longer considered possible
        can_deactivate = yes

        # dynamically updated text, which is shown over the progress bar of the Journal Entry
        # value can be a localization key or first_valid + triggered_desc script
        # To use in loc or UI: [JournalEntry.GetProgressDesc]
        # If this is not specified, GetProgressDesc will instead return loc from key <journal_entry_key>_progress
        progress_desc = journal_entry_goal_progress_integer

        # tutorial lesson explaining HOW to complete the Journal Entry
        how_tutorial = how_tutorial_lesson_key

        # tutorial lesson explaining the WHY around the Journal Entry
        why_tutorial = why_tutorial_lesson_key

        # whether a Journal Entry should be pinned in its outliner by default for involved countries.
        Defaults to 'no'

        # whether a Journal Entry should be pinned in its outliner by default for uninvolved countries of for jes with country context.
        Defaults to 'no'
        should_be_pinned_by_default_uninvolved_or_context = yes
    }
