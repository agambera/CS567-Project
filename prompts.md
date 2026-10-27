# AI Prompts Log

This file records every prompt given to an AI coding assistant while building the
backend and interactive demo for our agentic AI interface, along with what the
assistant did in response and how many tokens each step used.

- **Tool:** Claude Code (CLI)
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`)
- **Date:** October 13, 2026 (about 4:30 PM to 10:00 PM MT)
- **User:** Kyler Hixon

---

## Token Usage

Token counts come from the Claude Code session log
(`~/.claude/projects/-Users-kylerhixon-Desktop-CS567-Project/fd29a7a4-2379-4ffb-8e13-0628ba2730d8.jsonl`).
Each prompt usually led to several model calls, one after each tool use (reading files,
running commands, editing). The numbers below add up all of the calls for each prompt.

- **Input (new):** prompt tokens sent without caching
- **Cache write:** prompt tokens written to the cache
- **Cache read:** prompt tokens read back from the cache. This column is large because
  the whole conversation is re-sent on every call, but cached tokens are much cheaper
  than new input.
- **Output:** tokens the model generated (code, explanations, tool calls, reasoning)

| # | Prompt | Model calls | Input (new) | Cache write | Cache read | Output |
|---|--------|------------:|------------:|------------:|-----------:|-------:|
| 1 | Build backend to show gradebook.py | 11 | 22 | 28,102 | 340,947 | 5,855 |
| 2 | Don't edit index | 6 | 12 | 6,020 | 257,348 | 3,960 |
| 3 | Redo, edit index, use scrollable box | 6 | 12 | 7,542 | 301,093 | 3,972 |
| 4 | Simpler names, easier-to-read code | 7 | 14 | 52,033 | 379,248 | 6,182 |
| 5 | Status display | 4 | 8 | 2,178 | 263,078 | 1,449 |
| 6 | 2 minute timer | 3 | 6 | 2,379 | 203,671 | 1,718 |
| 7 | START message + message stack | 6 | 12 | 6,425 | 435,554 | 4,298 |
| 8 | Box around timer, status header | 6 | 12 | 9,013 | 472,632 | 4,567 |
| 9 | Write prompts.md | 3 | 6 | 1,473 | 259,976 | 457 |
| 10 | Include token usage* | 2 | 4 | 1,102 | 175,658 | 886 |
| | **Total** | **54** | **108** | **116,267** | **3,089,205** | **33,344** |

**Total input processed:** 3,205,580 tokens (new + cache write + cache read)
**Total output:** 33,344 tokens

\* Prompt 10's counts were taken while this file was still being written, so they
leave out the final calls that wrote this file and the closing reply.

---

## Prompt 1: Build the backend

> within your current directory there is an index.html file. I would like you to design
> and create backend code that will display gradebook.py within the large center box in
> the file. I do not want it hardcoded, i am simply looking for a basic interactive demo.
> The objective of the project is to create a fake agentic AI for a research paper. The
> pdf for the paper is also in this directory. if at any point something is unclear ask,
> do not simply add code/new sections. the main.tex contains the current research paper
> with the objective

**Clarifying questions the AI asked, and the answers:**

| Question | Answer |
|----------|--------|
| Which gradebook file: the buggy `backend/SampleCode/gradebook.py` or the fixed `gradedbook/gradedbook.py`? | Buggy gradebook.py |
| The center box only shows in "Full" density. Show the code at all levels, or Full only? | Full only |
| What makes the code appear: page load, or after the user sends a request? | After the user sends a request |
| Backend: built-in Python, or Flask? | Built-in Python |

**What was done:**
- Created `backend/server.py` using only built-in Python. It serves the frontend and has
  an endpoint that reads `gradebook.py` from disk each time it's asked, so nothing is
  hardcoded.
- The endpoint only serves `.py` files inside `SampleCode`, so participants can't open
  the answer key files (`*_bugs.txt`).
- Hooked the input bar and send button in `index.html` up to the backend.
- Noted that no PDF was found in the folder, so the work was based on `main.tex`.

## Prompt 2: Don't edit index

> dont edit index

**Clarifying question:** With `index.html` off-limits, how should the page get the code?
**Answer:** The server adds the script when it sends the page.

**What was done:**
- Undid all changes to `index.html`.
- Moved the page logic into a new `backend/inject.js`. The server added a `<script>` tag
  for it each time it served the page, so `index.html` on disk stayed the same.

## Prompt 3: Redo with index edits allowed

> redo the last request i had to wipe the git commit. you are allowed to edit index but
> put the code in the scrollable box

**What was done:**
- Took the script-adding out of `server.py` (it went back to a simple file and code server).
- Put the fetch-and-display code directly into `index.html`, showing the code inside the
  new scrollable box.
- Added a few layout styles (`min-height: 0` and making the box's parent a flex column)
  so the box scrolls instead of growing past the screen.

## Prompt 4: Simpler names and easier-to-read code

> change all of the names to something more basic, and try to humanize the code (to make
> it easier to read and asjust)

**What was done:**
- Renamed what the AI had added (the existing `setDensity`, `panels` and `density-btn`
  were left alone):
  - `/api/code/` became `/code/`
  - `sendRequest()` became `send()`, and `API_BASE` became `serverUrl`
  - `id="code-box"` became `id="code"`, and `id="request-input"` became `id="message"`
  - The server's class and folder names became `Server`, `send_reply`, `this_folder`,
    `website_folder` and `code_folder`
- Added short comments explaining each step.
- Put the settings people are likely to change (`fileToShow`, `serverUrl`, `PORT`) at
  the top.

## Prompt 5: Status display

> there is a box to the upper right in index.html can you implement a status display?
> right now all it needs to say is STATUS: Code Review (this happens AFTER the initial
> response through the text box)

**What was done:**
- Gave the upper-right box `id="status"`.
- Added `showStatus(text)`, which is called with `'Code Review'` only after the code has
  loaded.

## Prompt 6: Countdown timer

> in the same box underneath the status add a 2 minute timer that counts down

**What was done:**
- Added `id="timer"` under the status.
- Added `startTimer()`, which counts down from 2:00 to 0:00 and starts when the status
  appears. It starts over if called again.

## Prompt 7: START message and message stack

> change the initial message so that nothing happens until the user types "START" and
> after that all messages appear in a stack on the bottom right window (newest on top)
> it does not need a scroll feature but make sure the box stays the same size and doesnt
> go off the screen or cover the input box

**What was done:**
- `send()` ignores everything until the user types exactly `START`. START then loads the
  code, sets the status and starts the timer.
- After START, every message goes into the bottom-right box (`id="messages"`) through
  `addMessage()`, newest on top. Older messages are cut off at the bottom of the box.
- Checked in headless Chrome with 25 messages: the box stayed the same size and didn't
  cover the input box.

## Prompt 8: Box around the timer and a status header

> put a box around the timer, and add some kind of header around status to distinguish
> them.

**What was done:**
- The status became a light blue header bar across the top of the box.
- The timer got its own bordered box with centered text.
- Both stay hidden until START.
- Fixed a sizing bug found in the screenshots: the two right-hand boxes changed height
  depending on how many messages there were. Setting them to `flex: 1 1 0px` keeps them
  equal and fixed.

## Prompt 9: Write this file

> wrap all of this conversation up into an AI prompts file in the folder called prompts.md

## Prompt 10: Add token usage

> include all the token usage

**What was done:** Added the token usage section above, using the session log.

## Prompt 11: Open the panels at every density level

> for the server and the webpage, make it so all of the current elements opene when the
> respective level is clicked. all current elements should be in low, med, high, etc.
> currently only High works and the functionality must be copied over to the other
> elements. PRIOR TO DOING ANY CODE refine this prompt and ask questions to make it more
> flushed out

Follow-up: "go ahead for this, but leave availability for more elements in Med High and Full"

**Clarifying questions the AI asked, and the answers:**

| Question | Answer |
|----------|--------|
| Only "Full" opened the panels in the code, not "High". Which was meant? | Full |
| Same elements at every level, or different ones? | Different: Low has no message stack; Medium, High and Full show everything |
| What happens if the level is changed after START? | Lock the level after START |
| What should the server do with the level? | Accept it and log it, return the same data for now |

**What was done:**
- Every level now opens the panels. A `levels` table at the top of the script lists which
  elements (`code-panel`, `status-box`, `bug-card`, `message-stack`) each level shows. To
  add a new element, give it an id, add the id to `allElements`, and add it to the levels
  that should show it.
- Split the bottom-right box into `bug-card` and `message-stack` so they can be shown or
  hidden separately. Typed messages are no longer wiped when the next bug appears.
- The level buttons lock (and the unpicked ones fade) once START is typed. They unlock
  again if START fails to reach the server.
- The frontend sends `?level=<level>` with both requests. `server.py` reads it, logs it,
  and strips it off before looking up the file. Removed old debug prints in `send_bugs`.

## Prompt 12: More agentic elements and a bugfix trigger

> can you add more sample elements that makes the interface feel more like you are
> interacting with an agentic ai? for example add a box on the left that shows what you
> would see in the terminal if asking an agent to debug the code. In addition i would like
> the timer and bug snippets to not be shown until the user sends in a message that asks
> for the agent to do a bug fix. (as long as the message contains bugfix at any point that
> counts)

**What was done:**
- **Agent terminal** (left sidebar): types out commands, shows the real output of running
  the buggy program, lists each bug it checks, and logs each Correct/Incorrect answer.
  `server.py` has a new `/run/<file>` endpoint that actually runs the sample code (only
  `.py` files in `SampleCode`, 10 second limit), so the traceback is real.
- **Agent plan** checklist in the status box (Read, Run, Analyze, Report) that ticks off
  as the agent works.
- **Agent replies** in the message stack, with "thinking" dots before each one.
- **Line highlighting**: the current bug's line is highlighted and scrolled into view.
  Line numbers were added to the code viewer at every level.
- **Bugfix trigger**: START only opens the file. The timer, plan, and bug cards wait for a
  message containing "bugfix" (any capitalization). When all bugs are answered the timer
  stops and the status says "Review Complete".
- New elements by level: Low gets none of them; Medium adds agent replies and line
  highlighting; High adds the plan checklist; Full adds the terminal. The agent takes the
  same amount of time at every level, even when its terminal is hidden.

---

## Files Created or Changed

| File | Change |
|------|--------|
| `backend/server.py` | New. Built-in Python server that shows the site and serves sample code through `/code/<file>` |
| `frontend/index.html` | Code display, START gate, status header, countdown timer, message stack |
| `backend/inject.js` | Made in prompt 2 and removed in prompt 3 (no longer used) |

**To run the demo:** `python3 backend/server.py`, then open http://localhost:8000.
Select **Full**, type `START`, and press Enter.
