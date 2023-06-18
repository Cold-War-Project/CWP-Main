# Political parties rework

## Reasons why someone joins a party:
- Won a recent election
- Has a popular figurehead
- Has large membership (clout)
- Rallying against a mutually disliked policy
  
## Reasons to leave a party:
- Losing a lot
- Poorly liked leader
- not much membership (clout)
- Dissonance of ideals

## Variables:
- Morale (-100 to 100)
  - Increases and decreases with wins and loses
- Cumulative leader and politician popularity
- Cumulative clout
- Cognitive dissonance/consonance (-100 to 100)

## On Election Start:
- Get Leader Popularity
- Get Cumulative Clout
- Check if any law opinions that are strong are polar opposite. check if any law opinions are mid. check any neutral. 
- IGs join and leave based on calculations. 

## During the election:
- Various events fire for campaigning that raise and lower momentum. each week momentum pops and shifts based on decisions made. 

## On election end:
- winner gains morale
- losers lose morale

```ts
global = {
  every_country = {
      every_potential_party = {
        if = {
          limit = {
            var:starting_morale = {
              exists = yes
            }
            var:starting_popularity = {
              exists = yes
            }
            var:starting_clout = {
              exists = yes
            }
            var:starting_cohesion = {
              exists = yes
            }
          }
          create_variable = {
            name = party_morale
            value = var:starting_morale
          }
          create_variable = {
            name = party_popularity
            value = var:starting_popularity
          }
          create_variable = {
            name = party_clout
            value = var:starting_clout
          }
          create_variable = {
            name = party_cohesion
            value = var:starting_cohesion
          }
        }
        else = {
          create_variable = {
            name = party_morale
            value = 0
          }
          create_variable = {
            name = party_popularity
            value = 0
          }
          create_variable = {
            name = party_clout
            value = 0
          }
          create_variable = {
            name = party_cohesion
            value = 0
          }
        }
      }
  }
}
```
## example 1945 USA
```ts

GOVERNMENT = {
  c:USA = {
    py:liberal_party = {
      create_variable = {
        name = starting_morale
        value = 75
      }
      create_variable = {
        name = starting_popularity
        value = 75
      }
      create_variable = {
        name = starting_clout
        value = 25
      }
      create_variable = {
        name = starting_cohesion
        value = -50
      }
    }
  }
}
```
## List of parties
A general, global, categorization of parties, their colors, and symbols.
- Agrarian
  - Green
  - Grains and Clovers
- Anarchist
  - Black & Red
  - Black Flag or a Black and Red Flag; Circled letter A; Black Cat
- Centrist
  - Purple
  - (no traditional iconography)
- Christian Democratic
  - Orange & White
  - Christian Cross
- Communist
  - Red
  - Hammer and Sickle; shaking hands; red star
- Conservative
  - Blue
  - (no traditional iconography)
- Democratic Socialist
  - Red
  - shaking hands; red rose; fist
- Fascist
  - Black & Brown
  - Fasces (a bundle of sticks with an axe head); Swastika; various runes
- Feminist
  - White, Purple, Gold, & Pink
  - Venus Symbol; clenched fists; the letter F
- Green
  - Green
  - Sun, sunflower
- Islamist
  - Black & Green
  - Star and crescent
- Liberal
  - Yellow
  - A bird in flight
- Libertarian
  - Yellow & Gold
  - Porcupine, torch
- Monarchist
  - White, Gold & Purple
  - Crown, fleur-de-lis
- Pacifist
  - White
  - A white flag; dove; peace sign; white poppy; "V" sign
- Social Democrats
  - Red, Pink, Purple
  - Shaking Hands; Red Rose; Fist
- Socialist
  - Red
  - Red Rose

### Specific exceptions
- USA
  - Democratic
    - Blue
    - Donkey
  - Republican
    - Red
    - Elephant
- UK
  - Tory
    - Blue
    - Oak Tree
  - Labour
    - Red
    - Red Rose