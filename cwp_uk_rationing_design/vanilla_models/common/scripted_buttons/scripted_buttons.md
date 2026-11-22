UI can obtain a datamodel with all the scripted buttons via "[JournalEntry.GetScriptedButtons]". Each scripted button
can be referred to via "ScriptedButton".
Scripted buttons' properties can be accessed by UI via

- [ScriptedButton.GetName] -> provides a string
- [ScriptedButton.GetDesc] -> provides a string
- [ScriptedButton.GetShortDesc] -> provides a string (the `short_desc = X` value)
- [ScriptedButton.GetIcon] -> provides a texture (the `icon = X` value)
- [ScriptedButton.HasIcon] -> provides a bool
- [ScriptedButton.GetEffectDesc] -> provides a string
- [ScriptedButton.GetCost] -> provides a number (the `cost = X` value; display only, see note below)
- [ScriptedButton.IsVisible] -> provides a bool
- [ScriptedButton.IsPossible] -> provides a bool
- [ScriptedButton.IsAutocomplete] -> provides a bool (the `autocomplete = yes` value)
- [ScriptedButton.ExecuteEffect] -> provides nothing, executes the effect
- [ScriptedButton.HasTag('my_tag')] -> provides a bool

The optional `cost` property is a script value shown to the player via
[ScriptedButton.GetCost]. It is PURELY a display value - the code does not
consume, deduct, or enforce it in any way. Any actual cost/affordability must be
implemented in the button's own `possible` (gate) and `effect` (deduction)
blocks, e.g. via scripted triggers/effects.

The optional `tags` property is a free-form list of flags used to mark a button
for any purpose (queried by the UI via [ScriptedButton.HasTag('...')]). Any tag
string is allowed and defaults to none when omitted.

The optional `autocomplete` property makes the button complete on its own
instead of being clicked. Whenever the journal entry updates, the effect runs
for each country that may use the button if it is visible and possible, the
same rule as a click. The AI never clicks such a button. As with a clicked
button, use `possible` to stop the effect running again once it has run, e.g.
by checking a variable the effect sets, and `selected` to show it as completed.
A button with a `cooldown` runs again each time the cooldown ends and it is
still possible. On a journal entry with several involved countries, each
country completes the button separately, so a guard variable set on one
country does not stop the others. The player cannot run such a button by
command; the command is refused.

The optional `icon` property is a full path to a texture shown on the button by
the UI via [ScriptedButton.GetIcon]. Any directory works, as with modifier
icons, e.g.:

    icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds

When omitted, [ScriptedButton.HasIcon] is false and GetIcon provides no
texture, so the UI can fall back or hide the icon slot.

To show a character portrait on a tsarpoints decree, tag the button with one of
`unlocked_by_ruler`, `unlocked_by_favorite`, or `unlocked_by_heir`; the matching
ruler/favorite/heir portrait is then shown when that character exists. This
replaces the old `unlocked_by = ruler|favorite|heir` property. Example:

    je_tsarpoints_button_1 = {
      name = "je_tsarpoints_button_1_name"
      desc = "je_tsarpoints_button_1_desc"
      short_desc = "je_tsarpoints_button_1_short_desc"
      cost = tsarpoints_cost_large_value

      tags = { unlocked_by_ruler } # shows the ruler portrait

      # ... visible / possible / effect ...
    }


    scripted_button_key = {
      name = "LOC_KEY"
      desc = "LOC_KEY_DESC"
      short_desc = "LOC_KEY_SHORT_DESC"

          cost = 100 # optional: display-only value shown via GetCost, not enforced by code

          tags = { unlocked_by_ruler } # optional: any free-form tag flags

          icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds # optional: shown via GetIcon

          autocomplete = yes # optional: the effect runs on its own once visible and possible, instead of on click

          visible = { always = yes }

          #Country scope
          ai_chance = {
              base = 0
              modifier = {
                  trigger = { bureaucracy > 0 }
                  add = 5
              }
          }

          possible = {
              not = {
                  has_variable = my_cool_var
              }
          }

          effect = {
              set_variable = my_cool_var
          }
      }
