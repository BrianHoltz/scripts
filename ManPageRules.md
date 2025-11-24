# Man Page Typography Rules

This scheme splits the content into distinct categories for clarity and consistency.

## Typography

- Underline for filesystem variables and literals: mimics hyperlinks, suggesting navigation or location.
- Italics for variables: signals that the value is a placeholder, not a literal.
- Bold for commands: highlights the impact of the action.
- Command: DodgerBlue
- Flag: DeepSkyBlue
- Filesystem Variable: MediumSeaGreen
- Filesystem Literal: Green
- Argument Variable: Orange
- Argument Literal: DarkOrange
- Freeform Variable: HotPink 
- Freeform Literal: Magenta

## Command
- Anything that can be invoked by a shell.
- E.g. <span style="color:rgb(30,144,255);font-weight:bold;">mdar</span>, <span style="color:rgb(30,144,255);font-weight:bold;">ls</span>
- Color: DodgerBlue (RGB: 30, 144, 255)

## Flag
- Switches that modify command behavior but do not represent data values themselves.
- E.g. <span style="color:rgb(0,191,255);">--help</span>, <span style="color:rgb(0,191,255);">--verbose</span>
- Color: DeepSkyBlue (RGB: 0, 191, 255)

## Filesystem Variable
- A placeholder for a (part of a) filesystem path.
- E.g. <span style="color:rgb(60,179,113);text-decoration:underline;font-style:italic;">DIRECTORY</span>, <span style="color:rgb(60,179,113);text-decoration:underline;font-style:italic;">&lt;file&gt;</span>
- Color: MediumSeaGreen (RGB: 60, 179, 113)

## Filesystem Literal
- A concrete literal (part of a) filesystem path.
- E.g. <span style="color:rgb(0,128,0);text-decoration:underline;">/dev/null</span>, <span style="color:rgb(0,128,0);text-decoration:underline;">~/.config</span>
- Color: Green (RGB: 0, 128, 0)

## Argument Variable
- A placeholder for a non-filesystem value (numbers, time, strings).
- E.g. <span style="color:rgb(255,165,0);font-style:italic;">NUMFILES</span>, <span style="color:rgb(255,165,0);font-style:italic;">duration</span>
- Color: Orange (RGB: 255, 165, 0)

## Argument Literal
- A predefined set of valid values, usually for flags.
- E.g. <span style="color:rgb(255,140,0);">yes</span>, <span style="color:rgb(255,140,0);">no</span>
- Color: DarkOrange (RGB: 255, 140, 0)

## Freeform Variable
- A placeholder for arbitrary user-generated content (names, comments, search queries).
- E.g. <span style="color:rgb(255,105,180);font-style:italic;">commit_comment</span>, <span style="color:rgb(255,105,180);font-style:italic;">project-name</span>
- Color: HotPink (RGB: 255, 105, 180)

## Freeform Literal
- Literal examples of arbitrary user-generated content (names, comments, search queries).
- E.g. <span style="color:rgb(255,0,255);">my first commit</span>, <span style="color:rgb(255,0,255);">Brian's Resume</span>
- Color: Magenta (RGB: 255, 0, 255)

## Danger
- Commands, flags, or actions that are dangerous or destructive, especially if no undo.
- E.g. <span style="color:rgb(255,0,0);font-weight:bold;">rm -rf /</span>, <span style="color:rgb(255,0,0);font-weight:bold;">--force</span>, <span style="color:rgb(255,0,0);font-weight:bold;">[DELETE]</span>
- Color: Pure Red (RGB: 255, 0, 0)

## Verbosity Example
- E.g. <span style="color:rgb(30,144,255);">-v=</span><span style="color:rgb(65,105,225);">find/mv</span> files, <span style="color:rgb(30,144,255);">-vv=</span>+debug, <span style="color:rgb(30,144,255);">-vvv=</span>+shell tracing
