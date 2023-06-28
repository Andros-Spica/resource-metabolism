# Household activity profiles (NetLogo)

Directory:
>*1_householdActivityProfiles_netlogo*

The general modelling target here is that a household unit possessing stocks of different types of resources will update these (produce and consume) according to activities input and outputs. Activities are performed a number of times within a cycle (e.g. hours per day or week) according to a predefined sequence of activity IDs or activity profiles. A "farming" household could be expressed by an activity profile where a `farming` activity occupies 2/3 of their working time-person slots. There are several ways of implementing this general concept and many possible variations to how households are related to activity profiles.   

>In this section, we will be using Indus Village household framework in order to make the code more readily usable with the modules of the series, such as the Household Demography model. In this framework, the main agent class is a household (`breed [ households household ]`) and all household variables and procedures are marked with the prefix "hh_". Moreover, we will use the household variable `hh_stocks` to handle storage units of different types.

The code explanations bellow were written with the aid of [OpenAI's ChatGPT](https://chat.openai.com/).

- [Household activity profiles (NetLogo)](#household-activity-profiles-netlogo)
  - [Generic helper procedures](#generic-helper-procedures)
    - [`read-from-string`](#read-from-string)
  - [step 0: Minimal model with consume-produce fixed sequence](#step-0-minimal-model-with-consume-produce-fixed-sequence)
    - [Code explanation](#code-explanation)
  - [step 1: Multiple activities with different parameter profiles](#step-1-multiple-activities-with-different-parameter-profiles)
    - [Code explanation](#code-explanation-1)
  - [step 2: Refactoring activity parametrization](#step-2-refactoring-activity-parametrization)
    - [Code explanation](#code-explanation-2)
  - [step 3: Introducing multi-level time and activity profiles](#step-3-introducing-multi-level-time-and-activity-profiles)
    - [Code explanation](#code-explanation-3)

## Generic helper procedures

The following procedures are used throughout all versions.

### `read-from-string`

```NetLogo
to-report read-string-list [ stringList ]

  report read-from-string (word "[" stringList "]")

end
```

The `read-string-list` procedure takes a string representing a list of values (e.g., "200 100 50") and converts it into an actual list in NetLogo format by enclosing it with brackets (e.g., `[200 100 50]`). It uses the `read-from-string` function to achieve this conversion.

---

## step 0: Minimal model with consume-produce fixed sequence

This first version describe a baseline consumption of stocks (`consumption-baseline`) and the production process of a single unnamed activity (or the aggregate of a set of unnamed activities), which consumes stock items (`production-input`) while adding other items (`production-output`). As an example, we will consider `hh_stocks` to be organised into a first item representing "food" and a number of additional items representing non-food (unnamed) resources (e.g., "resource1", "resource2").  

![](screenshots/ResourceMetabolism_step0%20interface.png)

```NetLogo

breed [ households household ]

households-own
[
  hh_stocks
]

to setup

  clear-all

  create-households 1
  [
    hh_initialise
  ]

  reset-ticks

end

to hh_initialise

  ;;; load initial stocks from UI parameter initial-stocks (e.g., "200 100 50")
  set hh_stocks read-string-list initial-stocks

end

to go

  ask households
  [
    hh_consume-baseline

    hh_produce
  ]

  tick

end

to hh_consume-baseline

  ;;; subtract the baseline consumption of each element in stocks expressed by the UI parameter "consumption-baseline"
  set hh_stocks (map [ [ stocks baseline ] -> stocks - baseline ] hh_stocks (read-string-list consumption-baseline))

end

to hh_produce

  ;;; subtract the necessary production input of each element in stocks expressed by the UI parameter "production-input"
  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-string-list production-input))

  ;;; add the production output of each element in stocks expressed by the UI parameter "production-output"
  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-string-list production-output))

end
```

### Code explanation

The `setup` clears the world, creates one instance of the household breed using the `create-households` command, and calls the `hh_initialise` procedure to load the initial stock values from the user interface (UI) parameter (`initial-stocks`).

The `go` procedure is the main simulation loop. It instructs all households to perform the following actions:

1. `hh_consume-baseline`, which subtracts the baseline consumption of each resource element in the stocks based on the UI parameter called `consumption-baseline`.  
2. `hh_produce`, which:  
   1. subtracts the necessary production input of each resource element from the stocks based on the UI parameter called `production-input` and  
   2. adds the production output based on the UI parameter called `production-output`.

After each iteration, the simulation time is advanced by one tick using the `tick` command.

The `hh_consume-baseline` procedure subtracts the baseline consumption value from each element in the `hh_stocks` list using the `map` command. The baseline consumption values are obtained by parsing a UI parameter called `consumption-baseline` as a string list using the `read-string-list` procedure.

The `hh_produce` procedure subtracts the production input value and adds the production output value for each element in the `hh_stocks` list using the `map` command. The production input and output values are obtained from UI parameters `production-input` and `production-output`, respectively, after parsing them as string lists.

 Overall, this code implements a simple resource management model for households, where resources are updated based on consumption and production activities. The specific values for baseline consumption, production input, and output are provided through UI parameters, and the model can be run to observe the dynamics of resource stocks over time.

---

## step 1: Multiple activities with different parameter profiles

Developing step 0 further, we add a breakdown of the production process into two activities, each with their own input and output UI parameters.

![](screenshots/ResourceMetabolism_step1%20interface.png)

```NetLogo
breed [ households household ]

households-own
[
  hh_stocks
]

to setup

  clear-all

  create-households 1
  [
    hh_initialise
  ]

  reset-ticks

end

to hh_initialise

  ;;; load initial stocks from UI parameter initial-stocks (e.g., "200 100 50")
  set hh_stocks read-string-list initial-stocks

end

to go

  ask households
  [
    hh_consume-baseline

    hh_produce
  ]

  tick

end

to hh_consume-baseline

  ;;; subtract the baseline consumption of each element in stocks expressed by the UI parameter "consumption-baseline"
  set hh_stocks (map [ [ stocks baseline ] -> stocks - baseline ] hh_stocks (read-string-list consumption-baseline))

end

to hh_produce

  ;;; subtract the necessary production input and add the resulting output of each element in stocks
  ;;; per each activity expressed by the UI parameters "activity1-input", "activity1-output", "activity2-input", "activity2-output"

  ;;; activity 1
  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-string-list activity1-input))

  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-string-list activity1-output))

  ;;; activity 2
  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-string-list activity2-input))

  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-string-list activity2-output))

end
```

### Code explanation

The `setup` procedure remains the same as in step 0. On the other hand, the `go` procedure is modified and now performs the following actions for each household:

1. Calls the `hh_consume-baseline` procedure, which subtracts the baseline consumption value (specified by the UI parameter "consumption-baseline") from each element in the `hh_stocks` list.

2. Calls the `hh_produce` procedure, which simulates the production process with two activities. 
   1. It subtracts the necessary production input (specified by the UI parameters `activity1-input`, `activity2-input`, etc.) from each element in `hh_stocks` and 
   2. adds the resulting output (specified by the UI parameters `activity1-output`, `activity2-output`, etc.) to each element in `hh_stocks`.

After processing all households, the simulation time is incremented by calling `tick`.

---

## step 2: Refactoring activity parametrization

We pause the expansion of the code and refactor the code in a way that UI parameters specific to each activity (input and output) are set in code through a new procedure called in `setup` (`set-parameters`). This change is a preamble to the solution we aim to implement: reading a undetermined number of activity parameters from a external file (as a dataset). As a refactoring step, the behaviour of step 2 version remains the same as the one of step 1.

![](screenshots/ResourceMetabolism_step2%20interface.png)

```NetLogo
globals
[
  activity1-parameters
  activity2-parameters
]

breed [ households household ]

households-own
[
  hh_stocks
]

to setup

  clear-all

  set-parameters

  create-households 1
  [
    hh_initialise
  ]

  reset-ticks

end

to set-parameters

  set activity1-parameters [
    ;;; input
    [ 0 2 1 ]
    ;;; output
    [ 10 5 2 ]
  ]

  set activity2-parameters [
    ;;; input
    [ 0 5 1 ]
    ;;; output
    [ 0 0 10 ]
  ]

end

to hh_initialise

  ;;; load initial stocks from UI parameter initial-stocks (e.g., "200 100 50")
  set hh_stocks read-string-list initial-stocks

end

to go

  ask households
  [
    hh_consume-baseline

    hh_produce
  ]

  tick

end

to hh_consume-baseline

  ;;; subtract the baseline consumption of each element in stocks expressed by the UI parameter "consumption-baseline"
  set hh_stocks (map [ [ stocks baseline ] -> stocks - baseline ] hh_stocks (read-string-list consumption-baseline))

end

to hh_produce

  hh_perform-activity "activity 1"
  hh_perform-activity "activity 2"

end

to hh_perform-activity [ activityName ]

  ;;; subtract the necessary production input and add the resulting output of each element in stocks
  ;;; of a given activity, as expressed by the parameters "production1-input", "production1-output", "production2-input", "production2-output"

  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-activity-parameters activityName "input"))

  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-activity-parameters activityName "output"))

end

to-report read-activity-parameters [ activityName inputOrOutput ]

  let activity-parameters activity1-parameters
  if (activityName = "activity 2") [ set activity-parameters activity2-parameters ]

  let inputOrOutputIndex 0
  if (inputOrOutput = "output") [ set inputOrOutputIndex 1 ]

  report item inputOrOutputIndex activity-parameters

end

to-report read-string-list [ stringList ]

  report read-from-string (word "[" stringList "]")

end
```

### Code explanation

The global variables `activity1-parameters` and `activity2-parameters` store the parameters for two different activities. Each activity has input and output parameters specified as lists of values. For example, `activity1-parameters` has the input `[0 2 1]` and output `[10 5 2]`, while `activity2-parameters` has the input `[0 5 1]` and output `[0 0 10]`.

The `setup` procedure clears the world, sets the parameters using the `set-parameters` procedure, creates one household, and calls the `hh_initialise` procedure for each household.

The `set-parameters` procedure assigns values to the `activity1-parameters` and `activity2-parameters` lists, representing the input and output parameters for the respective activities.

The `hh_initialise` procedure loads the initial stocks of the household from a user interface (UI) parameter called `initial-stocks`. The parameter is expected to be a string representation of a list of values, which is converted to a list using the `read-string-list` procedure and assigned to the `hh_stocks` variable.

The `go` procedure is the main simulation loop. It asks each household to perform baseline consumption (`hh_consume-baseline`) and production (`hh_produce`), and then advances the simulation time by incrementing the tick.

The `hh_consume-baseline` procedure subtracts the baseline consumption values specified by the UI parameter `consumption-baseline` from each element in the `hh_stocks` list. The consumption values are read as a list of numbers using `read-string-list`, and the subtraction is performed using the `map` function.

The `hh_produce` procedure calls the `hh_perform-activity` procedure for two activities: "activity 1" and "activity 2".

The `hh_perform-activity` procedure subtracts the necessary production input and adds the resulting output to each element in the `hh_stocks` list for a given activity. The input and output parameters for the activity are obtained using the `read-activity-parameters` procedure, which selects the appropriate parameters based on the activity name and input or output flag.

The `read-activity-parameters` procedure retrieves the parameters for a specific activity from either `activity1-parameters` or `activity2-parameters` based on the provided activity name. It also selects the input or output parameters based on the `inputOrOutput` flag.

---

## step 3: Introducing multi-level time and activity profiles

We finally introduce an implementation of activity profiles, where these are the sequence of activities performed sequentially during a time-step (e.g., hours-person in a day). As before, each activity is determined by specific parameters (input and output). Each household have one activity profile and thus a specific trend in their stocks through time. As an example, we consider two activity profiles, one prioritising "activity 1" and the other "activity 2".

![](screenshots/ResourceMetabolism_step3%20interface.png)

```NetLogo
globals
[
  activity-profiles
  working-steps-per-tick

  activity1-parameters
  activity2-parameters
]

breed [ households household ]

households-own
[
  hh_stocks
  hh_activity-profile ;;; series of activities per each unit of time within a tick (e.g. hours within a day)
]

to setup

  clear-all

  set-parameters

  create-households num-profile-a-households
  [
    hh_initialise "A"
  ]

  create-households num-profile-b-households
  [
    hh_initialise "B"
  ]

  reset-ticks

end

to set-parameters

  set activity-profiles [
    [ 1 1 1 1 1 1 2 2 ]
    [ 1 1 2 2 2 2 2 2 ]
  ]
  set working-steps-per-tick length (item 0 activity-profiles)

  set activity1-parameters [
    ;;; input
    [ 0 2 2 ]
    ;;; output
    [ 10 8 0 ]
  ]

  set activity2-parameters [
    ;;; input
    [ 0 3 2 ]
    ;;; output
    [ 0 0 10 ]
  ]

end

to hh_initialise [ activityProfileType ]

  ;;; load initial stocks from UI parameter initial-stocks (e.g., "200 100 50")
  set hh_stocks read-string-list initial-stocks


  let activityProfileIndex position activityProfileType [ "A" "B" ]
  set hh_activity-profile item activityProfileIndex activity-profiles

end

to go

  ask households
  [
    hh_consume-baseline

    ;;; iterate for working steps within a tick
    ;;; following the household activity profile
    ;;; performing one activity step at a time
    foreach (n-values working-steps-per-tick [j -> j])
    [
      i ->
      let activityName (word "activity " item i hh_activity-profile)
      hh_produce activityName
    ]
  ]

  tick

end

to hh_consume-baseline

  ;;; subtract the baseline consumption of each element in stocks expressed by the UI parameter "consumption-baseline"
  set hh_stocks (map [ [ stocks baseline ] -> stocks - baseline ] hh_stocks (read-string-list consumption-baseline))

end

to hh_produce [ activityName ]

  hh_perform-activity activityName

end

to hh_perform-activity [ activityName ]

  ;;; subtract the necessary production input and add the resulting output of each element in stocks
  ;;; of a given activity, as expressed by the parameters "production1-input", "production1-output", "production2-input", "production2-output"

  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-activity-parameters activityName "input"))

  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-activity-parameters activityName "output"))

end

to-report read-activity-parameters [ activityName inputOrOutput ]

  let activity-parameters activity1-parameters
  if (activityName = "activity 2") [ set activity-parameters activity2-parameters ]

  let inputOrOutputIndex 0
  if (inputOrOutput = "output") [ set inputOrOutputIndex 1 ]

  report item inputOrOutputIndex activity-parameters

end

to-report read-string-list [ stringList ]

  report read-from-string (word "[" stringList "]")

end
```

### Code explanation

Here's a breakdown of the code (recapitulates everything):

1. Global Variables:
   - `activity-profiles`: Stores different profiles (lists of integers) for households where activities are represented as unique integers (i.e., integers are used as activity ID numbers).
   - `working-steps-per-tick`: Indicates the number of steps performed within each tick of the simulation.
   - `activity1-parameters` and `activity2-parameters`: Lists of parameters for different activities.

2. Breed Definition:
   - `breed [households household]`: Defines a breed of agents called "households."

3. Household Variables:
   - `hh_stocks`: Represents the stocks of different types of resources held by each household.
   - `hh_activity-profile`: Stores the sequence of activities (activity IDs) to be performed by the household within a tick.

4. `setup` Procedure:
   - Clears the simulation environment.
   - Sets the parameters for the simulation.
   - Creates households based on the number of profile A and profile B households specified.
   - Calls the `hh_initialise` procedure for each created household.
   - Resets the simulation ticks.

5. `set-parameters` Procedure:
   - Sets the values for the global variables and activity parameters used in the simulation.

6. `hh_initialise` Procedure:
   - Initializes the household by loading initial stocks from a user interface parameter called "initial-stocks."
   - Sets the activity profile for the household based on the provided activityProfileType (either "A" or "B").

7. `go` Procedure:
   - Executes the simulation for one tick.
   - Asks each household to perform activities sequentially according to their activity profile.
   - Iterates through each working step within a tick and calls the `hh_produce` procedure for the corresponding activity.

8. `hh_consume-baseline` Procedure:
   - Subtracts the baseline consumption value (specified by the UI parameter "consumption-baseline") from each element in the household's stocks.

9. `hh_produce` Procedure:
   - Calls the `hh_perform-activity` procedure for the given activity name.

10. `hh_perform-activity` Procedure:
    - Updates the household's stocks by subtracting the necessary production inputs and adding the resulting outputs for the given activity.
    - The production inputs and outputs are retrieved from the activity parameters based on the activity name.

11. Helper Procedures:
    - `read-activity-parameters`: Returns the activity parameters (input or output) based on the activity name and the specified type.
    - `read-string-list`: Converts a string representing a list of numbers into an actual list.

This code sets up a simulation where households perform activities based on predefined profiles and update their stocks accordingly. It demonstrates how households can consume resources, produce outputs, and manage their stocks within a simulation framework.
