# Dashboard Features Roadmap

This document captures the simplified, hackathon-ready dashboard direction for
the project.

The goal is to keep the product:
- easy for beginners and farmers to understand
- professional enough for a hackathon demo
- focused on working features instead of feature overload

## Product Rule

Keep the interface simple.

- Farmers should not see technical system fields
- Vets should see only the information needed to act
- Extra detail should live behind a clear link or button

Examples of technical fields that should stay hidden from users:
- latitude
- longitude
- location source
- raw coordinate values

## Hackathon-Ready Vet Dashboard Structure

The vet dashboard should stay focused on five main pages:

1. `Overview`
2. `Active Case`
3. `Farm Map`
4. `My Farms`
5. `Medical Records`

Support pages can still exist, but they should not crowd the main navigation.

Examples:
- schedule
- telehealth
- diagnosis
- prescriptions
- labs

These should be opened only when needed from links or action buttons.

## Main Dashboard Principle

The homepage should answer one question:

`What needs my attention right now?`

The homepage should stay light and should mainly show:
- compact stats
- urgent cases
- today's schedule
- links to deeper workflows

## Farmer Dashboard Improvement Roadmap

The farmer dashboard should feel simpler than the vet dashboard.

It should help a beginner farmer:
- see what matters today
- open the right next page
- avoid getting lost in too many cards

### Farmer overview structure

The farmer home should show only:
- compact summary counts
- cows due soon
- recent alerts
- a few clear quick actions
- links to deeper pages for the rest

### Farmer design direction

The farmer dashboard should borrow the same clean visual language as the vet
dashboard:
- one calm sidebar
- one simple header
- compact summary cards
- two main action lists
- one small quick-links area

This keeps the project consistent without making the farmer home heavy.

### What should move off the homepage

Do not keep these as large homepage sections:
- long account setup panels
- too many roadmap cards
- repeated explanation text
- detailed animal records
- full reports content

These should live behind dedicated pages instead:
- `My herd`
- `Alerts`
- `Reports`

### Farmer page rules

- The page should feel calm and easy to scan
- Important work should appear first
- Every section should support a real next action
- Extra information should be opened only when needed

### Farmer build order

1. simplify the overview arrangement
2. keep herd records on the herd page
3. keep alert follow-up on the alerts page
4. keep trends on the reports page
5. add farm location flow only after the simple dashboard works well

## Farmer-Friendly Location Feature

For the location flow, farmers should not see technical map language.

### What the farmer should see

- `My farm location`
- `Use my current location`
- `Pin my farm on map`
- `Save location`
- `Location saved`

### What the system stores behind the scenes

- latitude
- longitude
- source
- updated time

This keeps the user experience simple while still giving the system the data it
needs.

## Simplified Location Flow

1. Farmer opens the location section
2. Farmer chooses one of:
   - `Use my current location`
   - `Pin my farm on map`
3. Farmer clicks `Save location`
4. System stores the location quietly in the background
5. Vet sees the farm on the map
6. Vet clicks `Get directions`

## Best Map Strategy For Hackathon

Start with the simplest version that works:

1. save a farm location
2. show the farm marker on the vet map
3. give the vet a `Get directions` button

Avoid building advanced real-time map features too early.

## Kenya-First Map Plan

The map should start focused on `Kenya`.

This keeps the experience simple and avoids unnecessary map complexity at the
beginning.

### Default map behavior

- map opens focused on Kenya
- users do not need to search the whole world
- the system stays relevant to the project context

### Area narrowing behavior

When a user enters or selects a location:
- the map should narrow down to that place
- the zoom should move closer automatically
- the selected area should become the current working focus

Examples:
- Kenya
- Meru
- a town
- a farm area

The farmer and the vet should both be able to guide the focus of the map when
needed, but only through simple actions.

## Automatic Farmer-To-Vet Location Flow

The vet should not need to search manually once the farmer has already saved the
farm location.

### Planned workflow

1. Farmer pins the farm location or uses current location
2. Farmer saves the location
3. The system stores the farm location
4. The saved location appears automatically on the vet map
5. The vet opens the map and immediately sees the destination

This should feel automatic and reduce unnecessary clicks.

## Planned Route Display Behavior

The route experience should stay simple and visually clear.

### Minimum version

- show the farm destination marker
- show the vet location if available
- allow the vet to open directions quickly

### Better visual version

- draw a visible route line on the map
- use a strong route color like red for urgent or active direction flow
- make the destination clear without cluttering the page

### Important note

There are two route display levels:

1. `Simple line`
- a straight visible line between the vet and the farm
- easiest version for early demos

2. `Route path`
- a route that follows actual roads
- better for realism
- should only be added after the simple version works

## Simple User-Facing Map Language

To keep the feature beginner-friendly, the interface should use simple labels.

### Farmer side

- `Set farm location`
- `Use my current location`
- `Pin my farm on map`
- `Save location`
- `Location saved`

### Vet side

- `Farm location`
- `Open map`
- `Get directions`
- `Destination`
- `Route to farm`

Do not expose technical language like:
- latitude
- longitude
- source
- raw map coordinates

## Recommended Hackathon Map Demo Flow

1. Farmer opens location section
2. Farmer pins the farm or uses current location
3. Farmer saves
4. Vet opens farm map
5. Farm appears automatically
6. Route or route line is shown
7. Vet follows the map decision flow

This is a strong demo because it is:
- clear
- visual
- useful
- easy to understand quickly

## Features To Build First

### Vet side

1. `Overview`
- urgent case visibility
- next visit visibility
- quick links to active workflows

2. `Active Case`
- one active case at a time
- intervention log
- notes
- medications
- next action buttons

3. `Farm Map`
- farm markers
- simple status colors
- clear route handoff

4. `My Farms`
- assigned farms
- alert counts
- due-soon counts

5. `Medical Records`
- recent history
- treatment summaries
- lab-linked notes

### Farmer side

1. `Set farm location`
2. `Use my current location`
3. `Pin my farm on map`
4. `Save location`

## Things To Avoid

To keep the project hackathon-ready, avoid:
- exposing technical fields to users
- overloading the homepage
- too many top-level nav items
- complex admin flows with low demo value
- real-time tracking before the basic version works

## Build Order

1. keep the vet dashboard simple and clear
2. add the farmer-friendly location flow
3. store farm coordinates in the backend
4. show farm markers on the vet map
5. add `Get directions`
6. improve only after the simple version works end-to-end

## How To Make The Dashboards Hackathon-Winning

To stand out in a hackathon, the dashboards should not try to do everything.

They should feel:
- clear
- useful
- believable
- polished
- easy to demo in a few minutes

### 1. Solve one clear problem well

The dashboards should show one strong story:

- farmers can report important information simply
- vets can quickly understand what is urgent
- vets can decide what to do next
- vets can reach the farm faster

This is stronger than building many unrelated dashboard cards.

### 2. Keep each page focused on one main job

Each dashboard page should answer one question.

Examples:
- `Overview`: what needs attention right now?
- `Active Case`: what is happening in this case and what should I do next?
- `Farm Map`: where is the farm and how do I get there?
- `My Farms`: which farms need follow-up?
- `Medical Records`: what happened before?

This makes the product easier to understand for judges and users.

### 3. Make the user feel in control

The dashboard should never feel confusing or overloaded.

Good signs of control:
- one clear main action per page
- short labels
- few top-level navigation items
- important actions visible immediately
- extra detail hidden behind links instead of shown all at once

### 4. Show real usefulness, not just design

A good hackathon dashboard should help someone make a better decision.

Useful examples:
- urgent case highlighting
- clear case progress
- route guidance to the farm
- recent medical history before action
- simple AI support that suggests what to review next

Purely decorative sections should be avoided.

### 5. Keep the demo flow short and powerful

The best demo should be easy to follow.

Recommended demo story:

1. farmer saves farm location
2. system shows the farm on the map
3. vet opens the dashboard
4. vet sees the urgent case
5. vet opens the active case page
6. vet checks the map and gets directions

If the demo can be understood in under three minutes, the dashboard structure is
working well.

### 6. Use a simple but professional visual system

The dashboard should look intentional and consistent.

Use:
- one sidebar structure
- one typography direction
- one status color language
- repeated card styles
- clear spacing and hierarchy

Status colors should stay meaningful:
- red for urgent
- amber for monitoring
- green for clear
- blue for navigation, direction, or system support

### 7. Make the project structure look organized

A hackathon project feels stronger when the code structure is easy to explain.

Recommended separation:
- farmer workflows stay in farmer areas
- vet workflows stay in vet areas
- shared logic stays reusable
- dashboard pages stay task-based, not random

Important rule:
- do not mix public website content with dashboard workflow content

### 8. Build only features that can be demonstrated clearly

A feature should stay only if it improves the demo and works reliably.

Keep features that:
- help decision making
- help routing
- help communication
- help continuity of care

Avoid features that:
- are hard to explain
- are not connected to the main story
- look impressive but do not work end-to-end

### 9. Make the AI feel supportive, not risky

AI should support judgment, not replace the vet.

Good AI roles:
- summarize urgency
- suggest what to review next
- highlight possible risk
- provide a short recommendation

Bad AI roles:
- making final clinical decisions automatically
- replacing the vet's judgment
- giving long unclear paragraphs

### 10. Optimize for judging criteria

The dashboards should score well on common hackathon judging themes:

- `Impact`: solves a real farmer and veterinary coordination problem
- `Usability`: simple enough for beginners to understand
- `Technical quality`: clear working flow from user input to decision support
- `Design`: consistent, clean, and easy to navigate
- `Innovation`: useful AI plus map-assisted field response

## Project Structure Guidance

The project should stay easy to explain to judges and teammates.

### Recommended structure idea

- public website for landing and information
- farmer dashboard for simple reporting and farm-side actions
- vet dashboard for response, case review, and routing
- shared data models for farm, case, and location information
- shared AI support only where it improves action

### Dashboard architecture rule

Do not treat dashboards as a collection of random widgets.

Treat them as workflows.

That means:
- each dashboard page should have a job
- each job should connect to the next action
- each page should move the user forward

## Final Hackathon Standard

These dashboards should make a judge think:

`This team understood the real problem, built only what matters, and made it easy to use.`

## Success Standard

The product should feel like this:

### Farmer
`Set my location in one simple step`

### Vet
`See the farm, understand the case, and go there fast`
