# Capture sheet: one block per journey step

The AE fills this in during the journey walk (a whiteboard, OneNote or this file on screen). Claude captures the detail
from the transcript afterwards; the sheet is there so the **room asks the five prompts at every step** and nothing is
left to a follow-up email that could have been asked live.

## Step <n>: <their name for the step>

| Prompt | Ask | Their answer | Model |
|---|---|---|---|
| **Who** | "Who does this step? How many of them? Who checks or approves it?" | | `roles` |
| **The thing** | "What are you working on here: a job, an application, a quote? What do you call it? What status is it in when this step starts and ends?" | | `objects`, `stages` |
| **Where** | "Which system or screen? Or is it a spreadsheet, email or phone call? Are they at a desk or on site?" | | `systems`, `channels` |
| **The rule** | "Is there a limit, a deadline or a rule here? What's the number?" | | `rules` |
| **The pain** | "What goes wrong here? How often? What does it cost you: time, money, customers?" | | requirement + `pain` |

Also listen for: things they keep in a spreadsheet beside the system (a field list), "we have to ring someone"
(a missing integration or a portal), "it depends" (a rule, or branches: two paths at once means a process, not stages).

## After the walk

| | |
|---|---|
| Top 5 pains (read back) | 1. 2. 3. 4. 5. |
| Musts (voted) | |
| Disputed rule (live change candidate) | |
| AI moments | |
| They'll send, by when | |
| Next workshop date and journey | |
| Playback sign-off: who | |
