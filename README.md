# tft-rolldown
Simulate tft rolldowns.

## Install
`pip install -e .`

## Example usage
Create custom .json file containing headliner data or use one from "examples" folder.  
For example to roll for any Heartsteel headliner at lvl 8, in terminal type:  
`headliners -c .\examples\lvl8_heartsteel.json`  
  
You can also specify:  
`--rolldowns` to change simulation accuracy and speed.  
`--rules` whether to apply bad luck protection rules.


For more info:  
`headliners --help`

## New! Specify copies taken
You can specify copies taken in the .json config.  
Example at:  
`.\examples\lvl7_heartsteel_copiestaken.json`  
  
You can specify copies_taken for your headliners,  
or "cost" to apply copies_taken to all champions of that cost,  
or individual champions.  
  
Note: Champions specified with "cost" won't apply copies_taken to  
champions mentioned directly (by name) in  
"other" and "headliners" categories.  

## Coming soon
1. Rolling for 3 stars with headliners mechanics.
