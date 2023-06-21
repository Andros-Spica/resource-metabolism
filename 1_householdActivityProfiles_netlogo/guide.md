# Household activity profiles (NetLogo)

Directory:
>*1_householdActivityProfiles_netlogo*

The general modelling target here is that an household unit possessing stocks of different types of resources will update these (produce and consume) according to activities input and outputs. Activities are performed a number of times within a cycle (e.g. hours per day or week) according to a predefined sequence of activity IDs or activity profiles. For example, a "farming" household could be expressed by an activity profile where a `farming` activity occupies 2/3 of the slots. There are several ways of implementing this general concept and many possible variations to how households are related to activity profiles.   

>In this section, we will be using Indus Village household framework in order to make the code more readily usable with the modules of the series, such as the Household Demography model. In this framework, the main agent class is a household (`breed [ households household ]`) and all household variables and procedures are marked with the prefix "hh_". Moreover, we will use the household variable `hh_stocks` to handle storage units of different types.


## step 0: Minimal model with consume-produce fixed sequence

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

to-report read-string-list [ stringList ]

  report read-from-string (word "[" stringList "]")

end
```

## step 1: Multiple activities with different parameter profiles

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
  ;;; per each activity expressed by the UI parameters "production1-input", "production1-output", "production2-input", "production2-output"

  ;;; production 1
  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-string-list production1-input))

  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-string-list production1-output))

  ;;; production 2
  set hh_stocks (map [ [ stocks productionInput ] -> stocks - productionInput ] hh_stocks (read-string-list production2-input))

  set hh_stocks (map [ [ stocks productionOutput ] -> stocks + productionOutput ] hh_stocks (read-string-list production2-output))

end

to-report read-string-list [ stringList ]

  report read-from-string (word "[" stringList "]")

end
```

## step 2: Refactoring activity parametrization

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

## step 3: Introducing multi-level time and activity profiles

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