# 12. Mac desktop UX: cursor, focus, permissions, and helpers

Computer-use research can look like a model-evaluation problem, but the user experience often fails for ordinary desktop reasons. On macOS and desktop-like environments, the hard part is not only whether the model can plan an action. It is whether the harness can show the screen, move the cursor, keep the right window focused, receive permissions, and recover when the operating system changes state.

This chapter treats Mac desktop computer use as a UX and integration surface. It is intentionally separate from the Anthropic computer-use API contract. Anthropic computer use defines a tool loop where an application executes actions in a VM or container and returns screenshots and results ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). Codex Desktop computer use is a product path with app settings, helper registration, and macOS permissions ([OpenAI Codex app computer use](https://developers.openai.com/codex/cloud/computer-use/)). Open-source stacks such as Cua or OpenClaw make different tradeoffs around local VMs, native helpers, and screenshots ([trycua/cua](https://github.com/trycua/cua), [OpenClaw Peekaboo issue](https://github.com/openclaw/openclaw/issues/67776)).

The practical question is: can a human watch the run, understand what is happening, and stop it before anything bad happens?

## The UX surface is part of the experiment

A text-only model request either returns a useful answer or it does not. Desktop control has more moving pieces. A run may fail because:

- the model asked for a reasonable action;
- the helper clicked the wrong coordinate;
- the active window changed;
- macOS blocked the helper from controlling the UI;
- the screenshot was stale;
- the browser was offscreen;
- a permission dialog appeared behind another window;
- the user could not tell whether the agent was paused or still acting.

Those are not minor implementation details. They determine whether the system is safe enough to use.

The Anthropic docs emphasize that the application executes the tool and that the environment should be isolated and observable ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). For a Mac desktop path, observability includes the human-visible desktop. If the run happens in a hidden helper, an invisible browser, or a screen the user cannot watch, the safety model is weaker.

## Cursor visibility

Cursor visibility sounds trivial until it fails. A user watching a desktop agent needs to know where the agent is about to click and whether the click actually happened. If the cursor is hidden, too small, or decoupled from the actual action target, the user loses the simplest feedback channel.

Record the cursor behavior for every Mac desktop experiment:

```text
Cursor visible to human:
Cursor visible in screenshots:
Cursor moves before click:
Click marker or highlight:
Cursor position logged:
Coordinate system logged:
Retina scaling handled:
```

A good harness should make cursor motion legible. It does not need theatrical animation, but it should avoid teleporting silently from one point to another. If a click is going to happen, the human should see enough context to interrupt.

Coordinate scaling is a common source of bugs. macOS may report logical points while screenshots use physical pixels. External monitors, Retina scaling, display mirroring, and remote desktop layers can all change the apparent coordinate space. If an agent clicks at `(500, 300)`, the log should say what coordinate system that means.

For a containerized Anthropic demo, display resolution is part of the tool definition and sandbox configuration. For a Mac-native helper, display resolution is partly operating-system state. That makes the Mac path more convenient but less reproducible unless the harness records the actual screen geometry.

## Focus is a state machine

Desktop agents do not act on an abstract document. They act on whichever UI element currently receives input. Focus bugs are therefore dangerous. A type action intended for a text editor may land in a terminal. A keyboard shortcut intended for a browser tab may hit the host editor. A confirmation dialog may steal focus at exactly the wrong time.

Before evaluating task success, log focus state:

```text
Active application before action:
Active window title before action:
Target application expected:
Target UI element known:
Focus changed after action:
Unexpected modal present:
```

For simple compatibility tests, choose tasks that make focus obvious. The Stage 4 control prompt in this guide asks the agent to open a text editor, type a fixed phrase, take a screenshot, and stop. That task is useful because a focus failure is visible. If the phrase appears in the wrong place, the run did not pass.

Avoid tests where focus failure can be hidden. For example, asking an agent to “configure the browser” may produce many ambiguous clicks. A better first task is “open a blank local page, click the only text box, type this exact phrase, and stop.” The page can display a large focus indicator and record the input event in the DOM.

## Permission prompts are gates, not noise

macOS desktop automation depends on permissions. Screen Recording determines whether a helper can see the screen. Accessibility determines whether it can control the UI. Some helpers also need Automation permissions or input-monitoring-like capabilities depending on implementation.

A failed permission should be recorded as a permission failure, not as model failure. Codex issue reports around computer use include helper/plugin availability and setup state problems, which are product-integration failures before any model reasoning can be judged ([openai/codex#18258](https://github.com/openai/codex/issues/18258)).

Use a permission checklist:

```text
App bundle name:
Helper bundle name:
Screen Recording granted:
Accessibility granted:
Automation granted if needed:
Permission prompt observed:
Restart required after permission:
Helper relaunched after permission:
```

Mac permissions are often bound to a specific binary path or app bundle identity. Reinstalling or updating an app can invalidate an old grant. Running a helper from a different build path can create a new identity. That means “I already granted Accessibility” may not apply to the helper actually running.

Do not click through permission prompts as part of an autonomous run. Permission grants are consequential host-level actions. The human should grant them deliberately, outside the model-controlled loop, after confirming the app identity.

## Helper registration and product state

Product desktop automation often relies on helper processes. A main app may expose a “Computer Use” switch, but the real work may be done by a background helper, extension, privileged service, plugin cache, or native bridge. If the helper is missing, stale, or not registered, the UI may show a feature that cannot actually run.

Codex Desktop reports are useful here because they show the class of failure to expect: a product may have visible computer-use controls while the local helper path is unavailable or region/account/backend state is not aligned ([openai/codex#18258](https://github.com/openai/codex/issues/18258)). Treat that as a product-state boundary.

Record:

```text
Main app version:
Helper version:
Helper process running:
Helper registered:
Feature flag or account gate:
Region/account constraint:
Plugin cache state:
Error shown to user:
Logs path:
```

The important distinction is between “the model cannot use the computer” and “the product did not install or enable the local computer-use bridge.” Those are different failures and need different fixes.

## Human-visible control

Computer use needs a stop control that the human trusts. A tiny cancel button hidden inside a chat pane is weaker than a visible pause/stop affordance near the controlled desktop. A keyboard interrupt is useful only if focus and event handling make it reliable. Closing the app window is not a good stop mechanism if background helpers keep running.

A safe Mac UX should answer these questions before the first nontrivial task:

```text
How does the human pause the run?
How does the human stop the run?
Does stop cancel queued actions?
Does stop prevent further tool calls?
Does stop kill or suspend helper processes?
Is there a visible running indicator?
Can the user see the next intended action?
```

For early experiments, prefer single-action or short-loop tasks. The user should not have to stop a runaway sequence. A first run that asks the agent to type one phrase and stop is a better UX test than a long browser workflow, because the expected action count is small.

The stop control is also part of the security model. The security chapter says to stop immediately if the agent tries to access credentials, download and run a file, navigate outside the allowlist, or submit a form unexpectedly. That policy only works if the human can notice and stop the action in time.

## Screen recording quality

The model reasons from screenshots. The user audits the same or a related visual stream. Poor screenshot quality can cause model errors and user confusion.

Check:

```text
Screenshot resolution:
Compression artifacts:
Retina scaling:
Multiple monitor handling:
Cursor included:
Menus and modals visible:
Offscreen windows excluded:
Sensitive regions masked:
```

A model may misread small text, disabled buttons, or selected fields if screenshots are downscaled aggressively. A human may not notice a dangerous target if the preview is blurry. For compatibility testing, use large fonts and simple UI. Do not start with dense production web apps.

Multiple monitors should be avoided in the first run. If a helper captures the wrong monitor or clicks on a different display than the screenshot, the result is hard to debug. Use one controlled display or one virtual desktop until the coordinate system is proven.

## Window layout reproducibility

Desktop tasks are sensitive to layout. A browser window at one size may expose a button, while another size hides it behind a menu. A text editor may open with a sidebar. A permission dialog may appear at a different location. Reproducibility requires pinning layout as much as possible.

For Mac product testing, record:

```text
Display size:
Scaling mode:
Number of monitors:
Controlled app window size:
Controlled app window position:
Browser zoom:
Font size:
Dock position:
Menu bar visibility:
```

For container or VM testing, record the equivalent virtual display geometry. Anthropic's computer-use docs and demo examples make display size part of the environment contract ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [Claude Quickstarts](https://github.com/anthropics/anthropic-quickstarts)). That is a good habit even when the product path feels more automatic.

A reproducible task should start from a known state. If the browser has old tabs, cached sessions, extensions, or a personal profile, the test is no longer clean. The security chapter already says not to use the user's real browser profile. The UX reason is the same: personal state makes failures ambiguous.

## Browser profile and keychain behavior

Mac desktop agents often interact with browsers. A real browser profile is convenient because it contains sessions and history, but it is unsafe for compatibility testing. It also makes UX results less portable. The model may see private tabs, autofill suggestions, extension popups, password prompts, or personalized content.

Use a disposable profile for web tests. If the product requires a real browser integration, make that a separate, explicitly approved test after compatibility is proven in a safe profile.

The first web task should be local or synthetic:

```text
Open a local HTML page.
Click the only input field.
Type a fixed phrase.
Take a screenshot.
Stop.
```

This avoids account state, cookie prompts, recommendation feeds, and live prompt-injection surfaces. If later tests need the internet, use allowlisted documentation domains first. Anthropic recommends limiting internet access and using dedicated environments for computer use ([Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).

## Notifications and modals

Unexpected modals are one of the most common desktop automation traps. A notification banner, update prompt, cookie dialog, permission sheet, or “restore tabs” prompt can intercept clicks and keystrokes. The model may then reason from a screen state the task designer did not expect.

Before a run:

```text
Disable nonessential notifications:
Close unrelated apps:
Dismiss update prompts:
Clear restore-session prompts:
Use a fresh local page or app state:
Verify no modal is already present:
```

During a run, log unexpected modals as their own event. If a cookie banner appears on an allowlisted documentation page, do not silently accept it unless the experiment has a human-confirmation rule for consent prompts. The security chapter treats accepting cookies and agreeing to terms as actions requiring confirmation.

## Comparing Anthropic, Codex, and open-source UX

The three paths have different UX defaults.

Anthropic's official computer-use demo is explicit about the loop: the app shows a controlled environment, executes tool calls, and returns screenshots/results. That makes it easier to instrument, but it is not the same as native Mac control.

Codex Desktop is a product experience. It may be easier to launch and more integrated with the app, but it can also hide helper details behind product state. The useful question is not whether it feels slick on first launch. The useful question is whether failures are observable and recoverable.

Open-source stacks expose more of the machinery. Cua emphasizes computer-use agents and virtualized/macOS-oriented infrastructure ([trycua/cua](https://github.com/trycua/cua)). E2B's open-computer-use points toward cloud sandboxing ([e2b-dev/open-computer-use](https://github.com/e2b-dev/open-computer-use)). OpenClaw's Peekaboo-style discussion is valuable because it separates screenshot/accessibility capture from the agent loop ([OpenClaw Peekaboo issue](https://github.com/openclaw/openclaw/issues/67776)). These projects may require more setup, but they can offer clearer harness boundaries.

A comparison should score UX and safety, not only task completion:

| Criterion | Anthropic demo | Codex Desktop | Open-source runtime |
|---|---|---|---|
| Human can watch | usually yes in demo UI | product-dependent | runtime-dependent |
| Stop control visible | app-dependent | product-dependent | buildable |
| Helper state observable | high if instrumented | often opaque | usually higher |
| Sandbox boundary | container/VM-oriented | host/product-oriented | varies |
| Screenshot/action logs | app-controlled | product logs | runtime-controlled |
| Permission complexity | lower in container | high on macOS | varies |

The best path for experimentation is not necessarily the easiest path to start. It is the path where a failed action can be explained without guessing.

## Mac experiment record

For every Mac desktop run, save a compact record:

```text
Date:
Route/runtime:
Host macOS version:
Hardware/architecture:
Display count:
Display resolution and scaling:
App version:
Helper version/state:
Permissions granted:
Browser/profile used:
Task prompt:
Human stop method:
Cursor visible:
Focus logs available:
Screenshot logs available:
Result:
Failure label if any:
```

Do not include screenshots with sensitive data in durable notes. Keep raw screenshots under `tmp/` and summarize the safe facts in the research log or decision log.

## UX pass criteria

A Mac desktop computer-use run should not be marked as a UX pass just because it completed a task. It should pass only if:

```text
The human could see the controlled screen.
The cursor/action target was understandable.
The right app/window received input.
Required permissions were known and deliberate.
The helper state was understood.
The run had a reliable stop mechanism.
No real profile, secrets, or production account was exposed.
Enough logs exist to explain failures.
```

A run that completes the task but hides helper state, uses a personal browser profile, or cannot be interrupted should be marked partial or unsafe, not pass.

## The Mac UX takeaway

Desktop computer use is not just model intelligence plus mouse clicks. It is an operating-system integration with permissions, focus, windows, helpers, screenshots, and human supervision. For this project, the Mac path should be treated as a product and harness evaluation first. Only after the human-visible control loop is safe should the model's desktop reasoning be evaluated seriously.
