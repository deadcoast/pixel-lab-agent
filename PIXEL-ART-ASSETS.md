# PIXEL ART OVERHAUL

---

## Quick patch QOL FIXES

---

ADD AN OPTION IN THE MAP TO TOGGLE MOVEMENT WHILE MAP IS UP. EVERYTIME I TOGGLE THE MAP I NEEDLESSLY HAVE TO EXIT IT TO MOVE, THEN RE ADJUST IN THE MAP, THEN EXIT TO MOVE. I UNDERSTAND THE ABILITY TO TAKE MY TIME PLANNING A ROUTE ON THE MAP IS IMPORTANT, SO WE WANT TO HAVE THE ABILITY TO CHOSE WITH A TOGGLE SUCH AS`[ ] Pause Movement on Map.

FOR INTERACTION INSTANCES LIKE LADDER REPAIRS, LOOTING, SALVAGING, ETC, THERE SHOULD BE A STYLIZED KEYBOARD KEY BUTTON BESIDE THE PLAYER. THE BOTTOM LEFT IS TOO FAR FROM THE CENTRE EYELINE AS THE ONLY OPTION. THEY DO NOT NEED TO BE REMOVED. THEY SHOUDL STAY THERE. BUT A MINIMIAL [E] WITH A DOWN ARROW ONTOP SHOULD BE PROVIDED BESIDE THE CHARACTER AS AN INDICATOR THEY CAN PRESS THAT BUTTON, AS IN, SOMETHING NEAR THEM IS INTERACTABLE; IF THEY WANT TO KNOW EXACTLY WHAT THEY HAVE TO LOOK AT THE BOTTOM LEFT FOR THE FULL TOOLTIP LIKE IT IS RIGHT NOW. BELOW IS A DIRECT EXAMPLE YOU SHOULD USE FOR THE BUTTON. USE THE THIRD ONE THAT HAS THE DEPRECATION(PUSHING DOWN) ANIMATION. IT SHOULD BE ADJUSTED AND RELEVANT SIZE TO THE GAME WITHOUT LOSING CLARITY. ADDITIONALLY, IF THE USER PRESSES E FOR INTERACT, THAT BUTTON SHOULD REACT TO THE USERS INPUT, AS IN PLAY THE ANIMATION FOR THE BUTTON PRESS.

THE ABOVE LOGIC CAN BE USED TO OVERHAUL A SIGNIFICANT PORTION OF THE UI, WHILE ADJUSTING IT TO FIT THE UI COLOR SCHEME. ULTIMATELY; THIS IS YOUR DECISION TO BALANCE. DO NOT UNDER SATURATE AND CREATE CLEARLY OUT OF PLACE CONTRASTING ASSETS. DO NOT OVER SATURATE AND DESTROY THE DESIGN BALANCE BY CREATING A OVER CONCENTRATION OF THE PIXEL AESTHETIC IN BUTTONS ONLY AND ONTHING ELSE. ITS ABOUT BALANCE WITH THE PROVIDED ASSETS, TWEAKING AND POLISHING WHAT NEEDS TO BE. CHANGES CAN BE SMALL, BUT NEED TO BE CONSISTENT APPLICATION WIDE. WE DONT CHANGE ONE THING AND CALL IT AESTHETICALLY UPDATED. WE UPDATE IT TO FIT ACROSS THE APPLIATIONS AESTHETICS.

THIS STEP IS MORE OF A PIXEL ART UI OVERHAUL BALANCE. INTRODUCTION WHERE NECESSARY, ADJUSTMENTS IN OTHER PLACES TO BALANCE IT. OVERALL COHESIVE CHOICES IN DESIGN, BALANCE AMONGST THE MODERN AND RETRO.

PRIORITIZE VISUALS, THESE ARE NOT AUDIO PASSES UNLESS THE OPPORTUNIE ASSET IS EASILY UTILIZED.

---

## PIXEL ART OVERHAULS

---

## ITEMS, PROPS, UI

```html
<div class="page">

  <section>
    <div class="ui heading wrapper">
      <h1>Containers</h1>
    </div>
    <div class="ui heading wrapper">
      <h2>Default</h2>
    </div>
    <div class="ui container">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sed efficitur libero. Nam sit amet feugiat lacus, condimentum semper dolor.
    </div>
    <div class="ui heading wrapper">
      <h2>Inset</h2>
    </div>
    <div class="ui container inset">
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sed efficitur libero. Nam sit amet feugiat lacus, condimentum semper dolor.</p>
    </div>
    <div class="ui heading wrapper">
      <h2>Raised</h2>
    </div>
    <div class="ui container raised">
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sed efficitur libero. Nam sit amet feugiat lacus, condimentum semper dolor.
    </div>
  </section>
  
  <section>
    <div class="ui heading wrapper">
      <h1>Icons</h1>
    </div>
    <div class="flex">
      <span class="icon arrow-down"></span>
      <span class="icon arrow-up"></span>
      <span class="icon arrow-left"></span>
      <span class="icon arrow-right"></span>
      <span class="icon add"></span>
      <span class="icon minus"></span>
      <span class="icon close"></span>
      <span class="icon menu"></span>
    </div>
  </section>
  
  <section>
    <div class="ui heading wrapper">
      <h1>Lists</h1>
    </div>
    <div class="ui heading wrapper">
      <h2>Default</h2>
    </div>
    <div class="ui list wrapper">
      <ul>
        <li>Item One</li>
        <li>Item Two</li>
        <li>Item Three</li>
      </ul>
    </div>
    <div class="ui heading wrapper">
      <h2>Menu</h2>
    </div>
    <div class="ui menu wrapper">
      <ul>
        <li><a>Item One</a></li>
        <li><a>Item Two</a></li>
        <li><a>Item Three</a></li>
        <li><a>Item Four</a></li>
      </ul>
    </div>
  </section>
  
  <section>
    <div class="ui heading wrapper">
      <h1>Buttons</h1>
    </div>
    <div class="ui heading wrapper">
      <h2>States</h2>
    </div>
    <div class="ui wrapper">
      <button>Default</button>
      <button class="raised">Raised</button>
      <button class="pressed">Pressed</button>
    </div>
    <div class="ui heading wrapper">
      <h2>Groups</h2>
    </div>
    <div class="ui wrapper">
      <button>Button 1</button>
      <button class="secondary">Button 2</button>
      <button class="tertiary">Button 3</button>
    </div>
    <div class="ui button-group wrapper">
      <button>Button 1</button>
      <button class="secondary">Button 2</button>
      <button class="tertiary">Button 3</button>
    </div>
    <div class="ui heading wrapper">
      <h2>Icons</h2>
    </div>
    <div class="ui wrapper">
      <button>
        <span>Default</span>
        <span class="icon arrow-right">
      </button>
    </div>
  </section>

  <section>
    <div class="ui heading wrapper">
      <h1>Inputs</h1>
    </div>
    <div class="ui heading wrapper">
      <h2>Text</h2>
    </div>
    <div class="ui input wrapper">
      <input type="text" placeholder="placeholder" />
    </div>
    <div class="ui heading wrapper">
      <h2>Multiline Text</h2>
    </div>
    <div class="ui input wrapper">
      <textarea type="text" placeholder="placeholder"></textarea>
    </div>
    <div class="ui heading wrapper">
      <h2>Checkbox</h2>
    </div>
    <div class="ui checkbox wrapper">
      
    </div>
    <div class="ui heading wrapper">
      <h2>Radio</h2>
    </div>
    <div class="ui radio wrapper">
      
    </div>
    <div class="ui heading wrapper">
      <h2>Search</h2>
    </div>
    <div class="ui input wrapper">
      <input type="text" placeholder="search..." />
      <button class="flat">Go</button>
    </div>
    <div class="ui heading wrapper">
      <h2>Dropdown</h2>
    </div>
    <div class="ui dropdown menu wrapper">
      <button>Menu</button>
      <ul>
        <li><a>Item One</a></li>
        <li><a>Item Two</a></li>
      </ul> 
    </div>
  </section>
  
  <section>
    <div class="ui heading wrapper">
      <h1>Toolbars</h1>
    </div>
    <div class="ui toolbar">
      <p class="label">Toolbar</p>
      <div class="buttons button-group">
        <button class="secondary">-</button>
        <button class="tertiary">x</button>
      </div>
    </div>
  </section>
  
  

</div>

<div class="grid"></div>
```

```scss


* { box-sizing: border-box; }

$fontName: 'Press Start 2P', cursive;

$colors: (
    primary: #cf9,
    secondary: #fc9,
    tertiary: #f69
);

$primary: #cf9;
$secondary: #fc9;
$tertiary: #f69;
$shade: rgba(0,0,0,0.15);
$shadeLight: rgba(255,255,255,0.5);

$borderColor: rgba(0,0,0,0.84);
$textColor: rgba(0,0,0,0.84);

$gridSize: 16px;
$gridMajorLines: rgba(0, 0, 0, 0.25);
$gridMinorLines: rgba(0,0,0,.2);
$gridOpacity: 0;

$pixelSize: 4px;

@function pixel($size) {
  @return ($size*$pixelSize);
}

@mixin flat() {
  box-shadow: pixel(-1) 0 0 $borderColor, 
    pixel(1) 0 0 $borderColor, 
    0 pixel(1) 0 $borderColor, 
    0 pixel(-1) 0 $borderColor;
}

@mixin bevel() {
  box-shadow: 
    inset pixel(1) pixel(1) 0 $shadeLight,
    inset pixel(-1) pixel(-1) 0 $shade,
    pixel(-1) 0 0 $borderColor, 
    pixel(1) 0 0 $borderColor, 
    0 pixel(1) 0 $borderColor, 
    0 pixel(-1) 0 $borderColor;
}

@mixin raised() {
  box-shadow: 
    inset pixel(1) pixel(1) 0 $shadeLight,
    inset pixel(-1) pixel(-1) 0 $shade,
    pixel(-1) 0 0 $borderColor, 
    pixel(1) 0 0 $borderColor, 
    0 pixel(1) 0 $borderColor, 
    0 pixel(-1) 0 $borderColor, 
    pixel(2) pixel(1) 0 $shade, 
    pixel(1) pixel(2) 0 $shade;
}

@mixin inset() {
  box-shadow: 
    inset pixel(1) pixel(1) 0 $shade, 
    pixel(-1) 0 0 $borderColor, 
    pixel(1) 0 0 lighten($borderColor,20%), 
    0 pixel(1) 0 lighten($borderColor,20%), 
    0 pixel(-1) 0 $borderColor;
}

@mixin box($background, $foreground) {
  @include flat();
  background: $background;
  color: $foreground;
  border:none;
  margin: pixel(1) 0;
  padding: pixel(4);
}

@mixin insetBox($background, $foreground) {
  @include box($background, $foreground);
  @include inset();
}

@mixin raisedBox($background, $borderColor) {
  @include box($background, $borderColor);
  @include raised();
}

@mixin button($background) {
  @include box($background, $textColor);
  @include bevel();
  font-family: $fontName;
  height: pixel(12);
  cursor: pointer;
  text-align: left;
  line-height: 1;
  margin-top: pixel(1);
  margin-left: pixel(4);
  white-space: nowrap;
  &:first-child {
    margin-left: 0;
  }
  &:hover {
    background: lighten($background, 10%);
  }
  &:active,
  &.pressed {
    @include inset();
    background: darken($background, 5%);
    
  }
}

.ui {
  font-family: $fontName;
  padding: pixel(4) 0;
  display: flex;
  &:after {
    content: "";
    display: table;
    clear: both;
  }

  & + .ui {
    padding-top: pixel(0);
  }
  
  // BASE ELEMENTS
  
  h1, h2, h3, h4, h5, h6 {
    padding:0;
    margin: 0;
    line-height:1;
  }
  
  // BUTTONS
  button {
    @include button($primary);
    // Place buttons side by side in wrapper with some space

    &.secondary { @include button($secondary); }
    &.tertiary { @include button($tertiary);  }
    & + button { 
      margin-left: pixel(4);
      // add left margin to active state to keep horizontal place
      &:active { margin-left: pixel(4); }
    }
    &.raised {
      @include raised();
      &:active,
      &.pressed {
        @include inset();
        margin: pixel(2) 0 0 pixel(4);
      }
      &:first-child:active,
      &.pressed:first-child {
        margin-left:0;
      }
    }
    
  }


  
  input, textarea {
    @include box(#fff, $textColor);
    @include inset();
    font-family: $fontName;
    width:100%;
    padding: pixel(4);
    line-height:1.42;
    height: pixel(12);
    & + button {
      margin: pixel(1) 0;
    }
  }
  
  textarea {
    min-height: pixel(20);
  }

  ul {
    width:100%;
    list-style: none;
    padding:0;
    margin:0;
    li {
      position: relative;
      padding: pixel(2) pixel(2) pixel(2) pixel(5);
      &:before {
        content: "";
        position: absolute;
        width: pixel(2);
        height: pixel(2);
        background: $textColor;
        top:0;bottom:0;
        left: 0;
        margin:auto;
      }
    }
    li a {  
      display: block;
      padding: pixel(3) pixel(4) pixel(3);
      border-top: pixel(1) solid transparent;
      border-bottom: pixel(1) solid $shade;
      &:hover {
        background: $primary;
        margin-top: pixel(-1);
        padding-top: pixel(4);
        border-top-color: $shade;
      }
    }
    li:first-child a:hover {
      margin-top: 0;
      border-top: none;
    }
    li:last-child a { 
      border-bottom-color: transparent; 
    }
  }
  
  // END BASE ELEMENTS
  
  // CONTAINER
  &.container {
    @include box(#fff, $textColor);
    margin: 0 0 pixel(6);
    padding: pixel(4);
    line-height: 1.42;
    font-size: 14px;
    &.inset {
      @include inset();
    }
    &.raised {
      @include raised();
    }
    &.no-padding,
    &.list {
      padding:0;
    }
    p:last-child { margin-bottom: 0; }
    p:first-child { margin-top: 0; }
  }
  // END CONTAINER
  
 
  
  // HEADINGS
  &.heading {
    padding-top: pixel(4);
    padding-bottom: pixel(4);
  }
  
  &.menu {
    @include box(#fff, $textColor);
    padding:0;
    margin: 0 0 pixel(6);
    ul li { padding: 0; }
    ul li:before { display: none; }
  }

  &.toolbar {
    @include box(#efefef, $textColor);
    @include bevel();
    margin: 0;
    padding: 0;
    height: pixel(12);
    align-items: space-between;
    justify-items: flex-end;
    .label {
      flex:1;
      padding-left: pixel(4);
    }
    .buttons {
      display:flex;
      button { 
        margin: 0 0 0 pixel(1);
        text-shadow: 0 1px 0 $textColor;
        text-align: center;
        &:active {
          margin-left: pixel(1);
        }
      }
    }
  }
  
  &.dropdown {
    flex-direction: column;
    button, ul {
      width:100%;
    }
    ul {
      padding-top: pixel(2);
    }
    button {
      background: #efefef;
      position: relative;
      z-index:11;
      margin-top:0;
      margin-bottom:0;
      &:active {
        background: darken(#efefef, 10%);
      }
      &:after {
        content:"";
        display: block;
        position:absolute;
        right: pixel(6);
        top: pixel(2); 
        bottom:0;
        margin: auto;
        z-index: 10;
        width: pixel(1);
        height: pixel(1);
        background: $textColor;
        box-shadow: 0 pixel(-1) 0 $textColor,
          pixel(-1) pixel(-1) 0 $textColor,
          pixel(1) pixel(-1) 0 $textColor,
          0 pixel(-2) 0 $textColor,
          pixel(1) pixel(-2) 0 $textColor,
          pixel(-1) pixel(-2) 0 $textColor,
          pixel(2) pixel(-2) 0 $textColor,
          pixel(-2) pixel(-2) 0 $textColor;
      }
    }
    ul {
      position: relative;
      z-index:10;
      margin: pixel(-1) 0 0 0;
    }
  }
}

.ui .button-group, .ui.button-group {
  button + button { 
    margin-left: 0;
    &:active {
      margin-left: 0;
    }
  }
}

// Icons

@mixin downArrow($color) {
  background: $color;
  
  box-shadow: 0 pixel(-1) 0 $color,
    pixel(-1) pixel(-1) 0 $color,
    pixel(1) pixel(-1) 0 $color,
    0 pixel(-2) 0 $color,
    pixel(1) pixel(-2) 0 $color,
    pixel(-1) pixel(-2) 0 $color,
    pixel(2) pixel(-2) 0 $color,
    pixel(-2) pixel(-2) 0 $color;
}

@mixin close($color) {
  background: $color;
  margin: pixel(2) pixel(2) 0;
  box-shadow: 
    pixel(-1) pixel(-1) 0 $color,
    pixel(1) pixel(1)  0 $color,
    pixel(2) pixel(2) 0 $color,
    pixel(-2) pixel(-2) 0 $color,
    pixel(1) pixel(-1) 0 $color,
    pixel(-1) pixel(1)  0 $color,
    pixel(-2) pixel(2) 0 $color,
    pixel(2) pixel(-2) 0 $color;
}

@mixin minus($color) {
  background: $color;
  margin: pixel(2) pixel(2) 0;
  box-shadow: 
    pixel(1) 0 0 $color,
    pixel(-1) 0  0 $color,
    pixel(2) 0 0 $color,
    pixel(-2) 0 0 $color;
}

@mixin plus($color) {
  background: $color;
  margin: pixel(2) pixel(2) 0;
  box-shadow: 
    pixel(-1) 0 0 $color,
    pixel(1) 0  0 $color,
    pixel(2) 0 0 $color,
    pixel(-2) 0 0 $color,
    0 pixel(-1) 0 $color,
    0 pixel(1)  0 $color,
    0 pixel(2) 0 $color,
    0 pixel(-2) 0 $color;
}

@mixin menu($color) {
  background: $color;
  margin: pixel(2) pixel(2) 0;
  box-shadow: 
    pixel(1) 0 0 $color,
    pixel(-1) 0  0 $color,
    pixel(2) 0 0 $color,
    pixel(-2) 0 0 $color,
    0 pixel(-2) 0 $color,
    pixel(1) pixel(-2) 0 $color,
    pixel(-1) pixel(-2)  0 $color,
    pixel(2) pixel(-2) 0 $color,
    pixel(-2) pixel(-2) 0 $color,
    0 pixel(2) 0 $color,
    pixel(1) pixel(2) 0 $color,
    pixel(-1) pixel(2)  0 $color,
    pixel(2) pixel(2) 0 $color,
    pixel(-2) pixel(2) 0 $color;
}

.icon {
  display: inline-block;
  width: pixel(1);
  height: pixel(1);
  
  &.arrow-down {
    @include downArrow($textColor);
    margin: pixel(2) pixel(2) 0;
  }
  &.arrow-up {
    @include downArrow($textColor);
    transform: rotate(180deg);
    margin: 0 pixel(2) pixel(2) pixel(2);
  }
  &.arrow-right {
    @include downArrow($textColor);
    margin: pixel(2) 0 pixel(1) pixel(2);
    transform: rotate(-90deg);
  }
  &.arrow-left {
    @include downArrow($textColor);
    margin: pixel(2) pixel(2) pixel(1) pixel(0);
    transform: rotate(90deg);
  }
  &.add {
    @include plus($textColor);
    margin: pixel(2) pixel(2) pixel(1) pixel(2);
  }
  &.close {
    @include close($textColor);
    margin: pixel(2) pixel(2) pixel(1) pixel(2);
  }
  &.minus {
    @include minus($textColor);
    margin: pixel(2) pixel(2) pixel(1) pixel(2);
  }
  &.menu {
    @include menu($textColor);
    margin: pixel(2) pixel(2) pixel(1) pixel(2);
  }
}



// PAGE STYLES

.page {
  position:absolute;
  width:100%;
  min-height:100%;
  overflow:auto;
  padding: pixel(6);
  margin:auto;
  background: repeating-linear-gradient(
    45deg,
    #efdcef,
    #efdcef pixel(4),
    #e0d0e0 pixel(4),
    #e0d0e0 pixel(8)
  );
  section {
    max-width:pixel(160);
    margin:auto;
  }
}

.grid {
  position:fixed;
  pointer-events:none;
  top:0;left:0;right:0;bottom:0;
  width:100%;
  height:100%;
  z-index:999;
  opacity: $gridOpacity;
  background-image: linear-gradient(
    0deg, 
    transparent 0px,
    transparent (($gridSize/4) - 1),
    $gridMinorLines $gridSize/4,
    transparent $gridSize/4,
    transparent ($gridSize/4)*2 - 1,
    $gridMinorLines ($gridSize/4)*2,
    transparent $gridSize/4*2,
    transparent $gridSize/4*3 - 1,
    $gridMinorLines $gridSize/4*3,
    transparent $gridSize/4*3,
    transparent $gridSize - 1,
    $gridMinorLines $gridSize
  ), linear-gradient(
    90deg, 
    transparent 0px,
    transparent (($gridSize/4) - 1),
    $gridMinorLines $gridSize/4,
    transparent $gridSize/4,
    transparent ($gridSize/4)*2 - 1,
    $gridMinorLines ($gridSize/4)*2,
    transparent $gridSize/4*2,
    transparent $gridSize/4*3 - 1,
    $gridMinorLines $gridSize/4*3,
    transparent $gridSize/4*3,
    transparent $gridSize - 1,
    $gridMinorLines $gridSize
  ),
  linear-gradient(
    0deg, 
    transparent 0px,
    transparent (($gridSize) - 1),
    $gridMajorLines $gridSize
  ), linear-gradient(
    90deg, 
    transparent 0px,
    transparent ($gridSize - 1),
    $gridMajorLines $gridSize
  );
  background-size: $gridSize $gridSize;
}

```

```html
.container
  button.button Button
  button.button.button-radius-2 Button
  button.button.button-push.button-cyan Pushy
```

```css
@import url("<https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap>");

html,
body {
  background-color: hsl(0, 0, 50);
  font-family: "Press Start 2P", cursive;
  font-size: 18px;
}

button {
  border: none;
  font-family: inherit;
  cursor: pointer;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  width: 100vw;
  height: 100vh;
}

$border-color: hsl(0, 0, 0);
$active-color: hsl(0, 70, 50);
$inner-color: hsl(75, 70, 50);

.button {
  padding: 0.5rem 1rem;
  margin: 0.3rem;
  background-color: $inner-color;
  box-shadow: 0rem 0.3rem $border-color, 0rem -0.3rem $border-color,
    0.3rem 0rem $border-color, -0.3rem 0rem $border-color;

  &.button-cyan {
    background-color: hsl(170, 70, 50);
  }

  &:hover {
    background-color: $active-color;
    color: hsl(0, 0, 95);
  }

  &.button-radius-2 {
    margin: 0.6rem;
    box-shadow: 0rem 0.3rem $inner-color, 0rem -0.3rem $inner-color,
      0.3rem 0rem $inner-color, -0.3rem 0rem $inner-color,
      // Actual border
      0.6rem 0rem $border-color,
      -0.6rem 0rem $border-color, 0rem 0.6rem $border-color,
      0rem -0.6rem $border-color, 0.3rem 0.3rem $border-color,
      0.3rem -0.3rem $border-color, -0.3rem 0.3rem $border-color,
      -0.3rem -0.3rem $border-color;
    &:hover {
      box-shadow: 0rem 0.3rem $active-color, 0rem -0.3rem $active-color,
        0.3rem 0rem $active-color, -0.3rem 0rem $active-color,
        // Actual border
        0.6rem 0rem $border-color,
        -0.6rem 0rem $border-color, 0rem 0.6rem $border-color,
        0rem -0.6rem $border-color, 0.3rem 0.3rem $border-color,
        0.3rem -0.3rem $border-color, -0.3rem 0.3rem $border-color,
        -0.3rem -0.3rem $border-color;
    }
  }

  &.button-push {
    box-shadow: 0rem 0.3rem hsl(155, 70, 75), 0rem -0.3rem $border-color,
      0.3rem 0rem $border-color, -0.3rem 0rem $border-color,
      // Lateral face
      0rem 1.5rem hsl(185, 70, 30),
      0rem 1.8rem $border-color, 0.3rem 1.5rem $border-color,
      -0.3rem 1.5rem $border-color,
      // Shadow
      0.3rem 2.1rem hsl(0, 0, 25),
      0.6rem 2.4rem hsl(0, 0, 25), 0.9rem 2.7rem hsl(0, 0, 25),
      1.2rem 3rem hsl(0, 0, 25), 0.6rem 1.8rem hsl(0, 0, 25),
      0.9rem 2.1rem hsl(0, 0, 25), 1.2rem 2.4rem hsl(0, 0, 25),
      1.5rem 2.7rem hsl(0, 0, 25);

    &:hover {
      background-color: hsl(170, 70, 50);
      transform: translateY(0.9rem);
      box-shadow: 0rem 0.3rem hsl(155, 70, 75), 0rem -0.3rem $border-color,
        0.3rem 0rem $border-color, -0.3rem 0rem $border-color,
        // Button
        0rem 0.6rem hsl(185, 70, 30),
        0rem 0.9rem $border-color, 0.3rem 0.6rem $border-color,
        -0.3rem 0.6rem $border-color,
        // Shadow
        0.3rem 1.2rem hsl(0, 0, 25),
        0.6rem 1.5rem hsl(0, 0, 25), 0.6rem 0.9rem hsl(0, 0, 25),
        0.9rem 1.2rem hsl(0, 0, 25);
    }
  }
}
```

VARIANT 2

```html
<button><span class="text">Start Game</span></button>
```

```css
/*demo purposes*/
@import url('<https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap>');

*{
  font-family: 'Press Start 2P', monospace;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 5px;
  height: 100vh;
  margin: 0;
  background: #aaaccc;
}

.fluid {
  width: 100%;
  box-sizing: border-box;
}

button{
  display: inline-block;
  background: linear-gradient(#09f 50%, #0090f0 50%);
  color: #fff;
  border: none;
  font-size: 1.4rem;
  margin: 5px;
  padding: 30px 50px;
  text-shadow: 3px 3px #000, -3px -3px #000, 0 -3px #000, 0 3px #000, 3px 0 #000, -3px 0 #000;
  box-shadow: inset 0 5px 0px rgba(255,255,255,0.2),
              inset 5px 0px 0px rgba(255,255,255,0.1),
              inset 0 -5px 0px rgba(0,0,0,0.2),
              inset -5px 0px 0px rgba(0,0,0,0.1),
              5px 0px 0px #000,
              -5px 0px 0px #000,
              0px 5px 0px #000,
              0px -5px 0px #000;
}

button:hover {
  text-shadow: 3px 3px #000, -3px -3px #000, 0 -3px #000, 0 3px #000, 3px 0 #000, -3px 0 #000, 4px 4px #000;
  box-shadow: inset 0 5px 0px rgba(255,255,255,0.4),
              inset 5px 0px 0px rgba(255,255,255,0.3),
              inset 0 -5px 0px rgba(0,0,0,0.3),
              inset -5px 0px 0px rgba(0,0,0,0.2),
              5px 0px 0px #000,
              -5px 0px 0px #000,
              0px 5px 0px #000,
              0px -5px 0px #000;
}

button:active {
  text-shadow: 3px 3px #000, -3px -3px #000, 0 -3px #000, 0 3px #000, 3px 0 #000, -3px 0 #000;
  box-shadow: inset 0 -5px 0px rgba(255,255,255,0.4),
              inset -5px 0px 0px rgba(255,255,255,0.3),
              inset 0 5px 0px rgba(0,0,0,0.3),
              inset 5px 0px 0px rgba(0,0,0,0.2),
              5px 0px 0px #000,
              -5px 0px 0px #000,
              0px 5px 0px #000,
              0px -5px 0px #000;
}
```

### PIXEL ART ANIMATED HEARTS FOR HEALTH STATUS BAR

```html
<div class="heart"></div>
```

```css
// -webkit- only animation, because css filter.
// hover for something extra. just because.
// inspired by <http://dribbble.com/shots/471972-Film-Slide>

body,html{width:100%;height:100%;margin:0;background:linear-gradient(135deg, #160C23, #7B6762)}

// resizable, as usual
$s : 15;
$cols : 7;
$rows : 7;

.heart{
position:absolute;
left:50%;
top:50%;
width:$cols*$s+px;
height:$rows*$s+px;
margin:(-$rows/2)*$s+px 0 0 (-$cols/2)*$s+px;}

.heart:hover::before{-webkit-animation-play-state:paused;border-radius:100%;opacity:0}

.heart::before{
content:'';
display:block;
transition:all 400ms;
-webkit-animation:pulse 1.2s steps(1) infinite;
width:$s+px;
height:$s+px;
margin:(-$s+px) 0 0 (-$s+px);
box-shadow:2*$s+px 1*$s+px #8e1a19,3*$s+px 1*$s+px #ac0500,5*$s+px 1*$s+px #f73f0c,6*$s+px 1*$s+px #fa5f27,1*$s+px 2*$s+px #740100,2*$s+px 2*$s+px #8e0500,3*$s+px 2*$s+px #8e1918,4*$s+px 2*$s+px #ca1300,5*$s+px 2*$s+px #f34f2b,6*$s+px 2*$s+px #df351f,7*$s+px 2*$s+px #f77c2a,1*$s+px 3*$s+px #4b0000,2*$s+px 3*$s+px #690100,3*$s+px 3*$s+px #8e0f0b,4*$s+px 3*$s+px #bf1000,5*$s+px 3*$s+px #f84010,6*$s+px 3*$s+px #f04222,7*$s+px 3*$s+px #fa5724,1*$s+px 4*$s+px #451312,2*$s+px 4*$s+px #5a0100,3*$s+px 4*$s+px #840e0c,4*$s+px 4*$s+px #a51d1a,5*$s+px 4*$s+px #ed2805,6*$s+px 4*$s+px #d9321e,7*$s+px 4*$s+px #f44622,2*$s+px 5*$s+px #3b0000,3*$s+px 5*$s+px #5d1a1b,4*$s+px 5*$s+px #8e1a19,5*$s+px 5*$s+px #a80700,6*$s+px 5*$s+px #b90a00,3*$s+px 6*$s+px #3d0000,4*$s+px 6*$s+px #551415,5*$s+px 6*$s+px #670100,4*$s+px 7*$s+px #340000;
}

@-webkit-keyframes pulse{
  50%{
    -webkit-filter:blur(1.4px);
    -webkit-transform:translate(-2px, 2px);
  }
}
```

### RANDOM NPC ENCOUNTER POTENTIAL (REQUIRES TWEAKING OF THE OUTFITS BLACK SUIT TO A MORE WAYLIGHT COLOR AND AESTHETHIC. A SIMPLE LEATHER BROWN MAY SUFFICE. IT WILL NOT BE EASY. BUT VERY MUCH WORTH IT IF ITS DONE CORRECTLY)

> (haml)

```html
.pulp-fiction
  .vincent.pf-vincent-1
  .jules.pf-jules-1
%p Original gif: Dusan Cezek
```

> (scss)

```scss
html {
    background: #676766;
}

@import url(<https://fonts.googleapis.com/css?family=VT323>);

// Modify the pixel size
$width : 0.5em;

// Colors Vincent
$black: #231f20;
$grey: #3a3a3a;
$grey-d: #383838;
$grey-l: #494949;
$skin-shadow: #af8d76;
$skin: #c0997d;
$skin-dark: #927a6a;
$grey-vl: #dcdcdc;
$white: #f5f6f7;
$gun-lg: #c6c6c6;
$gun-d: #b7b7b7;
$shadow: #515252;

// Colors Jules
$brown-vl: #3f281c;
$brown: #2a1810;
$brown-d: #160e0d;
$skin-j-shadow: #573e2b;
$skin-j: #694c34;
$skin-j-dark: #4c3628;
$grey-j-l: #b3b3b3;

body {
  font-family: 'VT323';
  background:#f4f4f4;
  p {
    position: absolute;
    right: 20px;
    bottom: 5px;
    font-size:14px;
  }
}
@mixin jules-1 {
    box-shadow:
    ($width * 5) ($width * 0) 0 $brown-vl,

    ($width * 4) ($width * 1) 0 $brown,
    ($width * 5) ($width * 1) 0 $brown-vl,
    ($width * 6) ($width * 1) 0 $brown-vl,
    ($width * 7) ($width * 1) 0 $brown-vl,

    ($width * 3) ($width * 2) 0 $brown-d,
    ($width * 4) ($width * 2) 0 $brown,
    ($width * 5) ($width * 2) 0 $brown,
    ($width * 6) ($width * 2) 0 $brown,
    ($width * 7) ($width * 2) 0 $brown-vl,
    ($width * 8) ($width * 2) 0 $brown-vl,
    
    ($width * 2) ($width * 3) 0 $brown-d,
    ($width * 3) ($width * 3) 0 $brown-d,
    ($width * 4) ($width * 3) 0 $brown,
    ($width * 5) ($width * 3) 0 $brown-d,
    ($width * 6) ($width * 3) 0 $brown,
    ($width * 7) ($width * 3) 0 $brown,
    ($width * 8) ($width * 3) 0 $brown-vl,
    ($width * 9) ($width * 3) 0 $brown-vl,
    
    ($width * 1) ($width * 4) 0 $brown-d,
    ($width * 2) ($width * 4) 0 $brown-d,
    ($width * 3) ($width * 4) 0 $brown-d,
    ($width * 4) ($width * 4) 0 $brown-d,
    ($width * 5) ($width * 4) 0 $brown-d,
    ($width * 6) ($width * 4) 0 $brown,
    ($width * 7) ($width * 4) 0 $brown-d,
    ($width * 8) ($width * 4) 0 $brown,
    ($width * 9) ($width * 4) 0 $brown-vl,
    ($width * 10) ($width * 4) 0 $brown-vl,

    ($width * 2) ($width * 5) 0 $brown-d,
    ($width * 3) ($width * 5) 0 $skin-j-shadow,
    ($width * 4) ($width * 5) 0 $skin-j,
    ($width * 5) ($width * 5) 0 $skin-j,
    ($width * 6) ($width * 5) 0 $brown-d,
    ($width * 7) ($width * 5) 0 $brown,
    ($width * 8) ($width * 5) 0 $brown,
    ($width * 9) ($width * 5) 0 $brown-vl,

    ($width * 3) ($width * 6) 0 $black,
    ($width * 4) ($width * 6) 0 $black,
    ($width * 5) ($width * 6) 0 $black,
    ($width * 6) ($width * 6) 0 $skin-j,
    ($width * 7) ($width * 6) 0 $brown,
    ($width * 8) ($width * 6) 0 $brown,

    ($width * 3) ($width * 7) 0 $brown-d,
    ($width * 4) ($width * 7) 0 $brown,
    ($width * 5) ($width * 7) 0 $brown,
    ($width * 6) ($width * 7) 0 $skin-j,
    ($width * 7) ($width * 7) 0 $brown,
    ($width * 8) ($width * 7) 0 $skin-j,

    ($width * 3) ($width * 8) 0 $brown-d,
    ($width * 4) ($width * 8) 0 $skin-j,
    ($width * 5) ($width * 8) 0 $brown,
    ($width * 6) ($width * 8) 0 $skin-j,
    ($width * 7) ($width * 8) 0 $skin-j,

    ($width * 5) ($width * 9) 0 $skin-j-dark,
    ($width * 6) ($width * 9) 0 $skin-j-dark,

    ($width * 5) ($width * 10) 0 $skin-j-dark,
    ($width * 6) ($width * 10) 0 $white,
    
    ($width * 4) ($width * 11) 0 $grey-vl,
    ($width * 5) ($width * 11) 0 $skin-j-dark,
    ($width * 6) ($width * 11) 0 $white,
    ($width * 7) ($width * 11) 0 $black,

    ($width * 3) ($width * 12) 0 $black,
    ($width * 4) ($width * 12) 0 $grey-vl,
    ($width * 5) ($width * 12) 0 $black,
    ($width * 6) ($width * 12) 0 $white,
    ($width * 7) ($width * 12) 0 $black,

    ($width * 3) ($width * 13) 0 $black,
    ($width * 4) ($width * 13) 0 $white,
    ($width * 5) ($width * 13) 0 $black,
    ($width * 6) ($width * 13) 0 $white,
    ($width * 7) ($width * 13) 0 $black,

    ($width * 3) ($width * 14) 0 $black,
    ($width * 4) ($width * 14) 0 $white,
    ($width * 5) ($width * 14) 0 $black,
    ($width * 6) ($width * 14) 0 $white,
    ($width * 7) ($width * 14) 0 $black,
    ($width * 8) ($width * 14) 0 $black,

    ($width * 3) ($width * 15) 0 $black,
    ($width * 4) ($width * 15) 0 $white,
    ($width * 5) ($width * 15) 0 $black,
    ($width * 6) ($width * 15) 0 $white,
    ($width * 7) ($width * 15) 0 $black,
    ($width * 8) ($width * 15) 0 $black,

    ($width * 2) ($width * 16) 0 $black,
    ($width * 3) ($width * 16) 0 $black,
    ($width * 4) ($width * 16) 0 $white,
    ($width * 5) ($width * 16) 0 $black,
    ($width * 6) ($width * 16) 0 $white,
    ($width * 7) ($width * 16) 0 $black,
    ($width * 8) ($width * 16) 0 $black,

    ($width * 2) ($width * 17) 0 $black,
    ($width * 3) ($width * 17) 0 $black,
    ($width * 4) ($width * 17) 0 $grey-vl,
    ($width * 5) ($width * 17) 0 $black,
    ($width * 6) ($width * 17) 0 $white,
    ($width * 7) ($width * 17) 0 $black,
    ($width * 8) ($width * 17) 0 $black,

    ($width * 2) ($width * 18) 0 $black,
    ($width * 3) ($width * 18) 0 $black,
    ($width * 4) ($width * 18) 0 $white,
    ($width * 5) ($width * 18) 0 $black,
    ($width * 6) ($width * 18) 0 $white,
    ($width * 7) ($width * 18) 0 $black,
    ($width * 8) ($width * 18) 0 $black,

    ($width * 2) ($width * 19) 0 $black,
    ($width * 3) ($width * 19) 0 $black,
    ($width * 4) ($width * 19) 0 $grey-vl,
    ($width * 5) ($width * 19) 0 $black,
    ($width * 6) ($width * 19) 0 $white,
    ($width * 7) ($width * 19) 0 $black,
    ($width * 8) ($width * 19) 0 $black,
    ($width * 9) ($width * 19) 0 $black,

    ($width * 2) ($width * 20) 0 $black,
    ($width * 3) ($width * 20) 0 $black,
    ($width * 4) ($width * 20) 0 $grey-vl,
    ($width * 5) ($width * 20) 0 $grey-vl,
    ($width * 6) ($width * 20) 0 $white,
    ($width * 7) ($width * 20) 0 $black,
    ($width * 8) ($width * 20) 0 $black,
    ($width * 9) ($width * 20) 0 $black,

    ($width * 2) ($width * 21) 0 $black,
    ($width * 3) ($width * 21) 0 $black,
    ($width * 4) ($width * 21) 0 $black,
    ($width * 5) ($width * 21) 0 $grey-j-l,
    ($width * 6) ($width * 21) 0 $black,
    ($width * 7) ($width * 21) 0 $black,
    ($width * 8) ($width * 21) 0 $black,
    ($width * 9) ($width * 21) 0 $black,

    ($width * 2) ($width * 22) 0 $black,
    ($width * 3) ($width * 22) 0 $black,
    ($width * 4) ($width * 22) 0 $black,
    ($width * 5) ($width * 22) 0 $black,
    ($width * 6) ($width * 22) 0 $black,
    ($width * 7) ($width * 22) 0 $black,
    ($width * 8) ($width * 22) 0 $black,
    ($width * 9) ($width * 22) 0 $black,

    ($width * 2) ($width * 23) 0 $black,
    ($width * 3) ($width * 23) 0 $black,
    ($width * 4) ($width * 23) 0 $black,
    ($width * 5) ($width * 23) 0 $black,
    ($width * 6) ($width * 23) 0 $black,
    ($width * 7) ($width * 23) 0 $black,
    ($width * 8) ($width * 23) 0 $black,
    ($width * 9) ($width * 23) 0 $black,

    ($width * 2) ($width * 24) 0 $black,
    ($width * 3) ($width * 24) 0 $black,
    ($width * 4) ($width * 24) 0 $black,
    ($width * 7) ($width * 24) 0 $black,
    ($width * 8) ($width * 24) 0 $black,
    ($width * 9) ($width * 24) 0 $black,

    ($width * 2) ($width * 25) 0 $black,
    ($width * 3) ($width * 25) 0 $black,
    ($width * 4) ($width * 25) 0 $black,
    ($width * 7) ($width * 25) 0 $black,
    ($width * 8) ($width * 25) 0 $black,
    ($width * 9) ($width * 25) 0 $black,

    ($width * 2) ($width * 26) 0 $black,
    ($width * 3) ($width * 26) 0 $black,
    ($width * 4) ($width * 26) 0 $black,
    ($width * 7) ($width * 26) 0 $black,
    ($width * 8) ($width * 26) 0 $black,
    ($width * 9) ($width * 26) 0 $black,

    ($width * 2) ($width * 27) 0 $skin-j-dark,
    ($width * 3) ($width * 27) 0 $black,
    ($width * 4) ($width * 27) 0 $black,
    ($width * 7) ($width * 27) 0 $black,
    ($width * 8) ($width * 27) 0 $black,
    ($width * 9) ($width * 27) 0 $skin-j-dark,

    ($width * 1) ($width * 28) 0 $gun-lg,
    ($width * 2) ($width * 28) 0 $skin-j-dark,
    ($width * 3) ($width * 28) 0 $black,
    ($width * 4) ($width * 28) 0 $black,
    ($width * 7) ($width * 28) 0 $black,
    ($width * 8) ($width * 28) 0 $black,
    ($width * 9) ($width * 28) 0 $skin-j-dark,

    ($width * 1) ($width * 29) 0 $gun-d,
    ($width * 2) ($width * 29) 0 $gun-lg,
    ($width * 3) ($width * 29) 0 $black,
    ($width * 4) ($width * 29) 0 $black,
    ($width * 7) ($width * 29) 0 $black,
    ($width * 8) ($width * 29) 0 $black,

    ($width * 1) ($width * 30) 0 $gun-lg,
    ($width * 3) ($width * 30) 0 $black,
    ($width * 4) ($width * 30) 0 $black,
    ($width * 7) ($width * 30) 0 $black,
    ($width * 8) ($width * 30) 0 $black,

    ($width * 1) ($width * 31) 0 $white,
    ($width * 4) ($width * 31) 0 $black,
    ($width * 7) ($width * 31) 0 $black,
    ($width * 8) ($width * 31) 0 $black,

    ($width * 1) ($width * 32) 0 $white,
    ($width * 4) ($width * 32) 0 $black,
    ($width * 7) ($width * 32) 0 $black,

    ($width * 4) ($width * 33) 0 $black,
    ($width * 7) ($width * 33) 0 $black,

    ($width * 4) ($width * 34) 0 $black,
    ($width * 7) ($width * 34) 0 $black,

    ($width * 4) ($width * 35) 0 $black,
    ($width * 7) ($width * 35) 0 $black,

    ($width * 4) ($width * 36) 0 $black,
    ($width * 7) ($width * 36) 0 $black,

    ($width * 4) ($width * 37) 0 $black,
    ($width * 7) ($width * 37) 0 $black,

    ($width * 4) ($width * 38) 0 $black,
    ($width * 7) ($width * 38) 0 $black,

    ($width * 4) ($width * 39) 0 $black,
    ($width * 7) ($width * 39) 0 $black,

    ($width * 1) ($width * 40) 0 $shadow,
    ($width * 2) ($width * 40) 0 $shadow,
    ($width * 3) ($width * 40) 0 $shadow,
    ($width * 4) ($width * 40) 0 $black,
    ($width * 5) ($width * 40) 0 $shadow,
    ($width * 6) ($width * 40) 0 $shadow,
    ($width * 7) ($width * 40) 0 $black,
    ($width * 8) ($width * 40) 0 $shadow

}
@mixin jules-gun {
    box-shadow:
    ($width * 5) ($width * 0) 0 $brown-vl,

    ($width * 4) ($width * 1) 0 $brown,
    ($width * 5) ($width * 1) 0 $brown-vl,
    ($width * 6) ($width * 1) 0 $brown-vl,
    ($width * 7) ($width * 1) 0 $brown-vl,

    ($width * 3) ($width * 2) 0 $brown-d,
    ($width * 4) ($width * 2) 0 $brown,
    ($width * 5) ($width * 2) 0 $brown,
    ($width * 6) ($width * 2) 0 $brown,
    ($width * 7) ($width * 2) 0 $brown-vl,
    ($width * 8) ($width * 2) 0 $brown-vl,
    
    ($width * 2) ($width * 3) 0 $brown-d,
    ($width * 3) ($width * 3) 0 $brown-d,
    ($width * 4) ($width * 3) 0 $brown,
    ($width * 5) ($width * 3) 0 $brown-d,
    ($width * 6) ($width * 3) 0 $brown,
    ($width * 7) ($width * 3) 0 $brown,
    ($width * 8) ($width * 3) 0 $brown-vl,
    ($width * 9) ($width * 3) 0 $brown-vl,
    
    ($width * 1) ($width * 4) 0 $brown-d,
    ($width * 2) ($width * 4) 0 $brown-d,
    ($width * 3) ($width * 4) 0 $brown-d,
    ($width * 4) ($width * 4) 0 $brown-d,
    ($width * 5) ($width * 4) 0 $brown-d,
    ($width * 6) ($width * 4) 0 $brown,
    ($width * 7) ($width * 4) 0 $brown-d,
    ($width * 8) ($width * 4) 0 $brown,
    ($width * 9) ($width * 4) 0 $brown-vl,
    ($width * 10) ($width * 4) 0 $brown-vl,

    ($width * 2) ($width * 5) 0 $brown-d,
    ($width * 3) ($width * 5) 0 $skin-j-shadow,
    ($width * 4) ($width * 5) 0 $skin-j,
    ($width * 5) ($width * 5) 0 $skin-j,
    ($width * 6) ($width * 5) 0 $brown-d,
    ($width * 7) ($width * 5) 0 $brown,
    ($width * 8) ($width * 5) 0 $brown,
    ($width * 9) ($width * 5) 0 $brown-vl,

    ($width * 3) ($width * 6) 0 $black,
    ($width * 4) ($width * 6) 0 $black,
    ($width * 5) ($width * 6) 0 $black,
    ($width * 6) ($width * 6) 0 $skin-j,
    ($width * 7) ($width * 6) 0 $brown,
    ($width * 8) ($width * 6) 0 $brown,

    ($width * 3) ($width * 7) 0 $brown-d,
    ($width * 4) ($width * 7) 0 $brown,
    ($width * 5) ($width * 7) 0 $brown,
    ($width * 6) ($width * 7) 0 $skin-j,
    ($width * 7) ($width * 7) 0 $brown,
    ($width * 8) ($width * 7) 0 $skin-j,

    ($width * 3) ($width * 8) 0 $brown-d,
    ($width * 4) ($width * 8) 0 $skin-j,
    ($width * 5) ($width * 8) 0 $brown,
    ($width * 6) ($width * 8) 0 $skin-j,
    ($width * 7) ($width * 8) 0 $skin-j,

    ($width * 5) ($width * 9) 0 $skin-j-dark,
    ($width * 6) ($width * 9) 0 $skin-j-dark,

    ($width * 5) ($width * 10) 0 $skin-j-dark,
    ($width * 6) ($width * 10) 0 $white,
    
    ($width * 4) ($width * 11) 0 $grey-vl,
    ($width * 5) ($width * 11) 0 $skin-j-dark,
    ($width * 6) ($width * 11) 0 $white,
    ($width * 7) ($width * 11) 0 $black,
    
    ($width * -14) ($width * 12) 0 $grey-vl,
    ($width * -13) ($width * 12) 0 $grey-vl,
    ($width * -12) ($width * 12) 0 $grey-vl,
    ($width * -11) ($width * 12) 0 $grey-j-l,
    ($width * -10) ($width * 12) 0 $grey-vl,
    ($width * 4) ($width * 12) 0 $grey-vl,
    ($width * 5) ($width * 12) 0 $black,
    ($width * 6) ($width * 12) 0 $white,
    ($width * 7) ($width * 12) 0 $black,
    
    ($width * -11) ($width * 13) 0 $grey-vl,
    ($width * -10) ($width * 13) 0 $skin-j,
    ($width * -9) ($width * 13) 0 $skin-j,
    ($width * -8) ($width * 13) 0 $black,
    ($width * -7) ($width * 13) 0 $black,
    ($width * -6) ($width * 13) 0 $black,
    ($width * -5) ($width * 13) 0 $black,
    ($width * -4) ($width * 13) 0 $black,
    ($width * -3) ($width * 13) 0 $black,
    ($width * -2) ($width * 13) 0 $black,
    ($width * -1) ($width * 13) 0 $black,
    ($width * 0) ($width * 13) 0 $black,
    ($width * 1) ($width * 13) 0 $black,
    ($width * 2) ($width * 13) 0 $black,
    ($width * 3) ($width * 13) 0 $black,
    ($width * 4) ($width * 13) 0 $white,
    ($width * 5) ($width * 13) 0 $black,
    ($width * 6) ($width * 13) 0 $white,
    ($width * 7) ($width * 13) 0 $black,
    
    ($width * -10) ($width * 14) 0 $black,
    ($width * 1) ($width * 14) 0 $black,
    ($width * 2) ($width * 14) 0 $black,
    ($width * 3) ($width * 14) 0 $black,
    ($width * 4) ($width * 14) 0 $white,
    ($width * 5) ($width * 14) 0 $black,
    ($width * 6) ($width * 14) 0 $white,
    ($width * 7) ($width * 14) 0 $black,
    ($width * 8) ($width * 14) 0 $black,

    ($width * 1) ($width * 15) 0 $black,
    ($width * 2) ($width * 15) 0 $black,
    ($width * 3) ($width * 15) 0 $black,
    ($width * 4) ($width * 15) 0 $white,
    ($width * 5) ($width * 15) 0 $black,
    ($width * 6) ($width * 15) 0 $white,
    ($width * 7) ($width * 15) 0 $black,
    ($width * 8) ($width * 15) 0 $black,

    ($width * 2) ($width * 16) 0 $black,
    ($width * 3) ($width * 16) 0 $black,
    ($width * 4) ($width * 16) 0 $white,
    ($width * 5) ($width * 16) 0 $black,
    ($width * 6) ($width * 16) 0 $white,
    ($width * 7) ($width * 16) 0 $black,
    ($width * 8) ($width * 16) 0 $black,

    ($width * 2) ($width * 17) 0 $black,
    ($width * 3) ($width * 17) 0 $black,
    ($width * 4) ($width * 17) 0 $grey-vl,
    ($width * 5) ($width * 17) 0 $black,
    ($width * 6) ($width * 17) 0 $white,
    ($width * 7) ($width * 17) 0 $black,
    ($width * 8) ($width * 17) 0 $black,

    ($width * 2) ($width * 18) 0 $black,
    ($width * 3) ($width * 18) 0 $black,
    ($width * 4) ($width * 18) 0 $white,
    ($width * 5) ($width * 18) 0 $black,
    ($width * 6) ($width * 18) 0 $white,
    ($width * 7) ($width * 18) 0 $black,
    ($width * 8) ($width * 18) 0 $black,

    ($width * 2) ($width * 19) 0 $black,
    ($width * 3) ($width * 19) 0 $black,
    ($width * 4) ($width * 19) 0 $grey-vl,
    ($width * 5) ($width * 19) 0 $black,
    ($width * 6) ($width * 19) 0 $white,
    ($width * 7) ($width * 19) 0 $black,
    ($width * 8) ($width * 19) 0 $black,
    ($width * 9) ($width * 19) 0 $black,

    ($width * 2) ($width * 20) 0 $black,
    ($width * 3) ($width * 20) 0 $black,
    ($width * 4) ($width * 20) 0 $grey-vl,
    ($width * 5) ($width * 20) 0 $grey-vl,
    ($width * 6) ($width * 20) 0 $white,
    ($width * 7) ($width * 20) 0 $black,
    ($width * 8) ($width * 20) 0 $black,
    ($width * 9) ($width * 20) 0 $black,

    ($width * 2) ($width * 21) 0 $black,
    ($width * 3) ($width * 21) 0 $black,
    ($width * 4) ($width * 21) 0 $black,
    ($width * 5) ($width * 21) 0 $grey-j-l,
    ($width * 6) ($width * 21) 0 $black,
    ($width * 7) ($width * 21) 0 $black,
    ($width * 8) ($width * 21) 0 $black,
    ($width * 9) ($width * 21) 0 $black,

    ($width * 2) ($width * 22) 0 $black,
    ($width * 3) ($width * 22) 0 $black,
    ($width * 4) ($width * 22) 0 $black,
    ($width * 5) ($width * 22) 0 $black,
    ($width * 6) ($width * 22) 0 $black,
    ($width * 7) ($width * 22) 0 $black,
    ($width * 8) ($width * 22) 0 $black,
    ($width * 9) ($width * 22) 0 $black,


    ($width * 3) ($width * 23) 0 $black,
    ($width * 4) ($width * 23) 0 $black,
    ($width * 5) ($width * 23) 0 $black,
    ($width * 6) ($width * 23) 0 $black,
    ($width * 7) ($width * 23) 0 $black,
    ($width * 8) ($width * 23) 0 $black,
    ($width * 9) ($width * 23) 0 $black,


    ($width * 3) ($width * 24) 0 $black,
    ($width * 4) ($width * 24) 0 $black,
    ($width * 7) ($width * 24) 0 $black,
    ($width * 8) ($width * 24) 0 $black,
    ($width * 9) ($width * 24) 0 $black,

    ($width * 3) ($width * 25) 0 $black,
    ($width * 4) ($width * 25) 0 $black,
    ($width * 7) ($width * 25) 0 $black,
    ($width * 8) ($width * 25) 0 $black,
    ($width * 9) ($width * 25) 0 $black,

    ($width * 3) ($width * 26) 0 $black,
    ($width * 4) ($width * 26) 0 $black,
    ($width * 7) ($width * 26) 0 $black,
    ($width * 8) ($width * 26) 0 $black,
    ($width * 9) ($width * 26) 0 $black,

    ($width * 3) ($width * 27) 0 $black,
    ($width * 4) ($width * 27) 0 $black,
    ($width * 7) ($width * 27) 0 $black,
    ($width * 8) ($width * 27) 0 $black,
    ($width * 9) ($width * 27) 0 $skin-j-dark,

    ($width * 3) ($width * 28) 0 $black,
    ($width * 4) ($width * 28) 0 $black,
    ($width * 7) ($width * 28) 0 $black,
    ($width * 8) ($width * 28) 0 $black,
    ($width * 9) ($width * 28) 0 $skin-j-dark,

    ($width * 3) ($width * 29) 0 $black,
    ($width * 4) ($width * 29) 0 $black,
    ($width * 7) ($width * 29) 0 $black,
    ($width * 8) ($width * 29) 0 $black,

    ($width * 3) ($width * 30) 0 $black,
    ($width * 4) ($width * 30) 0 $black,
    ($width * 7) ($width * 30) 0 $black,
    ($width * 8) ($width * 30) 0 $black,

    ($width * 4) ($width * 31) 0 $black,
    ($width * 7) ($width * 31) 0 $black,
    ($width * 8) ($width * 31) 0 $black,

    ($width * 4) ($width * 32) 0 $black,
    ($width * 7) ($width * 32) 0 $black,

    ($width * 4) ($width * 33) 0 $black,
    ($width * 7) ($width * 33) 0 $black,

    ($width * 4) ($width * 34) 0 $black,
    ($width * 7) ($width * 34) 0 $black,

    ($width * 4) ($width * 35) 0 $black,
    ($width * 7) ($width * 35) 0 $black,

    ($width * 4) ($width * 36) 0 $black,
    ($width * 7) ($width * 36) 0 $black,

    ($width * 4) ($width * 37) 0 $black,
    ($width * 7) ($width * 37) 0 $black,

    ($width * 4) ($width * 38) 0 $black,
    ($width * 7) ($width * 38) 0 $black,

    ($width * 4) ($width * 39) 0 $black,
    ($width * 7) ($width * 39) 0 $black,

    ($width * 1) ($width * 40) 0 $shadow,
    ($width * 2) ($width * 40) 0 $shadow,
    ($width * 3) ($width * 40) 0 $shadow,
    ($width * 4) ($width * 40) 0 $black,
    ($width * 5) ($width * 40) 0 $shadow,
    ($width * 6) ($width * 40) 0 $shadow,
    ($width * 7) ($width * 40) 0 $black,
    ($width * 8) ($width * 40) 0 $shadow
}
@mixin jules-fire {
    box-shadow:
    ($width * 5) ($width * 0) 0 $brown-vl,

    ($width * 4) ($width * 1) 0 $brown,
    ($width * 5) ($width * 1) 0 $brown-vl,
    ($width * 6) ($width * 1) 0 $brown-vl,
    ($width * 7) ($width * 1) 0 $brown-vl,

    ($width * 3) ($width * 2) 0 $brown-d,
    ($width * 4) ($width * 2) 0 $brown,
    ($width * 5) ($width * 2) 0 $brown,
    ($width * 6) ($width * 2) 0 $brown,
    ($width * 7) ($width * 2) 0 $brown-vl,
    ($width * 8) ($width * 2) 0 $brown-vl,
    
    ($width * 2) ($width * 3) 0 $brown-d,
    ($width * 3) ($width * 3) 0 $brown-d,
    ($width * 4) ($width * 3) 0 $brown,
    ($width * 5) ($width * 3) 0 $brown-d,
    ($width * 6) ($width * 3) 0 $brown,
    ($width * 7) ($width * 3) 0 $brown,
    ($width * 8) ($width * 3) 0 $brown-vl,
    ($width * 9) ($width * 3) 0 $brown-vl,
    
    ($width * 1) ($width * 4) 0 $brown-d,
    ($width * 2) ($width * 4) 0 $brown-d,
    ($width * 3) ($width * 4) 0 $brown-d,
    ($width * 4) ($width * 4) 0 $brown-d,
    ($width * 5) ($width * 4) 0 $brown-d,
    ($width * 6) ($width * 4) 0 $brown,
    ($width * 7) ($width * 4) 0 $brown-d,
    ($width * 8) ($width * 4) 0 $brown,
    ($width * 9) ($width * 4) 0 $brown-vl,
    ($width * 10) ($width * 4) 0 $brown-vl,

    ($width * 2) ($width * 5) 0 $brown-d,
    ($width * 3) ($width * 5) 0 $skin-j-shadow,
    ($width * 4) ($width * 5) 0 $skin-j,
    ($width * 5) ($width * 5) 0 $skin-j,
    ($width * 6) ($width * 5) 0 $brown-d,
    ($width * 7) ($width * 5) 0 $brown,
    ($width * 8) ($width * 5) 0 $brown,
    ($width * 9) ($width * 5) 0 $brown-vl,

    ($width * 3) ($width * 6) 0 $black,
    ($width * 4) ($width * 6) 0 $black,
    ($width * 5) ($width * 6) 0 $black,
    ($width * 6) ($width * 6) 0 $skin-j,
    ($width * 7) ($width * 6) 0 $brown,
    ($width * 8) ($width * 6) 0 $brown,

    ($width * 3) ($width * 7) 0 $brown-d,
    ($width * 4) ($width * 7) 0 $brown,
    ($width * 5) ($width * 7) 0 $brown,
    ($width * 6) ($width * 7) 0 $skin-j,
    ($width * 7) ($width * 7) 0 $brown,
    ($width * 8) ($width * 7) 0 $skin-j,

    ($width * 3) ($width * 8) 0 $brown-d,
    ($width * 4) ($width * 8) 0 $skin-j,
    ($width * 5) ($width * 8) 0 $brown,
    ($width * 6) ($width * 8) 0 $skin-j,
    ($width * 7) ($width * 8) 0 $skin-j,

    ($width * 5) ($width * 9) 0 $skin-j-dark,
    ($width * 6) ($width * 9) 0 $skin-j-dark,

    ($width * 5) ($width * 10) 0 $skin-j-dark,
    ($width * 6) ($width * 10) 0 $white,
    
    ($width * -17) ($width * 11) 0 $white,
    ($width * 4) ($width * 11) 0 $grey-vl,
    ($width * 5) ($width * 11) 0 $skin-j-dark,
    ($width * 6) ($width * 11) 0 $white,
    ($width * 7) ($width * 11) 0 $black,
    

    ($width * -16) ($width * 12) 0 $white,
    ($width * -14) ($width * 12) 0 $grey-vl,
    ($width * -13) ($width * 12) 0 $grey-vl,
    ($width * -12) ($width * 12) 0 $grey-vl,
    ($width * -11) ($width * 12) 0 $grey-j-l,
    ($width * -10) ($width * 12) 0 $grey-vl,
    ($width * 4) ($width * 12) 0 $grey-vl,
    ($width * 5) ($width * 12) 0 $black,
    ($width * 6) ($width * 12) 0 $white,
    ($width * 7) ($width * 12) 0 $black,
    
    ($width * -17) ($width * 13) 0 $white,
    ($width * -11) ($width * 13) 0 $grey-vl,
    ($width * -10) ($width * 13) 0 $skin-j,
    ($width * -9) ($width * 13) 0 $skin-j,
    ($width * -8) ($width * 13) 0 $black,
    ($width * -7) ($width * 13) 0 $black,
    ($width * -6) ($width * 13) 0 $black,
    ($width * -5) ($width * 13) 0 $black,
    ($width * -4) ($width * 13) 0 $black,
    ($width * -3) ($width * 13) 0 $black,
    ($width * -2) ($width * 13) 0 $black,
    ($width * -1) ($width * 13) 0 $black,
    ($width * 0) ($width * 13) 0 $black,
    ($width * 1) ($width * 13) 0 $black,
    ($width * 2) ($width * 13) 0 $black,
    ($width * 3) ($width * 13) 0 $black,
    ($width * 4) ($width * 13) 0 $white,
    ($width * 5) ($width * 13) 0 $black,
    ($width * 6) ($width * 13) 0 $white,
    ($width * 7) ($width * 13) 0 $black,
    
    ($width * -10) ($width * 14) 0 $black,
    ($width * 1) ($width * 14) 0 $black,
    ($width * 2) ($width * 14) 0 $black,
    ($width * 3) ($width * 14) 0 $black,
    ($width * 4) ($width * 14) 0 $white,
    ($width * 5) ($width * 14) 0 $black,
    ($width * 6) ($width * 14) 0 $white,
    ($width * 7) ($width * 14) 0 $black,
    ($width * 8) ($width * 14) 0 $black,

    ($width * 1) ($width * 15) 0 $black,
    ($width * 2) ($width * 15) 0 $black,
    ($width * 3) ($width * 15) 0 $black,
    ($width * 4) ($width * 15) 0 $white,
    ($width * 5) ($width * 15) 0 $black,
    ($width * 6) ($width * 15) 0 $white,
    ($width * 7) ($width * 15) 0 $black,
    ($width * 8) ($width * 15) 0 $black,

    ($width * 2) ($width * 16) 0 $black,
    ($width * 3) ($width * 16) 0 $black,
    ($width * 4) ($width * 16) 0 $white,
    ($width * 5) ($width * 16) 0 $black,
    ($width * 6) ($width * 16) 0 $white,
    ($width * 7) ($width * 16) 0 $black,
    ($width * 8) ($width * 16) 0 $black,

    ($width * 2) ($width * 17) 0 $black,
    ($width * 3) ($width * 17) 0 $black,
    ($width * 4) ($width * 17) 0 $grey-vl,
    ($width * 5) ($width * 17) 0 $black,
    ($width * 6) ($width * 17) 0 $white,
    ($width * 7) ($width * 17) 0 $black,
    ($width * 8) ($width * 17) 0 $black,

    ($width * 2) ($width * 18) 0 $black,
    ($width * 3) ($width * 18) 0 $black,
    ($width * 4) ($width * 18) 0 $white,
    ($width * 5) ($width * 18) 0 $black,
    ($width * 6) ($width * 18) 0 $white,
    ($width * 7) ($width * 18) 0 $black,
    ($width * 8) ($width * 18) 0 $black,

    ($width * 2) ($width * 19) 0 $black,
    ($width * 3) ($width * 19) 0 $black,
    ($width * 4) ($width * 19) 0 $grey-vl,
    ($width * 5) ($width * 19) 0 $black,
    ($width * 6) ($width * 19) 0 $white,
    ($width * 7) ($width * 19) 0 $black,
    ($width * 8) ($width * 19) 0 $black,
    ($width * 9) ($width * 19) 0 $black,

    ($width * 2) ($width * 20) 0 $black,
    ($width * 3) ($width * 20) 0 $black,
    ($width * 4) ($width * 20) 0 $grey-vl,
    ($width * 5) ($width * 20) 0 $grey-vl,
    ($width * 6) ($width * 20) 0 $white,
    ($width * 7) ($width * 20) 0 $black,
    ($width * 8) ($width * 20) 0 $black,
    ($width * 9) ($width * 20) 0 $black,

    ($width * 2) ($width * 21) 0 $black,
    ($width * 3) ($width * 21) 0 $black,
    ($width * 4) ($width * 21) 0 $black,
    ($width * 5) ($width * 21) 0 $grey-j-l,
    ($width * 6) ($width * 21) 0 $black,
    ($width * 7) ($width * 21) 0 $black,
    ($width * 8) ($width * 21) 0 $black,
    ($width * 9) ($width * 21) 0 $black,

    ($width * 2) ($width * 22) 0 $black,
    ($width * 3) ($width * 22) 0 $black,
    ($width * 4) ($width * 22) 0 $black,
    ($width * 5) ($width * 22) 0 $black,
    ($width * 6) ($width * 22) 0 $black,
    ($width * 7) ($width * 22) 0 $black,
    ($width * 8) ($width * 22) 0 $black,
    ($width * 9) ($width * 22) 0 $black,


    ($width * 3) ($width * 23) 0 $black,
    ($width * 4) ($width * 23) 0 $black,
    ($width * 5) ($width * 23) 0 $black,
    ($width * 6) ($width * 23) 0 $black,
    ($width * 7) ($width * 23) 0 $black,
    ($width * 8) ($width * 23) 0 $black,
    ($width * 9) ($width * 23) 0 $black,


    ($width * 3) ($width * 24) 0 $black,
    ($width * 4) ($width * 24) 0 $black,
    ($width * 7) ($width * 24) 0 $black,
    ($width * 8) ($width * 24) 0 $black,
    ($width * 9) ($width * 24) 0 $black,

    ($width * 3) ($width * 25) 0 $black,
    ($width * 4) ($width * 25) 0 $black,
    ($width * 7) ($width * 25) 0 $black,
    ($width * 8) ($width * 25) 0 $black,
    ($width * 9) ($width * 25) 0 $black,

    ($width * 3) ($width * 26) 0 $black,
    ($width * 4) ($width * 26) 0 $black,
    ($width * 7) ($width * 26) 0 $black,
    ($width * 8) ($width * 26) 0 $black,
    ($width * 9) ($width * 26) 0 $black,

    ($width * 3) ($width * 27) 0 $black,
    ($width * 4) ($width * 27) 0 $black,
    ($width * 7) ($width * 27) 0 $black,
    ($width * 8) ($width * 27) 0 $black,
    ($width * 9) ($width * 27) 0 $skin-j-dark,

    ($width * 3) ($width * 28) 0 $black,
    ($width * 4) ($width * 28) 0 $black,
    ($width * 7) ($width * 28) 0 $black,
    ($width * 8) ($width * 28) 0 $black,
    ($width * 9) ($width * 28) 0 $skin-j-dark,

    ($width * 3) ($width * 29) 0 $black,
    ($width * 4) ($width * 29) 0 $black,
    ($width * 7) ($width * 29) 0 $black,
    ($width * 8) ($width * 29) 0 $black,

    ($width * 3) ($width * 30) 0 $black,
    ($width * 4) ($width * 30) 0 $black,
    ($width * 7) ($width * 30) 0 $black,
    ($width * 8) ($width * 30) 0 $black,

    ($width * 4) ($width * 31) 0 $black,
    ($width * 7) ($width * 31) 0 $black,
    ($width * 8) ($width * 31) 0 $black,

    ($width * 4) ($width * 32) 0 $black,
    ($width * 7) ($width * 32) 0 $black,

    ($width * 4) ($width * 33) 0 $black,
    ($width * 7) ($width * 33) 0 $black,

    ($width * 4) ($width * 34) 0 $black,
    ($width * 7) ($width * 34) 0 $black,

    ($width * 4) ($width * 35) 0 $black,
    ($width * 7) ($width * 35) 0 $black,

    ($width * 4) ($width * 36) 0 $black,
    ($width * 7) ($width * 36) 0 $black,

    ($width * 4) ($width * 37) 0 $black,
    ($width * 7) ($width * 37) 0 $black,

    ($width * 4) ($width * 38) 0 $black,
    ($width * 7) ($width * 38) 0 $black,

    ($width * 4) ($width * 39) 0 $black,
    ($width * 7) ($width * 39) 0 $black,

    ($width * 1) ($width * 40) 0 $shadow,
    ($width * 2) ($width * 40) 0 $shadow,
    ($width * 3) ($width * 40) 0 $shadow,
    ($width * 4) ($width * 40) 0 $black,
    ($width * 5) ($width * 40) 0 $shadow,
    ($width * 6) ($width * 40) 0 $shadow,
    ($width * 7) ($width * 40) 0 $black,
    ($width * 8) ($width * 40) 0 $shadow
}

@mixin vincent-1 {
  box-shadow:
    ($width * 4) ($width *4) 0 $black,
    ($width* 5) ($width * 4) 0 $grey,
    ($width * 6) ($width *4) 0 $black,
    ($width* 7) ($width * 4) 0 $grey-d,
    ($width * 8) ($width * 4) 0 $grey-l,

    ($width * 3) ($width * 5) 0 $black,
    ($width * 4) ($width * 5) 0 $skin-shadow,
    ($width * 5) ($width * 5) 0 $skin,
    ($width * 6) ($width * 5) 0 $skin,
    ($width * 7) ($width * 5) 0 $black,
    ($width * 8) ($width * 5) 0 $black,

    ($width * 4) ($width * 6) 0 $skin-shadow,
    ($width * 5) ($width * 6) 0 $skin,
    ($width * 6) ($width * 6) 0 $skin,
    ($width * 7) ($width * 6) 0 $skin,
    ($width * 8) ($width * 6) 0 $black,

    ($width * 4) ($width * 7) 0 $black,
    ($width * 5) ($width * 7) 0 $skin,
    ($width * 6) ($width * 7) 0 $black,
    ($width * 7) ($width * 7) 0 $skin,
    ($width * 8) ($width * 7) 0 $black,
    ($width * 9) ($width * 7) 0 $black,

    ($width * 4) ($width * 8) 0 $skin-shadow,
    ($width * 5) ($width * 8) 0 $skin,
    ($width * 6) ($width * 8) 0 $skin,
    ($width * 7) ($width * 8) 0 $skin,
    ($width * 8) ($width * 8) 0 $skin,

    ($width * 4) ($width * 9) 0 $skin-shadow,
    ($width * 5) ($width * 9) 0 $skin-shadow,
    ($width * 6) ($width * 9) 0 $skin,
    ($width * 7) ($width * 9) 0 $skin,
    ($width * 8) ($width * 9) 0 $black,

    ($width * 5) ($width * 10) 0 $black,
    ($width * 6) ($width * 10) 0 $skin-dark,
    ($width * 7) ($width * 10) 0 $skin-dark,
    ($width * 8) ($width * 10) 0 $black,
    ($width * 9) ($width * 10) 0 $black,

    ($width * 4) ($width * 11) 0 $black,
    ($width * 5) ($width * 11) 0 $black,
    ($width * 6) ($width * 11) 0 $skin-shadow,
    ($width * 7) ($width * 11) 0 $grey-vl,
    ($width * 8) ($width * 11) 0 $black,

    ($width * 5) ($width * 12) 0 $grey-vl,
    ($width * 6) ($width * 12) 0 $skin,
    ($width * 7) ($width * 12) 0 $grey-vl,
    ($width * 8) ($width * 12) 0 $black,

    ($width * 4) ($width * 13) 0 $black,
    ($width * 5) ($width * 13) 0 $grey-vl,
    ($width * 6) ($width * 13) 0 $black,
    ($width * 7) ($width * 13) 0 $white,
    ($width * 8) ($width * 13) 0 $black,

    ($width * 4) ($width * 14) 0 $black,
    ($width * 5) ($width * 14) 0 $grey-vl,
    ($width * 6) ($width * 14) 0 $black,
    ($width * 7) ($width * 14) 0 $white,
    ($width * 8) ($width * 14) 0 $black,

    ($width * 4) ($width * 15) 0 $black,
    ($width * 5) ($width * 15) 0 $grey-vl,
    ($width * 6) ($width * 15) 0 $black,
    ($width * 7) ($width * 15) 0 $white,
    ($width * 8) ($width * 15) 0 $black,
    ($width * 9) ($width * 15) 0 $black,

    ($width * 4) ($width * 16) 0 $black,
    ($width * 5) ($width * 16) 0 $grey-vl,
    ($width * 6) ($width * 16) 0 $black,
    ($width * 7) ($width * 16) 0 $white,
    ($width * 8) ($width * 16) 0 $black,
    ($width * 9) ($width * 16) 0 $black,

    ($width * 3) ($width * 17) 0 $black,
    ($width * 4) ($width * 17) 0 $black,
    ($width * 5) ($width * 17) 0 $white,
    ($width * 6) ($width * 17) 0 $black,
    ($width * 7) ($width * 17) 0 $white,
    ($width * 8) ($width * 17) 0 $black,
    ($width * 9) ($width * 17) 0 $black,

    ($width * 3) ($width * 18) 0 $black,
    ($width * 4) ($width * 18) 0 $black,
    ($width * 5) ($width * 18) 0 $white,
    ($width * 6) ($width * 18) 0 $black,
    ($width * 7) ($width * 18) 0 $white,
    ($width * 8) ($width * 18) 0 $black,
    ($width * 9) ($width * 18) 0 $black,

    ($width * 3) ($width * 19) 0 $black,
    ($width * 4) ($width * 19) 0 $black,
    ($width * 5) ($width * 19) 0 $white,
    ($width * 6) ($width * 19) 0 $black,
    ($width * 7) ($width * 19) 0 $white,
    ($width * 8) ($width * 19) 0 $black,
    ($width * 9) ($width * 19) 0 $black,

    ($width * 3) ($width * 20) 0 $black,
    ($width * 4) ($width * 20) 0 $black,
    ($width * 5) ($width * 20) 0 $grey-vl,
    ($width * 6) ($width * 20) 0 $black,
    ($width * 7) ($width * 20) 0 $white,
    ($width * 8) ($width * 20) 0 $black,
    ($width * 9) ($width * 20) 0 $black,

    ($width * 3) ($width * 21) 0 $black,
    ($width * 4) ($width * 21) 0 $black,
    ($width * 5) ($width * 21) 0 $grey-vl,
    ($width * 6) ($width * 21) 0 $black,
    ($width * 7) ($width * 21) 0 $grey-vl,
    ($width * 8) ($width * 21) 0 $black,
    ($width * 9) ($width * 21) 0 $black,
    ($width * 10) ($width * 21) 0 $black,

    ($width * 3) ($width * 22) 0 $black,
    ($width * 4) ($width * 22) 0 $black,
    ($width * 5) ($width * 22) 0 $black,
    ($width * 6) ($width * 22) 0 $black,
    ($width * 7) ($width * 22) 0 $black,
    ($width * 8) ($width * 22) 0 $black,
    ($width * 9) ($width * 22) 0 $black,
    ($width * 10) ($width * 22) 0 $black,

    ($width * 3) ($width * 23) 0 $black,
    ($width * 4) ($width * 23) 0 $black,
    ($width * 5) ($width * 23) 0 $black,
    ($width * 6) ($width * 23) 0 $black,
    ($width * 7) ($width * 23) 0 $black,
    ($width * 8) ($width * 23) 0 $black,
    ($width * 9) ($width * 23) 0 $black,
    ($width * 10) ($width * 23) 0 $black,

    ($width * 3) ($width * 24) 0 $black,
    ($width * 4) ($width * 24) 0 $black,
    ($width * 5) ($width * 24) 0 $black,
    ($width * 6) ($width * 24) 0 $black,
    ($width * 7) ($width * 24) 0 $black,
    ($width * 8) ($width * 24) 0 $black,
    ($width * 9) ($width * 24) 0 $black,
    ($width * 10) ($width * 24) 0 $black,

    ($width * 3) ($width * 25) 0 $black,
    ($width * 4) ($width * 25) 0 $black,
    ($width * 5) ($width * 25) 0 $black,
    ($width * 8) ($width * 25) 0 $black,
    ($width * 9) ($width * 25) 0 $black,
    ($width * 10) ($width * 25) 0 $black,

    ($width * 3) ($width * 26) 0 $black,
    ($width * 4) ($width * 26) 0 $black,
    ($width * 5) ($width * 26) 0 $black,
    ($width * 8) ($width * 26) 0 $black,
    ($width * 9) ($width * 26) 0 $black,
    ($width * 10) ($width * 26) 0 $black,

    ($width * 3) ($width * 27) 0 $black,
    ($width * 4) ($width * 27) 0 $black,
    ($width * 5) ($width * 27) 0 $black,
    ($width * 8) ($width * 27) 0 $black,
    ($width * 9) ($width * 27) 0 $black,
    ($width * 10) ($width * 27) 0 $black,

    ($width * 3) ($width * 28) 0 $skin,
    ($width * 4) ($width * 28) 0 $black,
    ($width * 5) ($width * 28) 0 $black,
    ($width * 8) ($width * 28) 0 $black,
    ($width * 9) ($width * 28) 0 $black,
    ($width * 10) ($width * 28) 0 $skin,
    
    ($width * 2) ($width * 29) 0 $gun-lg,
    ($width * 3) ($width * 29) 0 $skin,
    ($width * 4) ($width * 29) 0 $black,
    ($width * 5) ($width * 29) 0 $black,
    ($width * 8) ($width * 29) 0 $black,
    ($width * 9) ($width * 29) 0 $black,
    ($width * 10) ($width * 29) 0 $skin,

    ($width * 2) ($width * 30) 0 $gun-d,
    ($width * 3) ($width * 30) 0 $gun-lg,
    ($width * 4) ($width * 30) 0 $black,
    ($width * 5) ($width * 30) 0 $black,
    ($width * 8) ($width * 30) 0 $black,
    ($width * 9) ($width * 30) 0 $black,

    ($width * 2) ($width * 31) 0 $gun-lg,
    ($width * 5) ($width * 31) 0 $black,
    ($width * 8) ($width * 31) 0 $black,
    ($width * 9) ($width * 31) 0 $black,

    ($width * 2) ($width * 32) 0 $white,
    ($width * 5) ($width * 32) 0 $black,
    ($width * 8) ($width * 32) 0 $black,
    ($width * 9) ($width * 32) 0 $black,

    ($width * 2) ($width * 33) 0 $white,
    ($width * 5) ($width * 33) 0 $black,
    ($width * 9) ($width * 33) 0 $black,

    ($width * 5) ($width * 34) 0 $black,
    ($width * 9) ($width * 34) 0 $black,

    ($width * 5) ($width * 35) 0 $black,
    ($width * 9) ($width * 35) 0 $black,

    ($width * 5) ($width * 36) 0 $black,
    ($width * 9) ($width * 36) 0 $black,

    ($width * 5) ($width * 37) 0 $black,
    ($width * 9) ($width * 37) 0 $black,

    ($width * 5) ($width * 38) 0 $black,
    ($width * 9) ($width * 38) 0 $black,

    ($width * 5) ($width * 39) 0 $black,
    ($width * 9) ($width * 39) 0 $black,

    ($width * 5) ($width * 40) 0 $black,
    ($width * 9) ($width * 40) 0 $black,
    
    ($width * 2) ($width * 40) 0 $shadow,
    ($width * 3) ($width * 40) 0 $shadow,
    ($width * 4) ($width * 40) 0 $shadow,
    ($width * 5) ($width * 40) 0 $black,
    ($width * 6) ($width * 40) 0 $shadow,
    ($width * 7) ($width * 40) 0 $shadow,
    ($width * 8) ($width * 40) 0 $shadow,
    ($width * 9) ($width * 40) 0 $black,
    ($width * 10) ($width * 40) 0 $shadow
}

@mixin vincent-gun {
  box-shadow:
    ($width * 4) ($width *4) 0 $black,
    ($width* 5) ($width * 4) 0 $grey,
    ($width * 6) ($width *4) 0 $black,
    ($width* 7) ($width * 4) 0 $grey-d,
    ($width * 8) ($width * 4) 0 $grey-l,

    ($width * 3) ($width * 5) 0 $black,
    ($width * 4) ($width * 5) 0 $skin-shadow,
    ($width * 5) ($width * 5) 0 $skin,
    ($width * 6) ($width * 5) 0 $skin,
    ($width * 7) ($width * 5) 0 $black,
    ($width * 8) ($width * 5) 0 $black,

    ($width * 4) ($width * 6) 0 $skin-shadow,
    ($width * 5) ($width * 6) 0 $skin,
    ($width * 6) ($width * 6) 0 $skin,
    ($width * 7) ($width * 6) 0 $skin,
    ($width * 8) ($width * 6) 0 $black,

    ($width * 4) ($width * 7) 0 $black,
    ($width * 5) ($width * 7) 0 $skin,
    ($width * 6) ($width * 7) 0 $black,
    ($width * 7) ($width * 7) 0 $skin,
    ($width * 8) ($width * 7) 0 $black,
    ($width * 9) ($width * 7) 0 $black,

    ($width * 4) ($width * 8) 0 $skin-shadow,
    ($width * 5) ($width * 8) 0 $skin,
    ($width * 6) ($width * 8) 0 $skin,
    ($width * 7) ($width * 8) 0 $skin,
    ($width * 8) ($width * 8) 0 $skin,

    ($width * 4) ($width * 9) 0 $skin-shadow,
    ($width * 5) ($width * 9) 0 $skin-shadow,
    ($width * 6) ($width * 9) 0 $skin,
    ($width * 7) ($width * 9) 0 $skin,
    ($width * 8) ($width * 9) 0 $black,

    ($width * 5) ($width * 10) 0 $black,
    ($width * 6) ($width * 10) 0 $skin-dark,
    ($width * 7) ($width * 10) 0 $skin-dark,
    ($width * 8) ($width * 10) 0 $black,
    ($width * 9) ($width * 10) 0 $black,

    ($width * 4) ($width * 11) 0 $black,
    ($width * 5) ($width * 11) 0 $black,
    ($width * 6) ($width * 11) 0 $skin-shadow,
    ($width * 7) ($width * 11) 0 $grey-vl,
    ($width * 8) ($width * 11) 0 $black,

    ($width * 5) ($width * 12) 0 $grey-vl,
    ($width * 6) ($width * 12) 0 $skin,
    ($width * 7) ($width * 12) 0 $grey-vl,
    ($width * 8) ($width * 12) 0 $black,

    ($width * 4) ($width * 13) 0 $black,
    ($width * 5) ($width * 13) 0 $grey-vl,
    ($width * 6) ($width * 13) 0 $black,
    ($width * 7) ($width * 13) 0 $white,
    ($width * 8) ($width * 13) 0 $black,
    
    ($width * -13) ($width * 14) 0 $grey-vl,
    ($width * -12) ($width * 14) 0 $grey-vl,
    ($width * -11) ($width * 14) 0 $grey-vl,
    ($width * -10) ($width * 14) 0 $grey-j-l,
    ($width * -9) ($width * 14) 0 $grey-vl,
    ($width * 4) ($width * 14) 0 $black,
    ($width * 5) ($width * 14) 0 $grey-j-l,
    ($width * 6) ($width * 14) 0 $black,
    ($width * 7) ($width * 14) 0 $grey-j-l,
    ($width * 8) ($width * 14) 0 $black,
    

    ($width * -10) ($width * 15) 0 $grey-vl,
    ($width * -9) ($width * 15) 0 $skin,
    ($width * -8) ($width * 15) 0 $skin,
    ($width * -7) ($width * 15) 0 $black,
    ($width * -6) ($width * 15) 0 $black,
    ($width * -5) ($width * 15) 0 $black,
    ($width * -4) ($width * 15) 0 $black,
    ($width * -3) ($width * 15) 0 $black,
    ($width * -2) ($width * 15) 0 $black,
    ($width * -1) ($width * 15) 0 $black,
    ($width * 0) ($width * 15) 0 $black,
    ($width * 1) ($width * 15) 0 $black,
    ($width * 2) ($width * 15) 0 $black,
    ($width * 3) ($width * 15) 0 $black,
    ($width * 4) ($width * 15) 0 $black,
    ($width * 5) ($width * 15) 0 $grey-vl,
    ($width * 6) ($width * 15) 0 $black,
    ($width * 7) ($width * 15) 0 $white,
    ($width * 8) ($width * 15) 0 $black,
    ($width * 9) ($width * 15) 0 $black,
    
    ($width * -9) ($width * 16) 0 $black,
    ($width * 2) ($width * 16) 0 $black,
    ($width * 3) ($width * 16) 0 $black,
    ($width * 4) ($width * 16) 0 $black,
    ($width * 5) ($width * 16) 0 $grey-vl,
    ($width * 6) ($width * 16) 0 $black,
    ($width * 7) ($width * 16) 0 $white,
    ($width * 8) ($width * 16) 0 $black,
    ($width * 9) ($width * 16) 0 $black,

    ($width * 3) ($width * 17) 0 $black,
    ($width * 4) ($width * 17) 0 $black,
    ($width * 5) ($width * 17) 0 $white,
    ($width * 6) ($width * 17) 0 $black,
    ($width * 7) ($width * 17) 0 $white,
    ($width * 8) ($width * 17) 0 $black,
    ($width * 9) ($width * 17) 0 $black,

    ($width * 3) ($width * 18) 0 $black,
    ($width * 4) ($width * 18) 0 $black,
    ($width * 5) ($width * 18) 0 $white,
    ($width * 6) ($width * 18) 0 $black,
    ($width * 7) ($width * 18) 0 $white,
    ($width * 8) ($width * 18) 0 $black,
    ($width * 9) ($width * 18) 0 $black,

    ($width * 3) ($width * 19) 0 $black,
    ($width * 4) ($width * 19) 0 $black,
    ($width * 5) ($width * 19) 0 $white,
    ($width * 6) ($width * 19) 0 $black,
    ($width * 7) ($width * 19) 0 $white,
    ($width * 8) ($width * 19) 0 $black,
    ($width * 9) ($width * 19) 0 $black,

    ($width * 3) ($width * 20) 0 $black,
    ($width * 4) ($width * 20) 0 $black,
    ($width * 5) ($width * 20) 0 $grey-vl,
    ($width * 6) ($width * 20) 0 $black,
    ($width * 7) ($width * 20) 0 $white,
    ($width * 8) ($width * 20) 0 $black,
    ($width * 9) ($width * 20) 0 $black,

    ($width * 3) ($width * 21) 0 $black,
    ($width * 4) ($width * 21) 0 $black,
    ($width * 5) ($width * 21) 0 $grey-vl,
    ($width * 6) ($width * 21) 0 $black,
    ($width * 7) ($width * 21) 0 $grey-vl,
    ($width * 8) ($width * 21) 0 $black,
    ($width * 9) ($width * 21) 0 $black,
    ($width * 10) ($width * 21) 0 $black,

    ($width * 3) ($width * 22) 0 $black,
    ($width * 4) ($width * 22) 0 $black,
    ($width * 5) ($width * 22) 0 $black,
    ($width * 6) ($width * 22) 0 $black,
    ($width * 7) ($width * 22) 0 $black,
    ($width * 8) ($width * 22) 0 $black,
    ($width * 9) ($width * 22) 0 $black,
    ($width * 10) ($width * 22) 0 $black,

    ($width * 3) ($width * 23) 0 $black,
    ($width * 4) ($width * 23) 0 $black,
    ($width * 5) ($width * 23) 0 $black,
    ($width * 6) ($width * 23) 0 $black,
    ($width * 7) ($width * 23) 0 $black,
    ($width * 8) ($width * 23) 0 $black,
    ($width * 9) ($width * 23) 0 $black,
    ($width * 10) ($width * 23) 0 $black,

    ($width * 3) ($width * 24) 0 $black,
    ($width * 4) ($width * 24) 0 $black,
    ($width * 5) ($width * 24) 0 $black,
    ($width * 6) ($width * 24) 0 $black,
    ($width * 7) ($width * 24) 0 $black,
    ($width * 8) ($width * 24) 0 $black,
    ($width * 9) ($width * 24) 0 $black,
    ($width * 10) ($width * 24) 0 $black,

    ($width * 3) ($width * 25) 0 $black,
    ($width * 4) ($width * 25) 0 $black,
    ($width * 5) ($width * 25) 0 $black,
    ($width * 8) ($width * 25) 0 $black,
    ($width * 9) ($width * 25) 0 $black,
    ($width * 10) ($width * 25) 0 $black,

    ($width * 4) ($width * 26) 0 $black,
    ($width * 5) ($width * 26) 0 $black,
    ($width * 8) ($width * 26) 0 $black,
    ($width * 9) ($width * 26) 0 $black,
    ($width * 10) ($width * 26) 0 $black,

    ($width * 4) ($width * 27) 0 $black,
    ($width * 5) ($width * 27) 0 $black,
    ($width * 8) ($width * 27) 0 $black,
    ($width * 9) ($width * 27) 0 $black,
    ($width * 10) ($width * 27) 0 $black,

    ($width * 4) ($width * 28) 0 $black,
    ($width * 5) ($width * 28) 0 $black,
    ($width * 8) ($width * 28) 0 $black,
    ($width * 9) ($width * 28) 0 $black,
    ($width * 10) ($width * 28) 0 $skin,

    ($width * 4) ($width * 29) 0 $black,
    ($width * 5) ($width * 29) 0 $black,
    ($width * 8) ($width * 29) 0 $black,
    ($width * 9) ($width * 29) 0 $black,
    ($width * 10) ($width * 29) 0 $skin,

    ($width * 4) ($width * 30) 0 $black,
    ($width * 5) ($width * 30) 0 $black,
    ($width * 8) ($width * 30) 0 $black,
    ($width * 9) ($width * 30) 0 $black,

    ($width * 5) ($width * 31) 0 $black,
    ($width * 8) ($width * 31) 0 $black,
    ($width * 9) ($width * 31) 0 $black,

    ($width * 5) ($width * 32) 0 $black,
    ($width * 8) ($width * 32) 0 $black,
    ($width * 9) ($width * 32) 0 $black,

    ($width * 5) ($width * 33) 0 $black,
    ($width * 9) ($width * 33) 0 $black,

    ($width * 5) ($width * 34) 0 $black,
    ($width * 9) ($width * 34) 0 $black,

    ($width * 5) ($width * 35) 0 $black,
    ($width * 9) ($width * 35) 0 $black,

    ($width * 5) ($width * 36) 0 $black,
    ($width * 9) ($width * 36) 0 $black,

    ($width * 5) ($width * 37) 0 $black,
    ($width * 9) ($width * 37) 0 $black,

    ($width * 5) ($width * 38) 0 $black,
    ($width * 9) ($width * 38) 0 $black,

    ($width * 5) ($width * 39) 0 $black,
    ($width * 9) ($width * 39) 0 $black,

    ($width * 5) ($width * 40) 0 $black,
    ($width * 9) ($width * 40) 0 $black,
    
    ($width * 2) ($width * 40) 0 $shadow,
    ($width * 3) ($width * 40) 0 $shadow,
    ($width * 4) ($width * 40) 0 $shadow,
    ($width * 5) ($width * 40) 0 $black,
    ($width * 6) ($width * 40) 0 $shadow,
    ($width * 7) ($width * 40) 0 $shadow,
    ($width * 8) ($width * 40) 0 $shadow,
    ($width * 9) ($width * 40) 0 $black,
    ($width * 10) ($width * 40) 0 $shadow
}

@mixin vincent-fire {
  box-shadow:
    ($width * 4) ($width *4) 0 $black,
    ($width* 5) ($width * 4) 0 $grey,
    ($width * 6) ($width *4) 0 $black,
    ($width* 7) ($width * 4) 0 $grey-d,
    ($width * 8) ($width * 4) 0 $grey-l,

    ($width * 3) ($width * 5) 0 $black,
    ($width * 4) ($width * 5) 0 $skin-shadow,
    ($width * 5) ($width * 5) 0 $skin,
    ($width * 6) ($width * 5) 0 $skin,
    ($width * 7) ($width * 5) 0 $black,
    ($width * 8) ($width * 5) 0 $black,

    ($width * 4) ($width * 6) 0 $skin-shadow,
    ($width * 5) ($width * 6) 0 $skin,
    ($width * 6) ($width * 6) 0 $skin,
    ($width * 7) ($width * 6) 0 $skin,
    ($width * 8) ($width * 6) 0 $black,

    ($width * 4) ($width * 7) 0 $black,
    ($width * 5) ($width * 7) 0 $skin,
    ($width * 6) ($width * 7) 0 $black,
    ($width * 7) ($width * 7) 0 $skin,
    ($width * 8) ($width * 7) 0 $black,
    ($width * 9) ($width * 7) 0 $black,

    ($width * 4) ($width * 8) 0 $skin-shadow,
    ($width * 5) ($width * 8) 0 $skin,
    ($width * 6) ($width * 8) 0 $skin,
    ($width * 7) ($width * 8) 0 $skin,
    ($width * 8) ($width * 8) 0 $skin,

    ($width * 4) ($width * 9) 0 $skin-shadow,
    ($width * 5) ($width * 9) 0 $skin-shadow,
    ($width * 6) ($width * 9) 0 $skin,
    ($width * 7) ($width * 9) 0 $skin,
    ($width * 8) ($width * 9) 0 $black,

    ($width * 5) ($width * 10) 0 $black,
    ($width * 6) ($width * 10) 0 $skin-dark,
    ($width * 7) ($width * 10) 0 $skin-dark,
    ($width * 8) ($width * 10) 0 $black,
    ($width * 9) ($width * 10) 0 $black,

    ($width * 4) ($width * 11) 0 $black,
    ($width * 5) ($width * 11) 0 $black,
    ($width * 6) ($width * 11) 0 $skin-shadow,
    ($width * 7) ($width * 11) 0 $grey-vl,
    ($width * 8) ($width * 11) 0 $black,

    ($width * 5) ($width * 12) 0 $grey-vl,
    ($width * 6) ($width * 12) 0 $skin,
    ($width * 7) ($width * 12) 0 $grey-vl,
    ($width * 8) ($width * 12) 0 $black,
    
    ($width * -16) ($width * 13) 0 $white,
    ($width * 4) ($width * 13) 0 $black,
    ($width * 5) ($width * 13) 0 $grey-vl,
    ($width * 6) ($width * 13) 0 $black,
    ($width * 7) ($width * 13) 0 $white,
    ($width * 8) ($width * 13) 0 $black,
    
    ($width * -15) ($width * 14) 0 $white,
    ($width * -13) ($width * 14) 0 $grey-vl,
    ($width * -12) ($width * 14) 0 $grey-vl,
    ($width * -11) ($width * 14) 0 $grey-vl,
    ($width * -10) ($width * 14) 0 $grey-j-l,
    ($width * -9) ($width * 14) 0 $grey-vl,
    ($width * 4) ($width * 14) 0 $black,
    ($width * 5) ($width * 14) 0 $grey-j-l,
    ($width * 6) ($width * 14) 0 $black,
    ($width * 7) ($width * 14) 0 $grey-j-l,
    ($width * 8) ($width * 14) 0 $black,
    
    ($width * -16) ($width * 15) 0 $white,
    ($width * -10) ($width * 15) 0 $grey-vl,
    ($width * -9) ($width * 15) 0 $skin,
    ($width * -8) ($width * 15) 0 $skin,
    ($width * -7) ($width * 15) 0 $black,
    ($width * -6) ($width * 15) 0 $black,
    ($width * -5) ($width * 15) 0 $black,
    ($width * -4) ($width * 15) 0 $black,
    ($width * -3) ($width * 15) 0 $black,
    ($width * -2) ($width * 15) 0 $black,
    ($width * -1) ($width * 15) 0 $black,
    ($width * 0) ($width * 15) 0 $black,
    ($width * 1) ($width * 15) 0 $black,
    ($width * 2) ($width * 15) 0 $black,
    ($width * 3) ($width * 15) 0 $black,
    ($width * 4) ($width * 15) 0 $black,
    ($width * 5) ($width * 15) 0 $grey-vl,
    ($width * 6) ($width * 15) 0 $black,
    ($width * 7) ($width * 15) 0 $white,
    ($width * 8) ($width * 15) 0 $black,
    ($width * 9) ($width * 15) 0 $black,
    
    ($width * -9) ($width * 16) 0 $black,
    ($width * 2) ($width * 16) 0 $black,
    ($width * 3) ($width * 16) 0 $black,
    ($width * 4) ($width * 16) 0 $black,
    ($width * 5) ($width * 16) 0 $grey-vl,
    ($width * 6) ($width * 16) 0 $black,
    ($width * 7) ($width * 16) 0 $white,
    ($width * 8) ($width * 16) 0 $black,
    ($width * 9) ($width * 16) 0 $black,

    ($width * 3) ($width * 17) 0 $black,
    ($width * 4) ($width * 17) 0 $black,
    ($width * 5) ($width * 17) 0 $white,
    ($width * 6) ($width * 17) 0 $black,
    ($width * 7) ($width * 17) 0 $white,
    ($width * 8) ($width * 17) 0 $black,
    ($width * 9) ($width * 17) 0 $black,

    ($width * 3) ($width * 18) 0 $black,
    ($width * 4) ($width * 18) 0 $black,
    ($width * 5) ($width * 18) 0 $white,
    ($width * 6) ($width * 18) 0 $black,
    ($width * 7) ($width * 18) 0 $white,
    ($width * 8) ($width * 18) 0 $black,
    ($width * 9) ($width * 18) 0 $black,

    ($width * 3) ($width * 19) 0 $black,
    ($width * 4) ($width * 19) 0 $black,
    ($width * 5) ($width * 19) 0 $white,
    ($width * 6) ($width * 19) 0 $black,
    ($width * 7) ($width * 19) 0 $white,
    ($width * 8) ($width * 19) 0 $black,
    ($width * 9) ($width * 19) 0 $black,

    ($width * 3) ($width * 20) 0 $black,
    ($width * 4) ($width * 20) 0 $black,
    ($width * 5) ($width * 20) 0 $grey-vl,
    ($width * 6) ($width * 20) 0 $black,
    ($width * 7) ($width * 20) 0 $white,
    ($width * 8) ($width * 20) 0 $black,
    ($width * 9) ($width * 20) 0 $black,

    ($width * 3) ($width * 21) 0 $black,
    ($width * 4) ($width * 21) 0 $black,
    ($width * 5) ($width * 21) 0 $grey-vl,
    ($width * 6) ($width * 21) 0 $black,
    ($width * 7) ($width * 21) 0 $grey-vl,
    ($width * 8) ($width * 21) 0 $black,
    ($width * 9) ($width * 21) 0 $black,
    ($width * 10) ($width * 21) 0 $black,

    ($width * 3) ($width * 22) 0 $black,
    ($width * 4) ($width * 22) 0 $black,
    ($width * 5) ($width * 22) 0 $black,
    ($width * 6) ($width * 22) 0 $black,
    ($width * 7) ($width * 22) 0 $black,
    ($width * 8) ($width * 22) 0 $black,
    ($width * 9) ($width * 22) 0 $black,
    ($width * 10) ($width * 22) 0 $black,

    ($width * 3) ($width * 23) 0 $black,
    ($width * 4) ($width * 23) 0 $black,
    ($width * 5) ($width * 23) 0 $black,
    ($width * 6) ($width * 23) 0 $black,
    ($width * 7) ($width * 23) 0 $black,
    ($width * 8) ($width * 23) 0 $black,
    ($width * 9) ($width * 23) 0 $black,
    ($width * 10) ($width * 23) 0 $black,

    ($width * 3) ($width * 24) 0 $black,
    ($width * 4) ($width * 24) 0 $black,
    ($width * 5) ($width * 24) 0 $black,
    ($width * 6) ($width * 24) 0 $black,
    ($width * 7) ($width * 24) 0 $black,
    ($width * 8) ($width * 24) 0 $black,
    ($width * 9) ($width * 24) 0 $black,
    ($width * 10) ($width * 24) 0 $black,

    ($width * 3) ($width * 25) 0 $black,
    ($width * 4) ($width * 25) 0 $black,
    ($width * 5) ($width * 25) 0 $black,
    ($width * 8) ($width * 25) 0 $black,
    ($width * 9) ($width * 25) 0 $black,
    ($width * 10) ($width * 25) 0 $black,

    ($width * 4) ($width * 26) 0 $black,
    ($width * 5) ($width * 26) 0 $black,
    ($width * 8) ($width * 26) 0 $black,
    ($width * 9) ($width * 26) 0 $black,
    ($width * 10) ($width * 26) 0 $black,

    ($width * 4) ($width * 27) 0 $black,
    ($width * 5) ($width * 27) 0 $black,
    ($width * 8) ($width * 27) 0 $black,
    ($width * 9) ($width * 27) 0 $black,
    ($width * 10) ($width * 27) 0 $black,

    ($width * 4) ($width * 28) 0 $black,
    ($width * 5) ($width * 28) 0 $black,
    ($width * 8) ($width * 28) 0 $black,
    ($width * 9) ($width * 28) 0 $black,
    ($width * 10) ($width * 28) 0 $skin,

    ($width * 4) ($width * 29) 0 $black,
    ($width * 5) ($width * 29) 0 $black,
    ($width * 8) ($width * 29) 0 $black,
    ($width * 9) ($width * 29) 0 $black,
    ($width * 10) ($width * 29) 0 $skin,

    ($width * 4) ($width * 30) 0 $black,
    ($width * 5) ($width * 30) 0 $black,
    ($width * 8) ($width * 30) 0 $black,
    ($width * 9) ($width * 30) 0 $black,

    ($width * 5) ($width * 31) 0 $black,
    ($width * 8) ($width * 31) 0 $black,
    ($width * 9) ($width * 31) 0 $black,

    ($width * 5) ($width * 32) 0 $black,
    ($width * 8) ($width * 32) 0 $black,
    ($width * 9) ($width * 32) 0 $black,

    ($width * 5) ($width * 33) 0 $black,
    ($width * 9) ($width * 33) 0 $black,

    ($width * 5) ($width * 34) 0 $black,
    ($width * 9) ($width * 34) 0 $black,

    ($width * 5) ($width * 35) 0 $black,
    ($width * 9) ($width * 35) 0 $black,

    ($width * 5) ($width * 36) 0 $black,
    ($width * 9) ($width * 36) 0 $black,

    ($width * 5) ($width * 37) 0 $black,
    ($width * 9) ($width * 37) 0 $black,

    ($width * 5) ($width * 38) 0 $black,
    ($width * 9) ($width * 38) 0 $black,

    ($width * 5) ($width * 39) 0 $black,
    ($width * 9) ($width * 39) 0 $black,

    ($width * 5) ($width * 40) 0 $black,
    ($width * 9) ($width * 40) 0 $black,
    
    ($width * 2) ($width * 40) 0 $shadow,
    ($width * 3) ($width * 40) 0 $shadow,
    ($width * 4) ($width * 40) 0 $shadow,
    ($width * 5) ($width * 40) 0 $black,
    ($width * 6) ($width * 40) 0 $shadow,
    ($width * 7) ($width * 40) 0 $shadow,
    ($width * 8) ($width * 40) 0 $shadow,
    ($width * 9) ($width * 40) 0 $black,
    ($width * 10) ($width * 40) 0 $shadow
}
.pulp-fiction {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background: #676766;
    height: 40 * $width;
    width: 20 * $width;
}
.vincent {
    display: inline-block;
    position: relative;
    width: $width;
    height: $width;
}
.pf-vincent-1 {
    @include vincent-1;
}
.pf-vincent-gun {
    @include vincent-gun;
}
.pf-vincent-fire {
    @include vincent-fire;
}
.jules {
    display: inline-block;
    position: relative;
    left: $width * 9;
    width: $width;
    height: $width;
}
.pf-jules-1 {
    @include jules-1;
}
.pf-jules-gun {
    @include jules-gun;
}
.pf-jules-fire {
    @include jules-fire;
}

```

```js
function shoot() {
 setTimeout(function(){
  $('.vincent').addClass( "pf-vincent-gun");
  $('.jules').addClass( "pf-jules-gun");

    // You ever read the Bible?
  setTimeout(bullet, 500);
  setTimeout(bullet, 1500);

  setTimeout(function(){ 
   $('.vincent').removeClass( "pf-vincent-gun");
   $('.jules').removeClass( "pf-jules-gun");

   shoot();

  }, 3000);
 }, 1000);
 }

function bullet(){
 $('.vincent').addClass( "pf-vincent-fire");
 $('.jules').addClass( "pf-jules-fire");

 setTimeout(function(){ 
  $('.vincent').removeClass( "pf-vincent-fire");
  $('.jules').removeClass( "pf-jules-fire");
 }, 500);
}
shoot();
```

## CLASSIC PIXEL ART FOLDER

```html
<div class="container">
 <div class="pixelart-to-css-static static"></div>
 <div class="pixelart-to-css-static static2"></div>
 <div class="pixelart-to-css-static2 static3"></div>
 <div class="pixelart-to-css-static2 static4"></div>
 <div class="pixelart-to-css-static2 static5"></div>
 <div class="pixelart-to-css-static3 static6"></div>
 <div class="pixelart-to-css-static3 static7"></div>

 <p class="system-text">System Error</p>
 <div id="background" class="pixelart-to-css"></div>
 <div class="pixelart-to-css-error error"></div>
</div>
<div class="folders">
 <div class="pixelart-to-css-folder folder"></div>
 <div class="pixelart-to-css-folder folder2">
 </div>
 <div class="pixelart-to-css-text text"></div>
 <div class="pixelart-to-css-log log"></div>
</div>
<div class="bg"></div>
```

```css
@import url("<https://fonts.googleapis.com/css2?family=VT323&display=swap>");
:root {
 --pearly-purple: #bc63a3ff;
 --royal-purple: #805b9eff;
 --onyx: #303539ff;
 --english-violet: #494158ff;
}
html {
 height: 100%;
 padding: 0;
}
body {
 margin: 0;
 padding: 0;
 height: 100%;
 background: #edf2fb;
 font-family: "VT323", monospace;
}
.system-text {
 font-size: 24px;
 color: #fbfeffff;
 letter-spacing: 1px;
 position: absolute;
 z-index: 2;
 transform: translateX(400px) translateY(50px);
 animation: horizontalStatic 0.5s infinite;
}
.static {
 position: absolute;
 z-index: 2;
 transform: scale(0.6) translateX(200px) translateY(490px);
}
.static2 {
 position: absolute;
 z-index: 2;
 transform: scale(0.6) translateX(420px) translateY(85px);
}

.static {
 animation: horizontalStatic 1s infinite;
}
.static2 {
 animation: verticalStatic 0.8s infinite;
}
.static3,
.static4,
.static5 {
 position: absolute;
 z-index: 2;
 animation: verticalStatic 0.8s infinite;
}
.static6,
.static7 {
 position: absolute;
 z-index: 2;
 animation: horizontalStatic 0.8s infinite;
}
.static6 {
 transform: scale(0.6) translateX(-90px) translateY(790px);
}
.static7 {
 transform: scale(0.6) translateX(380px) translateY(290px);
}

.static3 {
 transform: scale(0.6) translateX(1020px) translateY(385px);
}
.static4 {
 transform: scale(0.6) translateX(980px) translateY(295px);
}
.static5 {
 transform: scale(0.6) translateX(10px) translateY(-70px);
}
.pixelart-to-css-static3 {
 box-shadow: 10px 10px 0 0 rgba(255, 255, 255, 1),
  30px 10px 0 0 rgba(255, 255, 255, 1), 50px 10px 0 0 rgba(255, 255, 255, 1),
  70px 10px 0 0 rgba(255, 255, 255, 1), 90px 10px 0 0 rgba(255, 255, 255, 1),
  110px 10px 0 0 rgba(255, 255, 255, 1), 150px 10px 0 0 rgba(255, 255, 255, 1),
  190px 10px 0 0 rgba(255, 255, 255, 1), 230px 10px 0 0 rgba(255, 255, 255, 1),
  20px 20px 0 0 rgba(255, 255, 255, 1), 40px 20px 0 0 rgba(255, 255, 255, 1),
  60px 20px 0 0 rgba(255, 255, 255, 1), 80px 20px 0 0 rgba(255, 255, 255, 1),
  100px 20px 0 0 rgba(255, 255, 255, 1), 10px 30px 0 0 rgba(255, 255, 255, 1),
  30px 30px 0 0 rgba(255, 255, 255, 1), 50px 30px 0 0 rgba(255, 255, 255, 1),
  70px 30px 0 0 rgba(255, 255, 255, 1), 90px 30px 0 0 rgba(255, 255, 255, 1),
  110px 30px 0 0 rgba(255, 255, 255, 1), 130px 30px 0 0 rgba(255, 255, 255, 1),
  170px 30px 0 0 rgba(255, 255, 255, 1), 210px 30px 0 0 rgba(255, 255, 255, 1);
 height: 10px;
 width: 10px;
}
.pixelart-to-css-static {
 box-shadow: 30px 10px 0 0 rgba(255, 255, 255, 1),
  50px 10px 0 0 rgba(255, 255, 255, 1), 70px 10px 0 0 rgba(255, 255, 255, 1),
  90px 10px 0 0 rgba(255, 255, 255, 1), 110px 10px 0 0 rgba(255, 255, 255, 1),
  130px 10px 0 0 rgba(255, 255, 255, 1), 80px 30px 0 0 rgba(255, 255, 255, 1),
  100px 30px 0 0 rgba(255, 255, 255, 1), 120px 30px 0 0 rgba(255, 255, 255, 1),
  140px 30px 0 0 rgba(255, 255, 255, 1), 160px 30px 0 0 rgba(255, 255, 255, 1),
  180px 30px 0 0 rgba(255, 255, 255, 1), 200px 30px 0 0 rgba(255, 255, 255, 1),
  220px 30px 0 0 rgba(255, 255, 255, 1), 240px 30px 0 0 rgba(255, 255, 255, 1),
  260px 30px 0 0 rgba(255, 255, 255, 1), 10px 50px 0 0 rgba(255, 255, 255, 1),
  30px 50px 0 0 rgba(255, 255, 255, 1), 50px 50px 0 0 rgba(255, 255, 255, 1),
  70px 50px 0 0 rgba(255, 255, 255, 1), 90px 50px 0 0 rgba(255, 255, 255, 1),
  110px 50px 0 0 rgba(255, 255, 255, 1), 130px 50px 0 0 rgba(255, 255, 255, 1),
  150px 50px 0 0 rgba(255, 255, 255, 1), 170px 50px 0 0 rgba(255, 255, 255, 1),
  190px 50px 0 0 rgba(255, 255, 255, 1), 210px 50px 0 0 rgba(255, 255, 255, 1),
  120px 70px 0 0 rgba(255, 255, 255, 1), 140px 70px 0 0 rgba(255, 255, 255, 1),
  160px 70px 0 0 rgba(255, 255, 255, 1), 180px 70px 0 0 rgba(255, 255, 255, 1),
  200px 70px 0 0 rgba(255, 255, 255, 1), 220px 70px 0 0 rgba(255, 255, 255, 1),
  240px 70px 0 0 rgba(255, 255, 255, 1), 260px 70px 0 0 rgba(255, 255, 255, 1),
  280px 70px 0 0 rgba(255, 255, 255, 1), 300px 70px 0 0 rgba(255, 255, 255, 1),
  320px 70px 0 0 rgba(255, 255, 255, 1);
 height: 10px;
 width: 10px;
}

.pixelart-to-css-error {
 box-shadow: 10px 10px 0 0 rgba(28, 32, 34, 1),
  20px 10px 0 0 rgba(219, 222, 232, 1), 30px 10px 0 0 rgba(111, 114, 121, 1),
  40px 10px 0 0 rgba(28, 32, 34, 1), 50px 10px 0 0 rgba(48, 53, 56, 1),
  60px 10px 0 0 rgba(48, 53, 56, 1), 70px 10px 0 0 rgba(48, 53, 56, 1),
  80px 10px 0 0 rgba(48, 53, 56, 1), 90px 10px 0 0 rgba(48, 53, 56, 1),
  100px 10px 0 0 rgba(48, 53, 56, 1), 110px 10px 0 0 rgba(48, 53, 56, 1),
  120px 10px 0 0 rgba(48, 53, 56, 1), 130px 10px 0 0 rgba(48, 53, 56, 1),
  140px 10px 0 0 rgba(48, 53, 56, 1), 150px 10px 0 0 rgba(48, 53, 56, 1),
  160px 10px 0 0 rgba(48, 53, 56, 1), 170px 10px 0 0 rgba(48, 53, 56, 1),
  180px 10px 0 0 rgba(48, 53, 56, 1), 190px 10px 0 0 rgba(48, 53, 56, 1),
  200px 10px 0 0 rgba(48, 53, 56, 1), 210px 10px 0 0 rgba(48, 53, 56, 1),
  220px 10px 0 0 rgba(48, 53, 56, 1), 230px 10px 0 0 rgba(48, 53, 56, 1),
  240px 10px 0 0 rgba(48, 53, 56, 1), 250px 10px 0 0 rgba(48, 53, 56, 1),
  260px 10px 0 0 rgba(48, 53, 56, 1), 270px 10px 0 0 rgba(48, 53, 56, 1),
  280px 10px 0 0 rgba(48, 53, 56, 1), 290px 10px 0 0 rgba(48, 53, 56, 1),
  300px 10px 0 0 rgba(48, 53, 56, 1), 310px 10px 0 0 rgba(48, 53, 56, 1),
  320px 10px 0 0 rgba(48, 53, 56, 1), 330px 10px 0 0 rgba(48, 53, 56, 1),
  340px 10px 0 0 rgba(48, 53, 56, 1), 350px 10px 0 0 rgba(48, 53, 56, 1),
  360px 10px 0 0 rgba(48, 53, 56, 1), 370px 10px 0 0 rgba(48, 53, 56, 1),
  380px 10px 0 0 rgba(48, 53, 56, 1), 390px 10px 0 0 rgba(48, 53, 56, 1),
  400px 10px 0 0 rgba(48, 53, 56, 1), 410px 10px 0 0 rgba(48, 53, 56, 1),
  420px 10px 0 0 rgba(48, 53, 56, 1), 430px 10px 0 0 rgba(48, 53, 56, 1),
  440px 10px 0 0 rgba(48, 53, 56, 1), 450px 10px 0 0 rgba(48, 53, 56, 1),
  460px 10px 0 0 rgba(48, 53, 56, 1), 470px 10px 0 0 rgba(48, 53, 56, 1),
  480px 10px 0 0 rgba(48, 53, 56, 1), 490px 10px 0 0 rgba(48, 53, 56, 1),
  500px 10px 0 0 rgba(48, 53, 56, 1), 510px 10px 0 0 rgba(48, 53, 56, 1),
  520px 10px 0 0 rgba(48, 53, 56, 1), 530px 10px 0 0 rgba(48, 53, 56, 1),
  540px 10px 0 0 rgba(48, 53, 56, 1), 550px 10px 0 0 rgba(48, 53, 56, 1),
  560px 10px 0 0 rgba(48, 53, 56, 1), 570px 10px 0 0 rgba(48, 53, 56, 1),
  580px 10px 0 0 rgba(48, 53, 56, 1), 590px 10px 0 0 rgba(48, 53, 56, 1),
  600px 10px 0 0 rgba(48, 53, 56, 1), 610px 10px 0 0 rgba(48, 53, 56, 1),
  620px 10px 0 0 rgba(48, 53, 56, 1), 630px 10px 0 0 rgba(48, 53, 56, 1),
  640px 10px 0 0 rgba(48, 53, 56, 1), 650px 10px 0 0 rgba(48, 53, 56, 1),
  660px 10px 0 0 rgba(48, 53, 56, 1), 670px 10px 0 0 rgba(48, 53, 56, 1),
  680px 10px 0 0 rgba(48, 53, 56, 1), 690px 10px 0 0 rgba(48, 53, 56, 1),
  700px 10px 0 0 rgba(48, 53, 56, 1), 710px 10px 0 0 rgba(48, 53, 56, 1),
  720px 10px 0 0 rgba(48, 53, 56, 1), 730px 10px 0 0 rgba(48, 53, 56, 1),
  740px 10px 0 0 rgba(48, 53, 56, 1), 750px 10px 0 0 rgba(48, 53, 56, 1),
  760px 10px 0 0 rgba(48, 53, 56, 1), 770px 10px 0 0 rgba(48, 53, 56, 1),
  780px 10px 0 0 rgba(48, 53, 56, 1), 790px 10px 0 0 rgba(48, 53, 56, 1),
  800px 10px 0 0 rgba(48, 53, 56, 1), 810px 10px 0 0 rgba(48, 53, 56, 1),
  820px 10px 0 0 rgba(48, 53, 56, 1), 830px 10px 0 0 rgba(48, 53, 56, 1),
  840px 10px 0 0 rgba(48, 53, 56, 1), 850px 10px 0 0 rgba(48, 53, 56, 1),
  860px 10px 0 0 rgba(48, 53, 56, 1), 870px 10px 0 0 rgba(48, 53, 56, 1),
  880px 10px 0 0 rgba(48, 53, 56, 1), 890px 10px 0 0 rgba(48, 53, 56, 1),
  900px 10px 0 0 rgba(48, 53, 56, 1), 910px 10px 0 0 rgba(48, 53, 56, 1),
  920px 10px 0 0 rgba(48, 53, 56, 1), 930px 10px 0 0 rgba(48, 53, 56, 1),
  940px 10px 0 0 rgba(48, 53, 56, 1), 950px 10px 0 0 rgba(48, 53, 56, 1),
  960px 10px 0 0 rgba(48, 53, 56, 1), 970px 10px 0 0 rgba(48, 53, 56, 1),
  980px 10px 0 0 rgba(48, 53, 56, 1), 990px 10px 0 0 rgba(48, 53, 56, 1),
  1000px 10px 0 0 rgba(48, 53, 56, 1), 10px 20px 0 0 rgba(28, 32, 34, 1),
  20px 20px 0 0 rgba(219, 222, 232, 1), 30px 20px 0 0 rgba(111, 114, 121, 1),
  40px 20px 0 0 rgba(28, 32, 34, 1), 50px 20px 0 0 rgba(48, 53, 56, 1),
  60px 20px 0 0 rgba(48, 53, 56, 1), 70px 20px 0 0 rgba(48, 53, 56, 1),
  80px 20px 0 0 rgba(48, 53, 56, 1), 90px 20px 0 0 rgba(48, 53, 56, 1),
  100px 20px 0 0 rgba(48, 53, 56, 1), 110px 20px 0 0 rgba(48, 53, 56, 1),
  120px 20px 0 0 rgba(48, 53, 56, 1), 130px 20px 0 0 rgba(48, 53, 56, 1),
  140px 20px 0 0 rgba(48, 53, 56, 1), 150px 20px 0 0 rgba(48, 53, 56, 1),
  160px 20px 0 0 rgba(48, 53, 56, 1), 170px 20px 0 0 rgba(48, 53, 56, 1),
  180px 20px 0 0 rgba(48, 53, 56, 1), 190px 20px 0 0 rgba(48, 53, 56, 1),
  200px 20px 0 0 rgba(48, 53, 56, 1), 210px 20px 0 0 rgba(48, 53, 56, 1),
  220px 20px 0 0 rgba(48, 53, 56, 1), 230px 20px 0 0 rgba(48, 53, 56, 1),
  240px 20px 0 0 rgba(48, 53, 56, 1), 250px 20px 0 0 rgba(48, 53, 56, 1),
  260px 20px 0 0 rgba(48, 53, 56, 1), 270px 20px 0 0 rgba(48, 53, 56, 1),
  280px 20px 0 0 rgba(48, 53, 56, 1), 290px 20px 0 0 rgba(48, 53, 56, 1),
  300px 20px 0 0 rgba(48, 53, 56, 1), 310px 20px 0 0 rgba(48, 53, 56, 1),
  320px 20px 0 0 rgba(48, 53, 56, 1), 330px 20px 0 0 rgba(48, 53, 56, 1),
  340px 20px 0 0 rgba(48, 53, 56, 1), 350px 20px 0 0 rgba(48, 53, 56, 1),
  360px 20px 0 0 rgba(48, 53, 56, 1), 370px 20px 0 0 rgba(48, 53, 56, 1),
  380px 20px 0 0 rgba(48, 53, 56, 1), 390px 20px 0 0 rgba(48, 53, 56, 1),
  400px 20px 0 0 rgba(48, 53, 56, 1), 410px 20px 0 0 rgba(48, 53, 56, 1),
  420px 20px 0 0 rgba(48, 53, 56, 1), 430px 20px 0 0 rgba(48, 53, 56, 1),
  440px 20px 0 0 rgba(48, 53, 56, 1), 450px 20px 0 0 rgba(48, 53, 56, 1),
  460px 20px 0 0 rgba(48, 53, 56, 1), 470px 20px 0 0 rgba(48, 53, 56, 1),
  480px 20px 0 0 rgba(48, 53, 56, 1), 490px 20px 0 0 rgba(48, 53, 56, 1),
  500px 20px 0 0 rgba(48, 53, 56, 1), 510px 20px 0 0 rgba(48, 53, 56, 1),
  520px 20px 0 0 rgba(48, 53, 56, 1), 530px 20px 0 0 rgba(48, 53, 56, 1),
  540px 20px 0 0 rgba(48, 53, 56, 1), 550px 20px 0 0 rgba(48, 53, 56, 1),
  560px 20px 0 0 rgba(48, 53, 56, 1), 570px 20px 0 0 rgba(48, 53, 56, 1),
  580px 20px 0 0 rgba(48, 53, 56, 1), 590px 20px 0 0 rgba(48, 53, 56, 1),
  600px 20px 0 0 rgba(48, 53, 56, 1), 610px 20px 0 0 rgba(48, 53, 56, 1),
  620px 20px 0 0 rgba(48, 53, 56, 1), 630px 20px 0 0 rgba(48, 53, 56, 1),
  640px 20px 0 0 rgba(48, 53, 56, 1), 650px 20px 0 0 rgba(48, 53, 56, 1),
  660px 20px 0 0 rgba(48, 53, 56, 1), 670px 20px 0 0 rgba(48, 53, 56, 1),
  680px 20px 0 0 rgba(48, 53, 56, 1), 690px 20px 0 0 rgba(48, 53, 56, 1),
  700px 20px 0 0 rgba(48, 53, 56, 1), 710px 20px 0 0 rgba(48, 53, 56, 1),
  720px 20px 0 0 rgba(48, 53, 56, 1), 730px 20px 0 0 rgba(48, 53, 56, 1),
  740px 20px 0 0 rgba(48, 53, 56, 1), 750px 20px 0 0 rgba(48, 53, 56, 1),
  760px 20px 0 0 rgba(48, 53, 56, 1), 770px 20px 0 0 rgba(48, 53, 56, 1),
  780px 20px 0 0 rgba(48, 53, 56, 1), 790px 20px 0 0 rgba(48, 53, 56, 1),
  800px 20px 0 0 rgba(48, 53, 56, 1), 810px 20px 0 0 rgba(48, 53, 56, 1),
  820px 20px 0 0 rgba(48, 53, 56, 1), 830px 20px 0 0 rgba(48, 53, 56, 1),
  840px 20px 0 0 rgba(48, 53, 56, 1), 850px 20px 0 0 rgba(48, 53, 56, 1),
  860px 20px 0 0 rgba(48, 53, 56, 1), 870px 20px 0 0 rgba(48, 53, 56, 1),
  880px 20px 0 0 rgba(48, 53, 56, 1), 890px 20px 0 0 rgba(48, 53, 56, 1),
  900px 20px 0 0 rgba(48, 53, 56, 1), 910px 20px 0 0 rgba(48, 53, 56, 1),
  920px 20px 0 0 rgba(48, 53, 56, 1), 930px 20px 0 0 rgba(48, 53, 56, 1),
  940px 20px 0 0 rgba(48, 53, 56, 1), 950px 20px 0 0 rgba(48, 53, 56, 1),
  960px 20px 0 0 rgba(48, 53, 56, 1), 970px 20px 0 0 rgba(48, 53, 56, 1),
  980px 20px 0 0 rgba(48, 53, 56, 1), 990px 20px 0 0 rgba(48, 53, 56, 1),
  1000px 20px 0 0 rgba(48, 53, 56, 1), 10px 30px 0 0 rgba(28, 32, 34, 1),
  20px 30px 0 0 rgba(219, 222, 232, 1), 30px 30px 0 0 rgba(111, 114, 121, 1),
  40px 30px 0 0 rgba(28, 32, 34, 1), 50px 30px 0 0 rgba(48, 53, 56, 1),
  60px 30px 0 0 rgba(48, 53, 56, 1), 70px 30px 0 0 rgba(48, 53, 56, 1),
  80px 30px 0 0 rgba(48, 53, 56, 1), 90px 30px 0 0 rgba(48, 53, 56, 1),
  100px 30px 0 0 rgba(48, 53, 56, 1), 110px 30px 0 0 rgba(48, 53, 56, 1),
  120px 30px 0 0 rgba(48, 53, 56, 1), 130px 30px 0 0 rgba(48, 53, 56, 1),
  140px 30px 0 0 rgba(48, 53, 56, 1), 150px 30px 0 0 rgba(48, 53, 56, 1),
  160px 30px 0 0 rgba(48, 53, 56, 1), 170px 30px 0 0 rgba(48, 53, 56, 1),
  180px 30px 0 0 rgba(48, 53, 56, 1), 190px 30px 0 0 rgba(48, 53, 56, 1),
  200px 30px 0 0 rgba(48, 53, 56, 1), 210px 30px 0 0 rgba(48, 53, 56, 1),
  220px 30px 0 0 rgba(48, 53, 56, 1), 230px 30px 0 0 rgba(48, 53, 56, 1),
  240px 30px 0 0 rgba(48, 53, 56, 1), 250px 30px 0 0 rgba(48, 53, 56, 1),
  260px 30px 0 0 rgba(48, 53, 56, 1), 270px 30px 0 0 rgba(48, 53, 56, 1),
  280px 30px 0 0 rgba(48, 53, 56, 1), 290px 30px 0 0 rgba(48, 53, 56, 1),
  300px 30px 0 0 rgba(48, 53, 56, 1), 310px 30px 0 0 rgba(48, 53, 56, 1),
  320px 30px 0 0 rgba(48, 53, 56, 1), 330px 30px 0 0 rgba(48, 53, 56, 1),
  340px 30px 0 0 rgba(48, 53, 56, 1), 350px 30px 0 0 rgba(48, 53, 56, 1),
  360px 30px 0 0 rgba(48, 53, 56, 1), 370px 30px 0 0 rgba(48, 53, 56, 1),
  380px 30px 0 0 rgba(48, 53, 56, 1), 390px 30px 0 0 rgba(48, 53, 56, 1),
  400px 30px 0 0 rgba(48, 53, 56, 1), 410px 30px 0 0 rgba(48, 53, 56, 1),
  420px 30px 0 0 rgba(48, 53, 56, 1), 430px 30px 0 0 rgba(48, 53, 56, 1),
  440px 30px 0 0 rgba(48, 53, 56, 1), 450px 30px 0 0 rgba(48, 53, 56, 1),
  460px 30px 0 0 rgba(48, 53, 56, 1), 470px 30px 0 0 rgba(48, 53, 56, 1),
  480px 30px 0 0 rgba(48, 53, 56, 1), 490px 30px 0 0 rgba(48, 53, 56, 1),
  500px 30px 0 0 rgba(48, 53, 56, 1), 510px 30px 0 0 rgba(48, 53, 56, 1),
  520px 30px 0 0 rgba(48, 53, 56, 1), 530px 30px 0 0 rgba(48, 53, 56, 1),
  540px 30px 0 0 rgba(48, 53, 56, 1), 550px 30px 0 0 rgba(48, 53, 56, 1),
  560px 30px 0 0 rgba(48, 53, 56, 1), 570px 30px 0 0 rgba(48, 53, 56, 1),
  580px 30px 0 0 rgba(48, 53, 56, 1), 590px 30px 0 0 rgba(48, 53, 56, 1),
  600px 30px 0 0 rgba(48, 53, 56, 1), 610px 30px 0 0 rgba(48, 53, 56, 1),
  620px 30px 0 0 rgba(48, 53, 56, 1), 630px 30px 0 0 rgba(48, 53, 56, 1),
  640px 30px 0 0 rgba(48, 53, 56, 1), 650px 30px 0 0 rgba(48, 53, 56, 1),
  660px 30px 0 0 rgba(48, 53, 56, 1), 670px 30px 0 0 rgba(48, 53, 56, 1),
  680px 30px 0 0 rgba(48, 53, 56, 1), 690px 30px 0 0 rgba(48, 53, 56, 1),
  700px 30px 0 0 rgba(48, 53, 56, 1), 710px 30px 0 0 rgba(48, 53, 56, 1),
  720px 30px 0 0 rgba(48, 53, 56, 1), 730px 30px 0 0 rgba(48, 53, 56, 1),
  740px 30px 0 0 rgba(48, 53, 56, 1), 750px 30px 0 0 rgba(48, 53, 56, 1),
  760px 30px 0 0 rgba(48, 53, 56, 1), 770px 30px 0 0 rgba(48, 53, 56, 1),
  780px 30px 0 0 rgba(48, 53, 56, 1), 790px 30px 0 0 rgba(48, 53, 56, 1),
  800px 30px 0 0 rgba(48, 53, 56, 1), 810px 30px 0 0 rgba(48, 53, 56, 1),
  820px 30px 0 0 rgba(48, 53, 56, 1), 830px 30px 0 0 rgba(48, 53, 56, 1),
  840px 30px 0 0 rgba(48, 53, 56, 1), 850px 30px 0 0 rgba(48, 53, 56, 1),
  860px 30px 0 0 rgba(48, 53, 56, 1), 870px 30px 0 0 rgba(48, 53, 56, 1),
  880px 30px 0 0 rgba(48, 53, 56, 1), 890px 30px 0 0 rgba(48, 53, 56, 1),
  900px 30px 0 0 rgba(48, 53, 56, 1), 910px 30px 0 0 rgba(48, 53, 56, 1),
  920px 30px 0 0 rgba(48, 53, 56, 1), 930px 30px 0 0 rgba(48, 53, 56, 1),
  940px 30px 0 0 rgba(48, 53, 56, 1), 950px 30px 0 0 rgba(48, 53, 56, 1),
  960px 30px 0 0 rgba(48, 53, 56, 1), 970px 30px 0 0 rgba(48, 53, 56, 1),
  980px 30px 0 0 rgba(48, 53, 56, 1), 990px 30px 0 0 rgba(48, 53, 56, 1),
  1000px 30px 0 0 rgba(48, 53, 56, 1), 10px 40px 0 0 rgba(28, 32, 34, 1),
  20px 40px 0 0 rgba(219, 222, 232, 1), 30px 40px 0 0 rgba(111, 114, 121, 1),
  40px 40px 0 0 rgba(28, 32, 34, 1), 50px 40px 0 0 rgba(48, 53, 56, 1),
  60px 40px 0 0 rgba(48, 53, 56, 1), 70px 40px 0 0 rgba(48, 53, 56, 1),
  80px 40px 0 0 rgba(48, 53, 56, 1), 90px 40px 0 0 rgba(48, 53, 56, 1),
  100px 40px 0 0 rgba(48, 53, 56, 1), 110px 40px 0 0 rgba(48, 53, 56, 1),
  120px 40px 0 0 rgba(48, 53, 56, 1), 130px 40px 0 0 rgba(48, 53, 56, 1),
  140px 40px 0 0 rgba(48, 53, 56, 1), 150px 40px 0 0 rgba(48, 53, 56, 1),
  160px 40px 0 0 rgba(48, 53, 56, 1), 170px 40px 0 0 rgba(48, 53, 56, 1),
  180px 40px 0 0 rgba(48, 53, 56, 1), 190px 40px 0 0 rgba(48, 53, 56, 1),
  200px 40px 0 0 rgba(48, 53, 56, 1), 210px 40px 0 0 rgba(48, 53, 56, 1),
  220px 40px 0 0 rgba(48, 53, 56, 1), 230px 40px 0 0 rgba(48, 53, 56, 1),
  240px 40px 0 0 rgba(48, 53, 56, 1), 250px 40px 0 0 rgba(48, 53, 56, 1),
  260px 40px 0 0 rgba(48, 53, 56, 1), 270px 40px 0 0 rgba(48, 53, 56, 1),
  280px 40px 0 0 rgba(48, 53, 56, 1), 290px 40px 0 0 rgba(48, 53, 56, 1),
  300px 40px 0 0 rgba(48, 53, 56, 1), 310px 40px 0 0 rgba(48, 53, 56, 1),
  320px 40px 0 0 rgba(48, 53, 56, 1), 330px 40px 0 0 rgba(48, 53, 56, 1),
  340px 40px 0 0 rgba(48, 53, 56, 1), 350px 40px 0 0 rgba(48, 53, 56, 1),
  360px 40px 0 0 rgba(48, 53, 56, 1), 370px 40px 0 0 rgba(48, 53, 56, 1),
  380px 40px 0 0 rgba(48, 53, 56, 1), 390px 40px 0 0 rgba(48, 53, 56, 1),
  400px 40px 0 0 rgba(48, 53, 56, 1), 410px 40px 0 0 rgba(48, 53, 56, 1),
  420px 40px 0 0 rgba(48, 53, 56, 1), 430px 40px 0 0 rgba(48, 53, 56, 1),
  440px 40px 0 0 rgba(48, 53, 56, 1), 450px 40px 0 0 rgba(48, 53, 56, 1),
  460px 40px 0 0 rgba(48, 53, 56, 1), 470px 40px 0 0 rgba(48, 53, 56, 1),
  480px 40px 0 0 rgba(48, 53, 56, 1), 490px 40px 0 0 rgba(48, 53, 56, 1),
  500px 40px 0 0 rgba(48, 53, 56, 1), 510px 40px 0 0 rgba(48, 53, 56, 1),
  520px 40px 0 0 rgba(48, 53, 56, 1), 530px 40px 0 0 rgba(48, 53, 56, 1),
  540px 40px 0 0 rgba(48, 53, 56, 1), 550px 40px 0 0 rgba(48, 53, 56, 1),
  560px 40px 0 0 rgba(48, 53, 56, 1), 570px 40px 0 0 rgba(48, 53, 56, 1),
  580px 40px 0 0 rgba(48, 53, 56, 1), 590px 40px 0 0 rgba(48, 53, 56, 1),
  600px 40px 0 0 rgba(48, 53, 56, 1), 610px 40px 0 0 rgba(48, 53, 56, 1),
  620px 40px 0 0 rgba(48, 53, 56, 1), 630px 40px 0 0 rgba(48, 53, 56, 1),
  640px 40px 0 0 rgba(48, 53, 56, 1), 650px 40px 0 0 rgba(48, 53, 56, 1),
  660px 40px 0 0 rgba(48, 53, 56, 1), 670px 40px 0 0 rgba(48, 53, 56, 1),
  680px 40px 0 0 rgba(48, 53, 56, 1), 690px 40px 0 0 rgba(48, 53, 56, 1),
  700px 40px 0 0 rgba(48, 53, 56, 1), 710px 40px 0 0 rgba(48, 53, 56, 1),
  720px 40px 0 0 rgba(48, 53, 56, 1), 730px 40px 0 0 rgba(48, 53, 56, 1),
  740px 40px 0 0 rgba(48, 53, 56, 1), 750px 40px 0 0 rgba(48, 53, 56, 1),
  760px 40px 0 0 rgba(48, 53, 56, 1), 770px 40px 0 0 rgba(48, 53, 56, 1),
  780px 40px 0 0 rgba(48, 53, 56, 1), 790px 40px 0 0 rgba(48, 53, 56, 1),
  800px 40px 0 0 rgba(48, 53, 56, 1), 810px 40px 0 0 rgba(48, 53, 56, 1),
  820px 40px 0 0 rgba(48, 53, 56, 1), 830px 40px 0 0 rgba(48, 53, 56, 1),
  840px 40px 0 0 rgba(48, 53, 56, 1), 850px 40px 0 0 rgba(48, 53, 56, 1),
  860px 40px 0 0 rgba(48, 53, 56, 1), 870px 40px 0 0 rgba(48, 53, 56, 1),
  880px 40px 0 0 rgba(48, 53, 56, 1), 890px 40px 0 0 rgba(48, 53, 56, 1),
  900px 40px 0 0 rgba(48, 53, 56, 1), 910px 40px 0 0 rgba(48, 53, 56, 1),
  920px 40px 0 0 rgba(48, 53, 56, 1), 930px 40px 0 0 rgba(48, 53, 56, 1),
  940px 40px 0 0 rgba(48, 53, 56, 1), 950px 40px 0 0 rgba(48, 53, 56, 1),
  960px 40px 0 0 rgba(48, 53, 56, 1), 970px 40px 0 0 rgba(48, 53, 56, 1),
  980px 40px 0 0 rgba(48, 53, 56, 1), 990px 40px 0 0 rgba(48, 53, 56, 1),
  1000px 40px 0 0 rgba(48, 53, 56, 1), 10px 50px 0 0 rgba(28, 32, 34, 1),
  20px 50px 0 0 rgba(219, 222, 232, 1), 30px 50px 0 0 rgba(111, 114, 121, 1),
  40px 50px 0 0 rgba(28, 32, 34, 1), 50px 50px 0 0 rgba(48, 53, 56, 1),
  60px 50px 0 0 rgba(48, 53, 56, 1), 70px 50px 0 0 rgba(48, 53, 56, 1),
  80px 50px 0 0 rgba(48, 53, 56, 1), 90px 50px 0 0 rgba(48, 53, 56, 1),
  100px 50px 0 0 rgba(48, 53, 56, 1), 110px 50px 0 0 rgba(48, 53, 56, 1),
  120px 50px 0 0 rgba(48, 53, 56, 1), 130px 50px 0 0 rgba(48, 53, 56, 1),
  140px 50px 0 0 rgba(48, 53, 56, 1), 150px 50px 0 0 rgba(48, 53, 56, 1),
  160px 50px 0 0 rgba(48, 53, 56, 1), 170px 50px 0 0 rgba(48, 53, 56, 1),
  180px 50px 0 0 rgba(48, 53, 56, 1), 190px 50px 0 0 rgba(48, 53, 56, 1),
  200px 50px 0 0 rgba(48, 53, 56, 1), 210px 50px 0 0 rgba(48, 53, 56, 1),
  220px 50px 0 0 rgba(48, 53, 56, 1), 230px 50px 0 0 rgba(48, 53, 56, 1),
  240px 50px 0 0 rgba(48, 53, 56, 1), 250px 50px 0 0 rgba(48, 53, 56, 1),
  260px 50px 0 0 rgba(48, 53, 56, 1), 270px 50px 0 0 rgba(48, 53, 56, 1),
  280px 50px 0 0 rgba(48, 53, 56, 1), 290px 50px 0 0 rgba(48, 53, 56, 1),
  300px 50px 0 0 rgba(48, 53, 56, 1), 310px 50px 0 0 rgba(48, 53, 56, 1),
  320px 50px 0 0 rgba(48, 53, 56, 1), 330px 50px 0 0 rgba(48, 53, 56, 1),
  340px 50px 0 0 rgba(48, 53, 56, 1), 350px 50px 0 0 rgba(48, 53, 56, 1),
  360px 50px 0 0 rgba(48, 53, 56, 1), 370px 50px 0 0 rgba(48, 53, 56, 1),
  380px 50px 0 0 rgba(48, 53, 56, 1), 390px 50px 0 0 rgba(48, 53, 56, 1),
  400px 50px 0 0 rgba(48, 53, 56, 1), 410px 50px 0 0 rgba(48, 53, 56, 1),
  420px 50px 0 0 rgba(48, 53, 56, 1), 430px 50px 0 0 rgba(48, 53, 56, 1),
  440px 50px 0 0 rgba(48, 53, 56, 1), 450px 50px 0 0 rgba(48, 53, 56, 1),
  460px 50px 0 0 rgba(48, 53, 56, 1), 470px 50px 0 0 rgba(48, 53, 56, 1),
  480px 50px 0 0 rgba(48, 53, 56, 1), 490px 50px 0 0 rgba(48, 53, 56, 1),
  500px 50px 0 0 rgba(48, 53, 56, 1), 510px 50px 0 0 rgba(48, 53, 56, 1),
  520px 50px 0 0 rgba(48, 53, 56, 1), 530px 50px 0 0 rgba(48, 53, 56, 1),
  540px 50px 0 0 rgba(48, 53, 56, 1), 550px 50px 0 0 rgba(48, 53, 56, 1),
  560px 50px 0 0 rgba(48, 53, 56, 1), 570px 50px 0 0 rgba(48, 53, 56, 1),
  580px 50px 0 0 rgba(48, 53, 56, 1), 590px 50px 0 0 rgba(48, 53, 56, 1),
  600px 50px 0 0 rgba(48, 53, 56, 1), 610px 50px 0 0 rgba(48, 53, 56, 1),
  620px 50px 0 0 rgba(48, 53, 56, 1), 630px 50px 0 0 rgba(48, 53, 56, 1),
  640px 50px 0 0 rgba(48, 53, 56, 1), 650px 50px 0 0 rgba(48, 53, 56, 1),
  660px 50px 0 0 rgba(48, 53, 56, 1), 670px 50px 0 0 rgba(48, 53, 56, 1),
  680px 50px 0 0 rgba(48, 53, 56, 1), 690px 50px 0 0 rgba(48, 53, 56, 1),
  700px 50px 0 0 rgba(48, 53, 56, 1), 710px 50px 0 0 rgba(48, 53, 56, 1),
  720px 50px 0 0 rgba(48, 53, 56, 1), 730px 50px 0 0 rgba(48, 53, 56, 1),
  740px 50px 0 0 rgba(48, 53, 56, 1), 750px 50px 0 0 rgba(48, 53, 56, 1),
  760px 50px 0 0 rgba(48, 53, 56, 1), 770px 50px 0 0 rgba(48, 53, 56, 1),
  780px 50px 0 0 rgba(48, 53, 56, 1), 790px 50px 0 0 rgba(48, 53, 56, 1),
  800px 50px 0 0 rgba(48, 53, 56, 1), 810px 50px 0 0 rgba(48, 53, 56, 1),
  820px 50px 0 0 rgba(48, 53, 56, 1), 830px 50px 0 0 rgba(48, 53, 56, 1),
  840px 50px 0 0 rgba(48, 53, 56, 1), 850px 50px 0 0 rgba(48, 53, 56, 1),
  860px 50px 0 0 rgba(48, 53, 56, 1), 870px 50px 0 0 rgba(48, 53, 56, 1),
  880px 50px 0 0 rgba(48, 53, 56, 1), 890px 50px 0 0 rgba(48, 53, 56, 1),
  900px 50px 0 0 rgba(48, 53, 56, 1), 910px 50px 0 0 rgba(48, 53, 56, 1),
  920px 50px 0 0 rgba(48, 53, 56, 1), 930px 50px 0 0 rgba(48, 53, 56, 1),
  940px 50px 0 0 rgba(48, 53, 56, 1), 950px 50px 0 0 rgba(48, 53, 56, 1),
  960px 50px 0 0 rgba(48, 53, 56, 1), 970px 50px 0 0 rgba(48, 53, 56, 1),
  980px 50px 0 0 rgba(48, 53, 56, 1), 990px 50px 0 0 rgba(48, 53, 56, 1),
  1000px 50px 0 0 rgba(48, 53, 56, 1), 10px 60px 0 0 rgba(28, 32, 34, 1),
  20px 60px 0 0 rgba(219, 222, 232, 1), 30px 60px 0 0 rgba(111, 114, 121, 1),
  40px 60px 0 0 rgba(28, 32, 34, 1), 50px 60px 0 0 rgba(48, 53, 56, 1),
  60px 60px 0 0 rgba(48, 53, 56, 1), 70px 60px 0 0 rgba(48, 53, 56, 1),
  80px 60px 0 0 rgba(48, 53, 56, 1), 90px 60px 0 0 rgba(48, 53, 56, 1),
  100px 60px 0 0 rgba(48, 53, 56, 1), 110px 60px 0 0 rgba(48, 53, 56, 1),
  120px 60px 0 0 rgba(48, 53, 56, 1), 130px 60px 0 0 rgba(48, 53, 56, 1),
  140px 60px 0 0 rgba(48, 53, 56, 1), 150px 60px 0 0 rgba(48, 53, 56, 1),
  160px 60px 0 0 rgba(48, 53, 56, 1), 170px 60px 0 0 rgba(48, 53, 56, 1),
  180px 60px 0 0 rgba(48, 53, 56, 1), 190px 60px 0 0 rgba(48, 53, 56, 1),
  200px 60px 0 0 rgba(48, 53, 56, 1), 210px 60px 0 0 rgba(48, 53, 56, 1),
  220px 60px 0 0 rgba(48, 53, 56, 1), 230px 60px 0 0 rgba(48, 53, 56, 1),
  240px 60px 0 0 rgba(48, 53, 56, 1), 250px 60px 0 0 rgba(48, 53, 56, 1),
  260px 60px 0 0 rgba(48, 53, 56, 1), 270px 60px 0 0 rgba(48, 53, 56, 1),
  280px 60px 0 0 rgba(48, 53, 56, 1), 290px 60px 0 0 rgba(48, 53, 56, 1),
  300px 60px 0 0 rgba(48, 53, 56, 1), 310px 60px 0 0 rgba(48, 53, 56, 1),
  320px 60px 0 0 rgba(48, 53, 56, 1), 330px 60px 0 0 rgba(48, 53, 56, 1),
  340px 60px 0 0 rgba(48, 53, 56, 1), 350px 60px 0 0 rgba(48, 53, 56, 1),
  360px 60px 0 0 rgba(48, 53, 56, 1), 370px 60px 0 0 rgba(48, 53, 56, 1),
  380px 60px 0 0 rgba(48, 53, 56, 1), 390px 60px 0 0 rgba(48, 53, 56, 1),
  400px 60px 0 0 rgba(48, 53, 56, 1), 410px 60px 0 0 rgba(48, 53, 56, 1),
  420px 60px 0 0 rgba(48, 53, 56, 1), 430px 60px 0 0 rgba(48, 53, 56, 1),
  440px 60px 0 0 rgba(48, 53, 56, 1), 450px 60px 0 0 rgba(48, 53, 56, 1),
  460px 60px 0 0 rgba(48, 53, 56, 1), 470px 60px 0 0 rgba(48, 53, 56, 1),
  480px 60px 0 0 rgba(48, 53, 56, 1), 490px 60px 0 0 rgba(48, 53, 56, 1),
  500px 60px 0 0 rgba(48, 53, 56, 1), 510px 60px 0 0 rgba(48, 53, 56, 1),
  520px 60px 0 0 rgba(48, 53, 56, 1), 530px 60px 0 0 rgba(48, 53, 56, 1),
  540px 60px 0 0 rgba(48, 53, 56, 1), 550px 60px 0 0 rgba(48, 53, 56, 1),
  560px 60px 0 0 rgba(48, 53, 56, 1), 570px 60px 0 0 rgba(48, 53, 56, 1),
  580px 60px 0 0 rgba(48, 53, 56, 1), 590px 60px 0 0 rgba(48, 53, 56, 1),
  600px 60px 0 0 rgba(48, 53, 56, 1), 610px 60px 0 0 rgba(48, 53, 56, 1),
  620px 60px 0 0 rgba(48, 53, 56, 1), 630px 60px 0 0 rgba(48, 53, 56, 1),
  640px 60px 0 0 rgba(48, 53, 56, 1), 650px 60px 0 0 rgba(48, 53, 56, 1),
  660px 60px 0 0 rgba(48, 53, 56, 1), 670px 60px 0 0 rgba(48, 53, 56, 1),
  680px 60px 0 0 rgba(48, 53, 56, 1), 690px 60px 0 0 rgba(48, 53, 56, 1),
  700px 60px 0 0 rgba(48, 53, 56, 1), 710px 60px 0 0 rgba(48, 53, 56, 1),
  720px 60px 0 0 rgba(48, 53, 56, 1), 730px 60px 0 0 rgba(48, 53, 56, 1),
  740px 60px 0 0 rgba(48, 53, 56, 1), 750px 60px 0 0 rgba(48, 53, 56, 1),
  760px 60px 0 0 rgba(48, 53, 56, 1), 770px 60px 0 0 rgba(48, 53, 56, 1),
  780px 60px 0 0 rgba(48, 53, 56, 1), 790px 60px 0 0 rgba(48, 53, 56, 1),
  800px 60px 0 0 rgba(48, 53, 56, 1), 810px 60px 0 0 rgba(48, 53, 56, 1),
  820px 60px 0 0 rgba(48, 53, 56, 1), 830px 60px 0 0 rgba(48, 53, 56, 1),
  840px 60px 0 0 rgba(48, 53, 56, 1), 850px 60px 0 0 rgba(48, 53, 56, 1),
  860px 60px 0 0 rgba(48, 53, 56, 1), 870px 60px 0 0 rgba(48, 53, 56, 1),
  880px 60px 0 0 rgba(48, 53, 56, 1), 890px 60px 0 0 rgba(48, 53, 56, 1),
  900px 60px 0 0 rgba(48, 53, 56, 1), 910px 60px 0 0 rgba(48, 53, 56, 1),
  920px 60px 0 0 rgba(48, 53, 56, 1), 930px 60px 0 0 rgba(48, 53, 56, 1),
  940px 60px 0 0 rgba(48, 53, 56, 1), 950px 60px 0 0 rgba(48, 53, 56, 1),
  960px 60px 0 0 rgba(48, 53, 56, 1), 970px 60px 0 0 rgba(48, 53, 56, 1),
  980px 60px 0 0 rgba(48, 53, 56, 1), 990px 60px 0 0 rgba(48, 53, 56, 1),
  1000px 60px 0 0 rgba(48, 53, 56, 1), 10px 70px 0 0 rgba(28, 32, 34, 1),
  20px 70px 0 0 rgba(219, 222, 232, 1), 30px 70px 0 0 rgba(111, 114, 121, 1),
  40px 70px 0 0 rgba(28, 32, 34, 1), 50px 70px 0 0 rgba(48, 53, 56, 1),
  60px 70px 0 0 rgba(48, 53, 56, 1), 70px 70px 0 0 rgba(48, 53, 56, 1),
  80px 70px 0 0 rgba(48, 53, 56, 1), 90px 70px 0 0 rgba(48, 53, 56, 1),
  100px 70px 0 0 rgba(48, 53, 56, 1), 110px 70px 0 0 rgba(48, 53, 56, 1),
  120px 70px 0 0 rgba(48, 53, 56, 1), 130px 70px 0 0 rgba(48, 53, 56, 1),
  140px 70px 0 0 rgba(48, 53, 56, 1), 150px 70px 0 0 rgba(48, 53, 56, 1),
  160px 70px 0 0 rgba(48, 53, 56, 1), 170px 70px 0 0 rgba(48, 53, 56, 1),
  180px 70px 0 0 rgba(48, 53, 56, 1), 190px 70px 0 0 rgba(48, 53, 56, 1),
  200px 70px 0 0 rgba(48, 53, 56, 1), 210px 70px 0 0 rgba(48, 53, 56, 1),
  220px 70px 0 0 rgba(48, 53, 56, 1), 230px 70px 0 0 rgba(48, 53, 56, 1),
  240px 70px 0 0 rgba(48, 53, 56, 1), 250px 70px 0 0 rgba(48, 53, 56, 1),
  260px 70px 0 0 rgba(48, 53, 56, 1), 270px 70px 0 0 rgba(48, 53, 56, 1),
  280px 70px 0 0 rgba(48, 53, 56, 1), 290px 70px 0 0 rgba(48, 53, 56, 1),
  300px 70px 0 0 rgba(48, 53, 56, 1), 310px 70px 0 0 rgba(48, 53, 56, 1),
  320px 70px 0 0 rgba(48, 53, 56, 1), 330px 70px 0 0 rgba(48, 53, 56, 1),
  340px 70px 0 0 rgba(48, 53, 56, 1), 350px 70px 0 0 rgba(48, 53, 56, 1),
  360px 70px 0 0 rgba(48, 53, 56, 1), 370px 70px 0 0 rgba(48, 53, 56, 1),
  380px 70px 0 0 rgba(48, 53, 56, 1), 390px 70px 0 0 rgba(48, 53, 56, 1),
  400px 70px 0 0 rgba(48, 53, 56, 1), 410px 70px 0 0 rgba(48, 53, 56, 1),
  420px 70px 0 0 rgba(48, 53, 56, 1), 430px 70px 0 0 rgba(48, 53, 56, 1),
  440px 70px 0 0 rgba(48, 53, 56, 1), 450px 70px 0 0 rgba(48, 53, 56, 1),
  460px 70px 0 0 rgba(48, 53, 56, 1), 470px 70px 0 0 rgba(48, 53, 56, 1),
  480px 70px 0 0 rgba(48, 53, 56, 1), 490px 70px 0 0 rgba(48, 53, 56, 1),
  500px 70px 0 0 rgba(48, 53, 56, 1), 510px 70px 0 0 rgba(48, 53, 56, 1),
  520px 70px 0 0 rgba(48, 53, 56, 1), 530px 70px 0 0 rgba(48, 53, 56, 1),
  540px 70px 0 0 rgba(48, 53, 56, 1), 550px 70px 0 0 rgba(48, 53, 56, 1),
  560px 70px 0 0 rgba(48, 53, 56, 1), 570px 70px 0 0 rgba(48, 53, 56, 1),
  580px 70px 0 0 rgba(48, 53, 56, 1), 590px 70px 0 0 rgba(48, 53, 56, 1),
  600px 70px 0 0 rgba(48, 53, 56, 1), 610px 70px 0 0 rgba(48, 53, 56, 1),
  620px 70px 0 0 rgba(48, 53, 56, 1), 630px 70px 0 0 rgba(48, 53, 56, 1),
  640px 70px 0 0 rgba(48, 53, 56, 1), 650px 70px 0 0 rgba(48, 53, 56, 1),
  660px 70px 0 0 rgba(48, 53, 56, 1), 670px 70px 0 0 rgba(48, 53, 56, 1),
  680px 70px 0 0 rgba(48, 53, 56, 1), 690px 70px 0 0 rgba(48, 53, 56, 1),
  700px 70px 0 0 rgba(48, 53, 56, 1), 710px 70px 0 0 rgba(48, 53, 56, 1),
  720px 70px 0 0 rgba(48, 53, 56, 1), 730px 70px 0 0 rgba(48, 53, 56, 1),
  740px 70px 0 0 rgba(48, 53, 56, 1), 750px 70px 0 0 rgba(48, 53, 56, 1),
  760px 70px 0 0 rgba(48, 53, 56, 1), 770px 70px 0 0 rgba(48, 53, 56, 1),
  780px 70px 0 0 rgba(48, 53, 56, 1), 790px 70px 0 0 rgba(48, 53, 56, 1),
  800px 70px 0 0 rgba(48, 53, 56, 1), 810px 70px 0 0 rgba(48, 53, 56, 1),
  820px 70px 0 0 rgba(48, 53, 56, 1), 830px 70px 0 0 rgba(48, 53, 56, 1),
  840px 70px 0 0 rgba(48, 53, 56, 1), 850px 70px 0 0 rgba(48, 53, 56, 1),
  860px 70px 0 0 rgba(48, 53, 56, 1), 870px 70px 0 0 rgba(48, 53, 56, 1),
  880px 70px 0 0 rgba(48, 53, 56, 1), 890px 70px 0 0 rgba(48, 53, 56, 1),
  900px 70px 0 0 rgba(48, 53, 56, 1), 910px 70px 0 0 rgba(48, 53, 56, 1),
  920px 70px 0 0 rgba(48, 53, 56, 1), 930px 70px 0 0 rgba(48, 53, 56, 1),
  940px 70px 0 0 rgba(48, 53, 56, 1), 950px 70px 0 0 rgba(48, 53, 56, 1),
  960px 70px 0 0 rgba(48, 53, 56, 1), 970px 70px 0 0 rgba(48, 53, 56, 1),
  980px 70px 0 0 rgba(48, 53, 56, 1), 990px 70px 0 0 rgba(48, 53, 56, 1),
  1000px 70px 0 0 rgba(48, 53, 56, 1), 10px 80px 0 0 rgba(28, 32, 34, 1),
  20px 80px 0 0 rgba(219, 222, 232, 1), 30px 80px 0 0 rgba(111, 114, 121, 1),
  40px 80px 0 0 rgba(28, 32, 34, 1), 50px 80px 0 0 rgba(48, 53, 56, 1),
  60px 80px 0 0 rgba(48, 53, 56, 1), 70px 80px 0 0 rgba(48, 53, 56, 1),
  80px 80px 0 0 rgba(48, 53, 56, 1), 90px 80px 0 0 rgba(48, 53, 56, 1),
  100px 80px 0 0 rgba(48, 53, 56, 1), 110px 80px 0 0 rgba(48, 53, 56, 1),
  120px 80px 0 0 rgba(48, 53, 56, 1), 130px 80px 0 0 rgba(48, 53, 56, 1),
  140px 80px 0 0 rgba(48, 53, 56, 1), 150px 80px 0 0 rgba(48, 53, 56, 1),
  160px 80px 0 0 rgba(48, 53, 56, 1), 170px 80px 0 0 rgba(48, 53, 56, 1),
  180px 80px 0 0 rgba(48, 53, 56, 1), 190px 80px 0 0 rgba(48, 53, 56, 1),
  200px 80px 0 0 rgba(48, 53, 56, 1), 210px 80px 0 0 rgba(48, 53, 56, 1),
  220px 80px 0 0 rgba(48, 53, 56, 1), 230px 80px 0 0 rgba(48, 53, 56, 1),
  240px 80px 0 0 rgba(48, 53, 56, 1), 250px 80px 0 0 rgba(48, 53, 56, 1),
  260px 80px 0 0 rgba(48, 53, 56, 1), 270px 80px 0 0 rgba(48, 53, 56, 1),
  280px 80px 0 0 rgba(48, 53, 56, 1), 290px 80px 0 0 rgba(48, 53, 56, 1),
  300px 80px 0 0 rgba(48, 53, 56, 1), 310px 80px 0 0 rgba(48, 53, 56, 1),
  320px 80px 0 0 rgba(48, 53, 56, 1), 330px 80px 0 0 rgba(48, 53, 56, 1),
  340px 80px 0 0 rgba(48, 53, 56, 1), 350px 80px 0 0 rgba(48, 53, 56, 1),
  360px 80px 0 0 rgba(48, 53, 56, 1), 370px 80px 0 0 rgba(48, 53, 56, 1),
  380px 80px 0 0 rgba(48, 53, 56, 1), 390px 80px 0 0 rgba(48, 53, 56, 1),
  400px 80px 0 0 rgba(48, 53, 56, 1), 410px 80px 0 0 rgba(48, 53, 56, 1),
  420px 80px 0 0 rgba(48, 53, 56, 1), 430px 80px 0 0 rgba(48, 53, 56, 1),
  440px 80px 0 0 rgba(48, 53, 56, 1), 450px 80px 0 0 rgba(48, 53, 56, 1),
  460px 80px 0 0 rgba(48, 53, 56, 1), 470px 80px 0 0 rgba(48, 53, 56, 1),
  480px 80px 0 0 rgba(48, 53, 56, 1), 490px 80px 0 0 rgba(48, 53, 56, 1),
  500px 80px 0 0 rgba(48, 53, 56, 1), 510px 80px 0 0 rgba(48, 53, 56, 1),
  520px 80px 0 0 rgba(48, 53, 56, 1), 530px 80px 0 0 rgba(48, 53, 56, 1),
  540px 80px 0 0 rgba(48, 53, 56, 1), 550px 80px 0 0 rgba(48, 53, 56, 1),
  560px 80px 0 0 rgba(48, 53, 56, 1), 570px 80px 0 0 rgba(48, 53, 56, 1),
  580px 80px 0 0 rgba(48, 53, 56, 1), 590px 80px 0 0 rgba(48, 53, 56, 1),
  600px 80px 0 0 rgba(48, 53, 56, 1), 610px 80px 0 0 rgba(48, 53, 56, 1),
  620px 80px 0 0 rgba(48, 53, 56, 1), 630px 80px 0 0 rgba(48, 53, 56, 1),
  640px 80px 0 0 rgba(48, 53, 56, 1), 650px 80px 0 0 rgba(48, 53, 56, 1),
  660px 80px 0 0 rgba(48, 53, 56, 1), 670px 80px 0 0 rgba(48, 53, 56, 1),
  680px 80px 0 0 rgba(48, 53, 56, 1), 690px 80px 0 0 rgba(48, 53, 56, 1),
  700px 80px 0 0 rgba(48, 53, 56, 1), 710px 80px 0 0 rgba(48, 53, 56, 1),
  720px 80px 0 0 rgba(48, 53, 56, 1), 730px 80px 0 0 rgba(48, 53, 56, 1),
  740px 80px 0 0 rgba(48, 53, 56, 1), 750px 80px 0 0 rgba(48, 53, 56, 1),
  760px 80px 0 0 rgba(48, 53, 56, 1), 770px 80px 0 0 rgba(48, 53, 56, 1),
  780px 80px 0 0 rgba(48, 53, 56, 1), 790px 80px 0 0 rgba(48, 53, 56, 1),
  800px 80px 0 0 rgba(48, 53, 56, 1), 810px 80px 0 0 rgba(48, 53, 56, 1),
  820px 80px 0 0 rgba(48, 53, 56, 1), 830px 80px 0 0 rgba(48, 53, 56, 1),
  840px 80px 0 0 rgba(48, 53, 56, 1), 850px 80px 0 0 rgba(48, 53, 56, 1),
  860px 80px 0 0 rgba(48, 53, 56, 1), 870px 80px 0 0 rgba(48, 53, 56, 1),
  880px 80px 0 0 rgba(48, 53, 56, 1), 890px 80px 0 0 rgba(48, 53, 56, 1),
  900px 80px 0 0 rgba(48, 53, 56, 1), 910px 80px 0 0 rgba(48, 53, 56, 1),
  920px 80px 0 0 rgba(48, 53, 56, 1), 930px 80px 0 0 rgba(48, 53, 56, 1),
  940px 80px 0 0 rgba(48, 53, 56, 1), 950px 80px 0 0 rgba(48, 53, 56, 1),
  960px 80px 0 0 rgba(48, 53, 56, 1), 970px 80px 0 0 rgba(48, 53, 56, 1),
  980px 80px 0 0 rgba(48, 53, 56, 1), 990px 80px 0 0 rgba(48, 53, 56, 1),
  1000px 80px 0 0 rgba(48, 53, 56, 1), 10px 90px 0 0 rgba(28, 32, 34, 1),
  20px 90px 0 0 rgba(219, 222, 232, 1), 30px 90px 0 0 rgba(111, 114, 121, 1),
  40px 90px 0 0 rgba(28, 32, 34, 1), 50px 90px 0 0 rgba(48, 53, 56, 1),
  60px 90px 0 0 rgba(48, 53, 56, 1), 70px 90px 0 0 rgba(48, 53, 56, 1),
  80px 90px 0 0 rgba(48, 53, 56, 1), 90px 90px 0 0 rgba(48, 53, 56, 1),
  100px 90px 0 0 rgba(48, 53, 56, 1), 110px 90px 0 0 rgba(48, 53, 56, 1),
  120px 90px 0 0 rgba(48, 53, 56, 1), 130px 90px 0 0 rgba(48, 53, 56, 1),
  140px 90px 0 0 rgba(48, 53, 56, 1), 150px 90px 0 0 rgba(48, 53, 56, 1),
  160px 90px 0 0 rgba(48, 53, 56, 1), 170px 90px 0 0 rgba(48, 53, 56, 1),
  180px 90px 0 0 rgba(48, 53, 56, 1), 190px 90px 0 0 rgba(48, 53, 56, 1),
  200px 90px 0 0 rgba(48, 53, 56, 1), 210px 90px 0 0 rgba(48, 53, 56, 1),
  220px 90px 0 0 rgba(48, 53, 56, 1), 230px 90px 0 0 rgba(48, 53, 56, 1),
  240px 90px 0 0 rgba(48, 53, 56, 1), 250px 90px 0 0 rgba(48, 53, 56, 1),
  260px 90px 0 0 rgba(48, 53, 56, 1), 270px 90px 0 0 rgba(48, 53, 56, 1),
  280px 90px 0 0 rgba(48, 53, 56, 1), 290px 90px 0 0 rgba(48, 53, 56, 1),
  300px 90px 0 0 rgba(48, 53, 56, 1), 310px 90px 0 0 rgba(48, 53, 56, 1),
  320px 90px 0 0 rgba(48, 53, 56, 1), 330px 90px 0 0 rgba(48, 53, 56, 1),
  340px 90px 0 0 rgba(48, 53, 56, 1), 350px 90px 0 0 rgba(48, 53, 56, 1),
  360px 90px 0 0 rgba(48, 53, 56, 1), 370px 90px 0 0 rgba(48, 53, 56, 1),
  380px 90px 0 0 rgba(48, 53, 56, 1), 390px 90px 0 0 rgba(48, 53, 56, 1),
  400px 90px 0 0 rgba(48, 53, 56, 1), 410px 90px 0 0 rgba(48, 53, 56, 1),
  420px 90px 0 0 rgba(48, 53, 56, 1), 430px 90px 0 0 rgba(48, 53, 56, 1),
  440px 90px 0 0 rgba(48, 53, 56, 1), 450px 90px 0 0 rgba(48, 53, 56, 1),
  460px 90px 0 0 rgba(48, 53, 56, 1), 470px 90px 0 0 rgba(48, 53, 56, 1),
  480px 90px 0 0 rgba(48, 53, 56, 1), 490px 90px 0 0 rgba(48, 53, 56, 1),
  500px 90px 0 0 rgba(48, 53, 56, 1), 510px 90px 0 0 rgba(48, 53, 56, 1),
  520px 90px 0 0 rgba(48, 53, 56, 1), 530px 90px 0 0 rgba(48, 53, 56, 1),
  540px 90px 0 0 rgba(48, 53, 56, 1), 550px 90px 0 0 rgba(48, 53, 56, 1),
  560px 90px 0 0 rgba(48, 53, 56, 1), 570px 90px 0 0 rgba(48, 53, 56, 1),
  580px 90px 0 0 rgba(48, 53, 56, 1), 590px 90px 0 0 rgba(48, 53, 56, 1),
  600px 90px 0 0 rgba(48, 53, 56, 1), 610px 90px 0 0 rgba(48, 53, 56, 1),
  620px 90px 0 0 rgba(48, 53, 56, 1), 630px 90px 0 0 rgba(48, 53, 56, 1),
  640px 90px 0 0 rgba(48, 53, 56, 1), 650px 90px 0 0 rgba(48, 53, 56, 1),
  660px 90px 0 0 rgba(48, 53, 56, 1), 670px 90px 0 0 rgba(48, 53, 56, 1),
  680px 90px 0 0 rgba(48, 53, 56, 1), 690px 90px 0 0 rgba(48, 53, 56, 1),
  700px 90px 0 0 rgba(48, 53, 56, 1), 710px 90px 0 0 rgba(48, 53, 56, 1),
  720px 90px 0 0 rgba(48, 53, 56, 1), 730px 90px 0 0 rgba(48, 53, 56, 1),
  740px 90px 0 0 rgba(48, 53, 56, 1), 750px 90px 0 0 rgba(48, 53, 56, 1),
  760px 90px 0 0 rgba(48, 53, 56, 1), 770px 90px 0 0 rgba(48, 53, 56, 1),
  780px 90px 0 0 rgba(48, 53, 56, 1), 790px 90px 0 0 rgba(48, 53, 56, 1),
  800px 90px 0 0 rgba(48, 53, 56, 1), 810px 90px 0 0 rgba(48, 53, 56, 1),
  820px 90px 0 0 rgba(48, 53, 56, 1), 830px 90px 0 0 rgba(48, 53, 56, 1),
  840px 90px 0 0 rgba(48, 53, 56, 1), 850px 90px 0 0 rgba(48, 53, 56, 1),
  860px 90px 0 0 rgba(48, 53, 56, 1), 870px 90px 0 0 rgba(48, 53, 56, 1),
  880px 90px 0 0 rgba(48, 53, 56, 1), 890px 90px 0 0 rgba(48, 53, 56, 1),
  900px 90px 0 0 rgba(48, 53, 56, 1), 910px 90px 0 0 rgba(48, 53, 56, 1),
  920px 90px 0 0 rgba(48, 53, 56, 1), 930px 90px 0 0 rgba(48, 53, 56, 1),
  940px 90px 0 0 rgba(48, 53, 56, 1), 950px 90px 0 0 rgba(48, 53, 56, 1),
  960px 90px 0 0 rgba(48, 53, 56, 1), 970px 90px 0 0 rgba(48, 53, 56, 1),
  980px 90px 0 0 rgba(48, 53, 56, 1), 990px 90px 0 0 rgba(48, 53, 56, 1),
  1000px 90px 0 0 rgba(48, 53, 56, 1), 10px 100px 0 0 rgba(28, 32, 34, 1),
  20px 100px 0 0 rgba(219, 222, 232, 1), 30px 100px 0 0 rgba(111, 114, 121, 1),
  40px 100px 0 0 rgba(28, 32, 34, 1), 50px 100px 0 0 rgba(48, 53, 56, 1),
  60px 100px 0 0 rgba(48, 53, 56, 1), 70px 100px 0 0 rgba(48, 53, 56, 1),
  80px 100px 0 0 rgba(48, 53, 56, 1), 90px 100px 0 0 rgba(48, 53, 56, 1),
  100px 100px 0 0 rgba(48, 53, 56, 1), 110px 100px 0 0 rgba(48, 53, 56, 1),
  120px 100px 0 0 rgba(48, 53, 56, 1), 130px 100px 0 0 rgba(48, 53, 56, 1),
  140px 100px 0 0 rgba(48, 53, 56, 1), 150px 100px 0 0 rgba(48, 53, 56, 1),
  160px 100px 0 0 rgba(48, 53, 56, 1), 170px 100px 0 0 rgba(48, 53, 56, 1),
  180px 100px 0 0 rgba(48, 53, 56, 1), 190px 100px 0 0 rgba(48, 53, 56, 1),
  200px 100px 0 0 rgba(48, 53, 56, 1), 210px 100px 0 0 rgba(48, 53, 56, 1),
  220px 100px 0 0 rgba(48, 53, 56, 1), 230px 100px 0 0 rgba(48, 53, 56, 1),
  240px 100px 0 0 rgba(48, 53, 56, 1), 250px 100px 0 0 rgba(48, 53, 56, 1),
  260px 100px 0 0 rgba(48, 53, 56, 1), 270px 100px 0 0 rgba(48, 53, 56, 1),
  280px 100px 0 0 rgba(48, 53, 56, 1), 290px 100px 0 0 rgba(48, 53, 56, 1),
  300px 100px 0 0 rgba(48, 53, 56, 1), 310px 100px 0 0 rgba(48, 53, 56, 1),
  320px 100px 0 0 rgba(48, 53, 56, 1), 330px 100px 0 0 rgba(48, 53, 56, 1),
  340px 100px 0 0 rgba(48, 53, 56, 1), 350px 100px 0 0 rgba(48, 53, 56, 1),
  360px 100px 0 0 rgba(48, 53, 56, 1), 370px 100px 0 0 rgba(48, 53, 56, 1),
  380px 100px 0 0 rgba(48, 53, 56, 1), 390px 100px 0 0 rgba(48, 53, 56, 1),
  400px 100px 0 0 rgba(48, 53, 56, 1), 410px 100px 0 0 rgba(48, 53, 56, 1),
  420px 100px 0 0 rgba(48, 53, 56, 1), 430px 100px 0 0 rgba(48, 53, 56, 1),
  440px 100px 0 0 rgba(48, 53, 56, 1), 450px 100px 0 0 rgba(48, 53, 56, 1),
  460px 100px 0 0 rgba(48, 53, 56, 1), 470px 100px 0 0 rgba(48, 53, 56, 1),
  480px 100px 0 0 rgba(48, 53, 56, 1), 490px 100px 0 0 rgba(48, 53, 56, 1),
  500px 100px 0 0 rgba(48, 53, 56, 1), 510px 100px 0 0 rgba(48, 53, 56, 1),
  520px 100px 0 0 rgba(48, 53, 56, 1), 530px 100px 0 0 rgba(48, 53, 56, 1),
  540px 100px 0 0 rgba(48, 53, 56, 1), 550px 100px 0 0 rgba(48, 53, 56, 1),
  560px 100px 0 0 rgba(48, 53, 56, 1), 570px 100px 0 0 rgba(48, 53, 56, 1),
  580px 100px 0 0 rgba(48, 53, 56, 1), 590px 100px 0 0 rgba(48, 53, 56, 1),
  600px 100px 0 0 rgba(48, 53, 56, 1), 610px 100px 0 0 rgba(48, 53, 56, 1),
  620px 100px 0 0 rgba(48, 53, 56, 1), 630px 100px 0 0 rgba(48, 53, 56, 1),
  640px 100px 0 0 rgba(48, 53, 56, 1), 650px 100px 0 0 rgba(48, 53, 56, 1),
  660px 100px 0 0 rgba(48, 53, 56, 1), 670px 100px 0 0 rgba(48, 53, 56, 1),
  680px 100px 0 0 rgba(48, 53, 56, 1), 690px 100px 0 0 rgba(48, 53, 56, 1),
  700px 100px 0 0 rgba(48, 53, 56, 1), 710px 100px 0 0 rgba(48, 53, 56, 1),
  720px 100px 0 0 rgba(48, 53, 56, 1), 730px 100px 0 0 rgba(48, 53, 56, 1),
  740px 100px 0 0 rgba(48, 53, 56, 1), 750px 100px 0 0 rgba(48, 53, 56, 1),
  760px 100px 0 0 rgba(48, 53, 56, 1), 770px 100px 0 0 rgba(48, 53, 56, 1),
  780px 100px 0 0 rgba(48, 53, 56, 1), 790px 100px 0 0 rgba(48, 53, 56, 1),
  800px 100px 0 0 rgba(48, 53, 56, 1), 810px 100px 0 0 rgba(48, 53, 56, 1),
  820px 100px 0 0 rgba(48, 53, 56, 1), 830px 100px 0 0 rgba(48, 53, 56, 1),
  840px 100px 0 0 rgba(48, 53, 56, 1), 850px 100px 0 0 rgba(48, 53, 56, 1),
  860px 100px 0 0 rgba(48, 53, 56, 1), 870px 100px 0 0 rgba(48, 53, 56, 1),
  880px 100px 0 0 rgba(48, 53, 56, 1), 890px 100px 0 0 rgba(48, 53, 56, 1),
  900px 100px 0 0 rgba(48, 53, 56, 1), 910px 100px 0 0 rgba(48, 53, 56, 1),
  920px 100px 0 0 rgba(48, 53, 56, 1), 930px 100px 0 0 rgba(48, 53, 56, 1),
  940px 100px 0 0 rgba(48, 53, 56, 1), 950px 100px 0 0 rgba(48, 53, 56, 1),
  960px 100px 0 0 rgba(48, 53, 56, 1), 970px 100px 0 0 rgba(48, 53, 56, 1),
  980px 100px 0 0 rgba(48, 53, 56, 1), 990px 100px 0 0 rgba(48, 53, 56, 1),
  1000px 100px 0 0 rgba(242, 245, 252, 1), 10px 110px 0 0 rgba(28, 32, 34, 1),
  20px 110px 0 0 rgba(219, 222, 232, 1), 30px 110px 0 0 rgba(111, 114, 121, 1),
  40px 110px 0 0 rgba(28, 32, 34, 1), 50px 110px 0 0 rgba(48, 53, 56, 1),
  60px 110px 0 0 rgba(48, 53, 56, 1), 70px 110px 0 0 rgba(48, 53, 56, 1),
  80px 110px 0 0 rgba(48, 53, 56, 1), 90px 110px 0 0 rgba(48, 53, 56, 1),
  100px 110px 0 0 rgba(48, 53, 56, 1), 110px 110px 0 0 rgba(48, 53, 56, 1),
  120px 110px 0 0 rgba(48, 53, 56, 1), 130px 110px 0 0 rgba(48, 53, 56, 1),
  140px 110px 0 0 rgba(242, 245, 252, 1), 150px 110px 0 0 rgba(48, 53, 56, 1),
  160px 110px 0 0 rgba(242, 245, 252, 1), 170px 110px 0 0 rgba(242, 245, 252, 1),
  180px 110px 0 0 rgba(242, 245, 252, 1), 190px 110px 0 0 rgba(48, 53, 56, 1),
  200px 110px 0 0 rgba(48, 53, 56, 1), 210px 110px 0 0 rgba(48, 53, 56, 1),
  220px 110px 0 0 rgba(48, 53, 56, 1), 230px 110px 0 0 rgba(48, 53, 56, 1),
  240px 110px 0 0 rgba(48, 53, 56, 1), 250px 110px 0 0 rgba(48, 53, 56, 1),
  260px 110px 0 0 rgba(48, 53, 56, 1), 270px 110px 0 0 rgba(48, 53, 56, 1),
  280px 110px 0 0 rgba(48, 53, 56, 1), 290px 110px 0 0 rgba(48, 53, 56, 1),
  300px 110px 0 0 rgba(48, 53, 56, 1), 310px 110px 0 0 rgba(48, 53, 56, 1),
  320px 110px 0 0 rgba(242, 245, 252, 1), 330px 110px 0 0 rgba(48, 53, 56, 1),
  340px 110px 0 0 rgba(242, 245, 252, 1), 350px 110px 0 0 rgba(48, 53, 56, 1),
  360px 110px 0 0 rgba(242, 245, 252, 1), 370px 110px 0 0 rgba(48, 53, 56, 1),
  380px 110px 0 0 rgba(242, 245, 252, 1), 390px 110px 0 0 rgba(242, 245, 252, 1),
  400px 110px 0 0 rgba(48, 53, 56, 1), 410px 110px 0 0 rgba(242, 245, 252, 1),
  420px 110px 0 0 rgba(48, 53, 56, 1), 430px 110px 0 0 rgba(242, 245, 252, 1),
  440px 110px 0 0 rgba(242, 245, 252, 1), 450px 110px 0 0 rgba(242, 245, 252, 1),
  460px 110px 0 0 rgba(48, 53, 56, 1), 470px 110px 0 0 rgba(48, 53, 56, 1),
  480px 110px 0 0 rgba(48, 53, 56, 1), 490px 110px 0 0 rgba(242, 245, 252, 1),
  500px 110px 0 0 rgba(48, 53, 56, 1), 510px 110px 0 0 rgba(48, 53, 56, 1),
  520px 110px 0 0 rgba(242, 245, 252, 1), 530px 110px 0 0 rgba(48, 53, 56, 1),
  540px 110px 0 0 rgba(242, 245, 252, 1), 550px 110px 0 0 rgba(48, 53, 56, 1),
  560px 110px 0 0 rgba(242, 245, 252, 1), 570px 110px 0 0 rgba(242, 245, 252, 1),
  580px 110px 0 0 rgba(48, 53, 56, 1), 590px 110px 0 0 rgba(242, 245, 252, 1),
  600px 110px 0 0 rgba(48, 53, 56, 1), 610px 110px 0 0 rgba(48, 53, 56, 1),
  620px 110px 0 0 rgba(242, 245, 252, 1), 630px 110px 0 0 rgba(242, 245, 252, 1),
  640px 110px 0 0 rgba(48, 53, 56, 1), 650px 110px 0 0 rgba(48, 53, 56, 1),
  660px 110px 0 0 rgba(242, 245, 252, 1), 670px 110px 0 0 rgba(242, 245, 252, 1),
  680px 110px 0 0 rgba(48, 53, 56, 1), 690px 110px 0 0 rgba(242, 245, 252, 1),
  700px 110px 0 0 rgba(48, 53, 56, 1), 710px 110px 0 0 rgba(242, 245, 252, 1),
  720px 110px 0 0 rgba(242, 245, 252, 1), 730px 110px 0 0 rgba(48, 53, 56, 1),
  740px 110px 0 0 rgba(242, 245, 252, 1), 750px 110px 0 0 rgba(48, 53, 56, 1),
  760px 110px 0 0 rgba(242, 245, 252, 1), 770px 110px 0 0 rgba(48, 53, 56, 1),
  780px 110px 0 0 rgba(48, 53, 56, 1), 790px 110px 0 0 rgba(48, 53, 56, 1),
  800px 110px 0 0 rgba(48, 53, 56, 1), 810px 110px 0 0 rgba(48, 53, 56, 1),
  820px 110px 0 0 rgba(48, 53, 56, 1), 830px 110px 0 0 rgba(48, 53, 56, 1),
  840px 110px 0 0 rgba(48, 53, 56, 1), 850px 110px 0 0 rgba(48, 53, 56, 1),
  860px 110px 0 0 rgba(48, 53, 56, 1), 870px 110px 0 0 rgba(48, 53, 56, 1),
  880px 110px 0 0 rgba(48, 53, 56, 1), 890px 110px 0 0 rgba(48, 53, 56, 1),
  900px 110px 0 0 rgba(48, 53, 56, 1), 910px 110px 0 0 rgba(48, 53, 56, 1),
  920px 110px 0 0 rgba(48, 53, 56, 1), 930px 110px 0 0 rgba(48, 53, 56, 1),
  940px 110px 0 0 rgba(48, 53, 56, 1), 950px 110px 0 0 rgba(48, 53, 56, 1),
  960px 110px 0 0 rgba(48, 53, 56, 1), 970px 110px 0 0 rgba(48, 53, 56, 1),
  980px 110px 0 0 rgba(48, 53, 56, 1), 990px 110px 0 0 rgba(242, 245, 252, 1),
  1000px 110px 0 0 rgba(48, 53, 56, 1), 10px 120px 0 0 rgba(28, 32, 34, 1),
  20px 120px 0 0 rgba(219, 222, 232, 1), 30px 120px 0 0 rgba(111, 114, 121, 1),
  40px 120px 0 0 rgba(28, 32, 34, 1), 50px 120px 0 0 rgba(48, 53, 56, 1),
  60px 120px 0 0 rgba(48, 53, 56, 1), 70px 120px 0 0 rgba(48, 53, 56, 1),
  80px 120px 0 0 rgba(48, 53, 56, 1), 90px 120px 0 0 rgba(48, 53, 56, 1),
  100px 120px 0 0 rgba(48, 53, 56, 1), 110px 120px 0 0 rgba(48, 53, 56, 1),
  120px 120px 0 0 rgba(48, 53, 56, 1), 130px 120px 0 0 rgba(48, 53, 56, 1),
  140px 120px 0 0 rgba(242, 245, 252, 1), 150px 120px 0 0 rgba(48, 53, 56, 1),
  160px 120px 0 0 rgba(48, 53, 56, 1), 170px 120px 0 0 rgba(48, 53, 56, 1),
  180px 120px 0 0 rgba(48, 53, 56, 1), 190px 120px 0 0 rgba(48, 53, 56, 1),
  200px 120px 0 0 rgba(48, 53, 56, 1), 210px 120px 0 0 rgba(48, 53, 56, 1),
  220px 120px 0 0 rgba(48, 53, 56, 1), 230px 120px 0 0 rgba(48, 53, 56, 1),
  240px 120px 0 0 rgba(48, 53, 56, 1), 250px 120px 0 0 rgba(48, 53, 56, 1),
  260px 120px 0 0 rgba(48, 53, 56, 1), 270px 120px 0 0 rgba(48, 53, 56, 1),
  280px 120px 0 0 rgba(48, 53, 56, 1), 290px 120px 0 0 rgba(48, 53, 56, 1),
  300px 120px 0 0 rgba(48, 53, 56, 1), 310px 120px 0 0 rgba(48, 53, 56, 1),
  320px 120px 0 0 rgba(48, 53, 56, 1), 330px 120px 0 0 rgba(48, 53, 56, 1),
  340px 120px 0 0 rgba(48, 53, 56, 1), 350px 120px 0 0 rgba(48, 53, 56, 1),
  360px 120px 0 0 rgba(48, 53, 56, 1), 370px 120px 0 0 rgba(48, 53, 56, 1),
  380px 120px 0 0 rgba(48, 53, 56, 1), 390px 120px 0 0 rgba(48, 53, 56, 1),
  400px 120px 0 0 rgba(48, 53, 56, 1), 410px 120px 0 0 rgba(48, 53, 56, 1),
  420px 120px 0 0 rgba(48, 53, 56, 1), 430px 120px 0 0 rgba(48, 53, 56, 1),
  440px 120px 0 0 rgba(48, 53, 56, 1), 450px 120px 0 0 rgba(48, 53, 56, 1),
  460px 120px 0 0 rgba(48, 53, 56, 1), 470px 120px 0 0 rgba(48, 53, 56, 1),
  480px 120px 0 0 rgba(48, 53, 56, 1), 490px 120px 0 0 rgba(48, 53, 56, 1),
  500px 120px 0 0 rgba(48, 53, 56, 1), 510px 120px 0 0 rgba(48, 53, 56, 1),
  520px 120px 0 0 rgba(48, 53, 56, 1), 530px 120px 0 0 rgba(48, 53, 56, 1),
  540px 120px 0 0 rgba(48, 53, 56, 1), 550px 120px 0 0 rgba(48, 53, 56, 1),
  560px 120px 0 0 rgba(48, 53, 56, 1), 570px 120px 0 0 rgba(48, 53, 56, 1),
  580px 120px 0 0 rgba(48, 53, 56, 1), 590px 120px 0 0 rgba(48, 53, 56, 1),
  600px 120px 0 0 rgba(48, 53, 56, 1), 610px 120px 0 0 rgba(48, 53, 56, 1),
  620px 120px 0 0 rgba(48, 53, 56, 1), 630px 120px 0 0 rgba(48, 53, 56, 1),
  640px 120px 0 0 rgba(48, 53, 56, 1), 650px 120px 0 0 rgba(48, 53, 56, 1),
  660px 120px 0 0 rgba(48, 53, 56, 1), 670px 120px 0 0 rgba(48, 53, 56, 1),
  680px 120px 0 0 rgba(48, 53, 56, 1), 690px 120px 0 0 rgba(48, 53, 56, 1),
  700px 120px 0 0 rgba(48, 53, 56, 1), 710px 120px 0 0 rgba(48, 53, 56, 1),
  720px 120px 0 0 rgba(48, 53, 56, 1), 730px 120px 0 0 rgba(48, 53, 56, 1),
  740px 120px 0 0 rgba(48, 53, 56, 1), 750px 120px 0 0 rgba(48, 53, 56, 1),
  760px 120px 0 0 rgba(242, 245, 252, 1), 770px 120px 0 0 rgba(48, 53, 56, 1),
  780px 120px 0 0 rgba(48, 53, 56, 1), 790px 120px 0 0 rgba(48, 53, 56, 1),
  800px 120px 0 0 rgba(48, 53, 56, 1), 810px 120px 0 0 rgba(48, 53, 56, 1),
  820px 120px 0 0 rgba(48, 53, 56, 1), 830px 120px 0 0 rgba(48, 53, 56, 1),
  840px 120px 0 0 rgba(48, 53, 56, 1), 850px 120px 0 0 rgba(48, 53, 56, 1),
  860px 120px 0 0 rgba(48, 53, 56, 1), 870px 120px 0 0 rgba(48, 53, 56, 1),
  880px 120px 0 0 rgba(48, 53, 56, 1), 890px 120px 0 0 rgba(48, 53, 56, 1),
  900px 120px 0 0 rgba(48, 53, 56, 1), 910px 120px 0 0 rgba(48, 53, 56, 1),
  920px 120px 0 0 rgba(48, 53, 56, 1), 930px 120px 0 0 rgba(48, 53, 56, 1),
  940px 120px 0 0 rgba(48, 53, 56, 1), 950px 120px 0 0 rgba(48, 53, 56, 1),
  960px 120px 0 0 rgba(48, 53, 56, 1), 970px 120px 0 0 rgba(48, 53, 56, 1),
  980px 120px 0 0 rgba(242, 245, 252, 1), 990px 120px 0 0 rgba(48, 53, 56, 1),
  1000px 120px 0 0 rgba(48, 53, 56, 1), 10px 130px 0 0 rgba(28, 32, 34, 1),
  20px 130px 0 0 rgba(219, 222, 232, 1), 30px 130px 0 0 rgba(111, 114, 121, 1),
  40px 130px 0 0 rgba(28, 32, 34, 1), 50px 130px 0 0 rgba(48, 53, 56, 1),
  60px 130px 0 0 rgba(48, 53, 56, 1), 70px 130px 0 0 rgba(48, 53, 56, 1),
  80px 130px 0 0 rgba(48, 53, 56, 1), 90px 130px 0 0 rgba(48, 53, 56, 1),
  100px 130px 0 0 rgba(48, 53, 56, 1), 110px 130px 0 0 rgba(48, 53, 56, 1),
  120px 130px 0 0 rgba(48, 53, 56, 1), 130px 130px 0 0 rgba(48, 53, 56, 1),
  140px 130px 0 0 rgba(242, 245, 252, 1), 150px 130px 0 0 rgba(48, 53, 56, 1),
  160px 130px 0 0 rgba(48, 53, 56, 1), 170px 130px 0 0 rgba(48, 53, 56, 1),
  180px 130px 0 0 rgba(48, 53, 56, 1), 190px 130px 0 0 rgba(48, 53, 56, 1),
  200px 130px 0 0 rgba(48, 53, 56, 1), 210px 130px 0 0 rgba(48, 53, 56, 1),
  220px 130px 0 0 rgba(48, 53, 56, 1), 230px 130px 0 0 rgba(48, 53, 56, 1),
  240px 130px 0 0 rgba(48, 53, 56, 1), 250px 130px 0 0 rgba(48, 53, 56, 1),
  260px 130px 0 0 rgba(48, 53, 56, 1), 270px 130px 0 0 rgba(48, 53, 56, 1),
  280px 130px 0 0 rgba(48, 53, 56, 1), 290px 130px 0 0 rgba(48, 53, 56, 1),
  300px 130px 0 0 rgba(48, 53, 56, 1), 310px 130px 0 0 rgba(48, 53, 56, 1),
  320px 130px 0 0 rgba(48, 53, 56, 1), 330px 130px 0 0 rgba(48, 53, 56, 1),
  340px 130px 0 0 rgba(48, 53, 56, 1), 350px 130px 0 0 rgba(48, 53, 56, 1),
  360px 130px 0 0 rgba(48, 53, 56, 1), 370px 130px 0 0 rgba(48, 53, 56, 1),
  380px 130px 0 0 rgba(48, 53, 56, 1), 390px 130px 0 0 rgba(48, 53, 56, 1),
  400px 130px 0 0 rgba(48, 53, 56, 1), 410px 130px 0 0 rgba(48, 53, 56, 1),
  420px 130px 0 0 rgba(48, 53, 56, 1), 430px 130px 0 0 rgba(48, 53, 56, 1),
  440px 130px 0 0 rgba(48, 53, 56, 1), 450px 130px 0 0 rgba(48, 53, 56, 1),
  460px 130px 0 0 rgba(48, 53, 56, 1), 470px 130px 0 0 rgba(48, 53, 56, 1),
  480px 130px 0 0 rgba(48, 53, 56, 1), 490px 130px 0 0 rgba(48, 53, 56, 1),
  500px 130px 0 0 rgba(48, 53, 56, 1), 510px 130px 0 0 rgba(48, 53, 56, 1),
  520px 130px 0 0 rgba(48, 53, 56, 1), 530px 130px 0 0 rgba(48, 53, 56, 1),
  540px 130px 0 0 rgba(48, 53, 56, 1), 550px 130px 0 0 rgba(48, 53, 56, 1),
  560px 130px 0 0 rgba(48, 53, 56, 1), 570px 130px 0 0 rgba(48, 53, 56, 1),
  580px 130px 0 0 rgba(48, 53, 56, 1), 590px 130px 0 0 rgba(48, 53, 56, 1),
  600px 130px 0 0 rgba(48, 53, 56, 1), 610px 130px 0 0 rgba(48, 53, 56, 1),
  620px 130px 0 0 rgba(48, 53, 56, 1), 630px 130px 0 0 rgba(48, 53, 56, 1),
  640px 130px 0 0 rgba(48, 53, 56, 1), 650px 130px 0 0 rgba(48, 53, 56, 1),
  660px 130px 0 0 rgba(48, 53, 56, 1), 670px 130px 0 0 rgba(48, 53, 56, 1),
  680px 130px 0 0 rgba(48, 53, 56, 1), 690px 130px 0 0 rgba(48, 53, 56, 1),
  700px 130px 0 0 rgba(48, 53, 56, 1), 710px 130px 0 0 rgba(48, 53, 56, 1),
  720px 130px 0 0 rgba(48, 53, 56, 1), 730px 130px 0 0 rgba(48, 53, 56, 1),
  740px 130px 0 0 rgba(48, 53, 56, 1), 750px 130px 0 0 rgba(48, 53, 56, 1),
  760px 130px 0 0 rgba(242, 245, 252, 1), 770px 130px 0 0 rgba(48, 53, 56, 1),
  780px 130px 0 0 rgba(48, 53, 56, 1), 790px 130px 0 0 rgba(48, 53, 56, 1),
  800px 130px 0 0 rgba(48, 53, 56, 1), 810px 130px 0 0 rgba(48, 53, 56, 1),
  820px 130px 0 0 rgba(48, 53, 56, 1), 830px 130px 0 0 rgba(48, 53, 56, 1),
  840px 130px 0 0 rgba(48, 53, 56, 1), 850px 130px 0 0 rgba(48, 53, 56, 1),
  860px 130px 0 0 rgba(48, 53, 56, 1), 870px 130px 0 0 rgba(48, 53, 56, 1),
  880px 130px 0 0 rgba(48, 53, 56, 1), 890px 130px 0 0 rgba(48, 53, 56, 1),
  900px 130px 0 0 rgba(48, 53, 56, 1), 910px 130px 0 0 rgba(48, 53, 56, 1),
  920px 130px 0 0 rgba(48, 53, 56, 1), 930px 130px 0 0 rgba(48, 53, 56, 1),
  940px 130px 0 0 rgba(48, 53, 56, 1), 950px 130px 0 0 rgba(48, 53, 56, 1),
  960px 130px 0 0 rgba(48, 53, 56, 1), 970px 130px 0 0 rgba(242, 245, 252, 1),
  980px 130px 0 0 rgba(48, 53, 56, 1), 990px 130px 0 0 rgba(48, 53, 56, 1),
  1000px 130px 0 0 rgba(48, 53, 56, 1), 10px 140px 0 0 rgba(28, 32, 34, 1),
  20px 140px 0 0 rgba(219, 222, 232, 1), 30px 140px 0 0 rgba(111, 114, 121, 1),
  40px 140px 0 0 rgba(28, 32, 34, 1), 50px 140px 0 0 rgba(48, 53, 56, 1),
  60px 140px 0 0 rgba(48, 53, 56, 1), 70px 140px 0 0 rgba(48, 53, 56, 1),
  80px 140px 0 0 rgba(48, 53, 56, 1), 90px 140px 0 0 rgba(48, 53, 56, 1),
  100px 140px 0 0 rgba(48, 53, 56, 1), 110px 140px 0 0 rgba(48, 53, 56, 1),
  120px 140px 0 0 rgba(48, 53, 56, 1), 130px 140px 0 0 rgba(48, 53, 56, 1),
  140px 140px 0 0 rgba(242, 245, 252, 1), 150px 140px 0 0 rgba(48, 53, 56, 1),
  160px 140px 0 0 rgba(48, 53, 56, 1), 170px 140px 0 0 rgba(48, 53, 56, 1),
  180px 140px 0 0 rgba(48, 53, 56, 1), 190px 140px 0 0 rgba(48, 53, 56, 1),
  200px 140px 0 0 rgba(48, 53, 56, 1), 210px 140px 0 0 rgba(48, 53, 56, 1),
  220px 140px 0 0 rgba(48, 53, 56, 1), 230px 140px 0 0 rgba(48, 53, 56, 1),
  240px 140px 0 0 rgba(48, 53, 56, 1), 250px 140px 0 0 rgba(48, 53, 56, 1),
  260px 140px 0 0 rgba(48, 53, 56, 1), 270px 140px 0 0 rgba(48, 53, 56, 1),
  280px 140px 0 0 rgba(48, 53, 56, 1), 290px 140px 0 0 rgba(48, 53, 56, 1),
  300px 140px 0 0 rgba(48, 53, 56, 1), 310px 140px 0 0 rgba(48, 53, 56, 1),
  320px 140px 0 0 rgba(48, 53, 56, 1), 330px 140px 0 0 rgba(48, 53, 56, 1),
  340px 140px 0 0 rgba(48, 53, 56, 1), 350px 140px 0 0 rgba(48, 53, 56, 1),
  360px 140px 0 0 rgba(48, 53, 56, 1), 370px 140px 0 0 rgba(48, 53, 56, 1),
  380px 140px 0 0 rgba(48, 53, 56, 1), 390px 140px 0 0 rgba(48, 53, 56, 1),
  400px 140px 0 0 rgba(48, 53, 56, 1), 410px 140px 0 0 rgba(48, 53, 56, 1),
  420px 140px 0 0 rgba(48, 53, 56, 1), 430px 140px 0 0 rgba(48, 53, 56, 1),
  440px 140px 0 0 rgba(48, 53, 56, 1), 450px 140px 0 0 rgba(48, 53, 56, 1),
  460px 140px 0 0 rgba(48, 53, 56, 1), 470px 140px 0 0 rgba(48, 53, 56, 1),
  480px 140px 0 0 rgba(48, 53, 56, 1), 490px 140px 0 0 rgba(48, 53, 56, 1),
  500px 140px 0 0 rgba(48, 53, 56, 1), 510px 140px 0 0 rgba(48, 53, 56, 1),
  520px 140px 0 0 rgba(48, 53, 56, 1), 530px 140px 0 0 rgba(48, 53, 56, 1),
  540px 140px 0 0 rgba(48, 53, 56, 1), 550px 140px 0 0 rgba(48, 53, 56, 1),
  560px 140px 0 0 rgba(48, 53, 56, 1), 570px 140px 0 0 rgba(48, 53, 56, 1),
  580px 140px 0 0 rgba(48, 53, 56, 1), 590px 140px 0 0 rgba(48, 53, 56, 1),
  600px 140px 0 0 rgba(48, 53, 56, 1), 610px 140px 0 0 rgba(48, 53, 56, 1),
  620px 140px 0 0 rgba(48, 53, 56, 1), 630px 140px 0 0 rgba(48, 53, 56, 1),
  640px 140px 0 0 rgba(48, 53, 56, 1), 650px 140px 0 0 rgba(48, 53, 56, 1),
  660px 140px 0 0 rgba(48, 53, 56, 1), 670px 140px 0 0 rgba(48, 53, 56, 1),
  680px 140px 0 0 rgba(48, 53, 56, 1), 690px 140px 0 0 rgba(48, 53, 56, 1),
  700px 140px 0 0 rgba(48, 53, 56, 1), 710px 140px 0 0 rgba(48, 53, 56, 1),
  720px 140px 0 0 rgba(48, 53, 56, 1), 730px 140px 0 0 rgba(48, 53, 56, 1),
  740px 140px 0 0 rgba(48, 53, 56, 1), 750px 140px 0 0 rgba(48, 53, 56, 1),
  760px 140px 0 0 rgba(242, 245, 252, 1), 770px 140px 0 0 rgba(48, 53, 56, 1),
  780px 140px 0 0 rgba(48, 53, 56, 1), 790px 140px 0 0 rgba(48, 53, 56, 1),
  800px 140px 0 0 rgba(48, 53, 56, 1), 810px 140px 0 0 rgba(48, 53, 56, 1),
  820px 140px 0 0 rgba(48, 53, 56, 1), 830px 140px 0 0 rgba(48, 53, 56, 1),
  840px 140px 0 0 rgba(48, 53, 56, 1), 850px 140px 0 0 rgba(48, 53, 56, 1),
  860px 140px 0 0 rgba(48, 53, 56, 1), 870px 140px 0 0 rgba(48, 53, 56, 1),
  880px 140px 0 0 rgba(48, 53, 56, 1), 890px 140px 0 0 rgba(48, 53, 56, 1),
  900px 140px 0 0 rgba(48, 53, 56, 1), 910px 140px 0 0 rgba(48, 53, 56, 1),
  920px 140px 0 0 rgba(48, 53, 56, 1), 930px 140px 0 0 rgba(48, 53, 56, 1),
  940px 140px 0 0 rgba(48, 53, 56, 1), 950px 140px 0 0 rgba(48, 53, 56, 1),
  960px 140px 0 0 rgba(242, 245, 252, 1), 970px 140px 0 0 rgba(48, 53, 56, 1),
  980px 140px 0 0 rgba(48, 53, 56, 1), 990px 140px 0 0 rgba(48, 53, 56, 1),
  1000px 140px 0 0 rgba(48, 53, 56, 1), 10px 150px 0 0 rgba(28, 32, 34, 1),
  20px 150px 0 0 rgba(219, 222, 232, 1), 30px 150px 0 0 rgba(111, 114, 121, 1),
  40px 150px 0 0 rgba(28, 32, 34, 1), 50px 150px 0 0 rgba(48, 53, 56, 1),
  60px 150px 0 0 rgba(48, 53, 56, 1), 70px 150px 0 0 rgba(48, 53, 56, 1),
  80px 150px 0 0 rgba(48, 53, 56, 1), 90px 150px 0 0 rgba(48, 53, 56, 1),
  100px 150px 0 0 rgba(48, 53, 56, 1), 110px 150px 0 0 rgba(48, 53, 56, 1),
  120px 150px 0 0 rgba(48, 53, 56, 1), 130px 150px 0 0 rgba(48, 53, 56, 1),
  140px 150px 0 0 rgba(242, 245, 252, 1), 150px 150px 0 0 rgba(48, 53, 56, 1),
  160px 150px 0 0 rgba(48, 53, 56, 1), 170px 150px 0 0 rgba(48, 53, 56, 1),
  180px 150px 0 0 rgba(48, 53, 56, 1), 190px 150px 0 0 rgba(48, 53, 56, 1),
  200px 150px 0 0 rgba(48, 53, 56, 1), 210px 150px 0 0 rgba(48, 53, 56, 1),
  220px 150px 0 0 rgba(48, 53, 56, 1), 230px 150px 0 0 rgba(48, 53, 56, 1),
  240px 150px 0 0 rgba(48, 53, 56, 1), 250px 150px 0 0 rgba(48, 53, 56, 1),
  260px 150px 0 0 rgba(48, 53, 56, 1), 270px 150px 0 0 rgba(48, 53, 56, 1),
  280px 150px 0 0 rgba(48, 53, 56, 1), 290px 150px 0 0 rgba(48, 53, 56, 1),
  300px 150px 0 0 rgba(48, 53, 56, 1), 310px 150px 0 0 rgba(48, 53, 56, 1),
  320px 150px 0 0 rgba(48, 53, 56, 1), 330px 150px 0 0 rgba(48, 53, 56, 1),
  340px 150px 0 0 rgba(48, 53, 56, 1), 350px 150px 0 0 rgba(48, 53, 56, 1),
  360px 150px 0 0 rgba(48, 53, 56, 1), 370px 150px 0 0 rgba(48, 53, 56, 1),
  380px 150px 0 0 rgba(48, 53, 56, 1), 390px 150px 0 0 rgba(48, 53, 56, 1),
  400px 150px 0 0 rgba(48, 53, 56, 1), 410px 150px 0 0 rgba(48, 53, 56, 1),
  420px 150px 0 0 rgba(48, 53, 56, 1), 430px 150px 0 0 rgba(48, 53, 56, 1),
  440px 150px 0 0 rgba(48, 53, 56, 1), 450px 150px 0 0 rgba(48, 53, 56, 1),
  460px 150px 0 0 rgba(48, 53, 56, 1), 470px 150px 0 0 rgba(48, 53, 56, 1),
  480px 150px 0 0 rgba(48, 53, 56, 1), 490px 150px 0 0 rgba(48, 53, 56, 1),
  500px 150px 0 0 rgba(48, 53, 56, 1), 510px 150px 0 0 rgba(48, 53, 56, 1),
  520px 150px 0 0 rgba(48, 53, 56, 1), 530px 150px 0 0 rgba(48, 53, 56, 1),
  540px 150px 0 0 rgba(48, 53, 56, 1), 550px 150px 0 0 rgba(48, 53, 56, 1),
  560px 150px 0 0 rgba(48, 53, 56, 1), 570px 150px 0 0 rgba(48, 53, 56, 1),
  580px 150px 0 0 rgba(48, 53, 56, 1), 590px 150px 0 0 rgba(48, 53, 56, 1),
  600px 150px 0 0 rgba(48, 53, 56, 1), 610px 150px 0 0 rgba(48, 53, 56, 1),
  620px 150px 0 0 rgba(48, 53, 56, 1), 630px 150px 0 0 rgba(48, 53, 56, 1),
  640px 150px 0 0 rgba(48, 53, 56, 1), 650px 150px 0 0 rgba(48, 53, 56, 1),
  660px 150px 0 0 rgba(48, 53, 56, 1), 670px 150px 0 0 rgba(48, 53, 56, 1),
  680px 150px 0 0 rgba(48, 53, 56, 1), 690px 150px 0 0 rgba(48, 53, 56, 1),
  700px 150px 0 0 rgba(48, 53, 56, 1), 710px 150px 0 0 rgba(48, 53, 56, 1),
  720px 150px 0 0 rgba(48, 53, 56, 1), 730px 150px 0 0 rgba(48, 53, 56, 1),
  740px 150px 0 0 rgba(48, 53, 56, 1), 750px 150px 0 0 rgba(48, 53, 56, 1),
  760px 150px 0 0 rgba(242, 245, 252, 1), 770px 150px 0 0 rgba(48, 53, 56, 1),
  780px 150px 0 0 rgba(48, 53, 56, 1), 790px 150px 0 0 rgba(48, 53, 56, 1),
  800px 150px 0 0 rgba(48, 53, 56, 1), 810px 150px 0 0 rgba(48, 53, 56, 1),
  820px 150px 0 0 rgba(48, 53, 56, 1), 830px 150px 0 0 rgba(48, 53, 56, 1),
  840px 150px 0 0 rgba(48, 53, 56, 1), 850px 150px 0 0 rgba(48, 53, 56, 1),
  860px 150px 0 0 rgba(48, 53, 56, 1), 870px 150px 0 0 rgba(48, 53, 56, 1),
  880px 150px 0 0 rgba(48, 53, 56, 1), 890px 150px 0 0 rgba(48, 53, 56, 1),
  900px 150px 0 0 rgba(48, 53, 56, 1), 910px 150px 0 0 rgba(48, 53, 56, 1),
  920px 150px 0 0 rgba(48, 53, 56, 1), 930px 150px 0 0 rgba(48, 53, 56, 1),
  940px 150px 0 0 rgba(48, 53, 56, 1), 950px 150px 0 0 rgba(242, 245, 252, 1),
  960px 150px 0 0 rgba(48, 53, 56, 1), 970px 150px 0 0 rgba(48, 53, 56, 1),
  980px 150px 0 0 rgba(48, 53, 56, 1), 990px 150px 0 0 rgba(48, 53, 56, 1),
  1000px 150px 0 0 rgba(48, 53, 56, 1), 10px 160px 0 0 rgba(28, 32, 34, 1),
  20px 160px 0 0 rgba(219, 222, 232, 1), 30px 160px 0 0 rgba(111, 114, 121, 1),
  40px 160px 0 0 rgba(28, 32, 34, 1), 50px 160px 0 0 rgba(48, 53, 56, 1),
  60px 160px 0 0 rgba(48, 53, 56, 1), 70px 160px 0 0 rgba(48, 53, 56, 1),
  80px 160px 0 0 rgba(48, 53, 56, 1), 90px 160px 0 0 rgba(48, 53, 56, 1),
  100px 160px 0 0 rgba(48, 53, 56, 1), 110px 160px 0 0 rgba(48, 53, 56, 1),
  120px 160px 0 0 rgba(48, 53, 56, 1), 130px 160px 0 0 rgba(48, 53, 56, 1),
  140px 160px 0 0 rgba(242, 245, 252, 1), 150px 160px 0 0 rgba(48, 53, 56, 1),
  160px 160px 0 0 rgba(48, 53, 56, 1), 170px 160px 0 0 rgba(48, 53, 56, 1),
  180px 160px 0 0 rgba(48, 53, 56, 1), 190px 160px 0 0 rgba(48, 53, 56, 1),
  200px 160px 0 0 rgba(48, 53, 56, 1), 210px 160px 0 0 rgba(48, 53, 56, 1),
  220px 160px 0 0 rgba(48, 53, 56, 1), 230px 160px 0 0 rgba(48, 53, 56, 1),
  240px 160px 0 0 rgba(48, 53, 56, 1), 250px 160px 0 0 rgba(48, 53, 56, 1),
  260px 160px 0 0 rgba(48, 53, 56, 1), 270px 160px 0 0 rgba(48, 53, 56, 1),
  280px 160px 0 0 rgba(48, 53, 56, 1), 290px 160px 0 0 rgba(48, 53, 56, 1),
  300px 160px 0 0 rgba(48, 53, 56, 1), 310px 160px 0 0 rgba(48, 53, 56, 1),
  320px 160px 0 0 rgba(48, 53, 56, 1), 330px 160px 0 0 rgba(48, 53, 56, 1),
  340px 160px 0 0 rgba(48, 53, 56, 1), 350px 160px 0 0 rgba(48, 53, 56, 1),
  360px 160px 0 0 rgba(48, 53, 56, 1), 370px 160px 0 0 rgba(48, 53, 56, 1),
  380px 160px 0 0 rgba(48, 53, 56, 1), 390px 160px 0 0 rgba(48, 53, 56, 1),
  400px 160px 0 0 rgba(48, 53, 56, 1), 410px 160px 0 0 rgba(48, 53, 56, 1),
  420px 160px 0 0 rgba(48, 53, 56, 1), 430px 160px 0 0 rgba(48, 53, 56, 1),
  440px 160px 0 0 rgba(48, 53, 56, 1), 450px 160px 0 0 rgba(48, 53, 56, 1),
  460px 160px 0 0 rgba(48, 53, 56, 1), 470px 160px 0 0 rgba(48, 53, 56, 1),
  480px 160px 0 0 rgba(48, 53, 56, 1), 490px 160px 0 0 rgba(48, 53, 56, 1),
  500px 160px 0 0 rgba(48, 53, 56, 1), 510px 160px 0 0 rgba(48, 53, 56, 1),
  520px 160px 0 0 rgba(48, 53, 56, 1), 530px 160px 0 0 rgba(48, 53, 56, 1),
  540px 160px 0 0 rgba(48, 53, 56, 1), 550px 160px 0 0 rgba(48, 53, 56, 1),
  560px 160px 0 0 rgba(48, 53, 56, 1), 570px 160px 0 0 rgba(48, 53, 56, 1),
  580px 160px 0 0 rgba(48, 53, 56, 1), 590px 160px 0 0 rgba(48, 53, 56, 1),
  600px 160px 0 0 rgba(48, 53, 56, 1), 610px 160px 0 0 rgba(48, 53, 56, 1),
  620px 160px 0 0 rgba(48, 53, 56, 1), 630px 160px 0 0 rgba(48, 53, 56, 1),
  640px 160px 0 0 rgba(48, 53, 56, 1), 650px 160px 0 0 rgba(48, 53, 56, 1),
  660px 160px 0 0 rgba(48, 53, 56, 1), 670px 160px 0 0 rgba(48, 53, 56, 1),
  680px 160px 0 0 rgba(48, 53, 56, 1), 690px 160px 0 0 rgba(48, 53, 56, 1),
  700px 160px 0 0 rgba(48, 53, 56, 1), 710px 160px 0 0 rgba(48, 53, 56, 1),
  720px 160px 0 0 rgba(48, 53, 56, 1), 730px 160px 0 0 rgba(48, 53, 56, 1),
  740px 160px 0 0 rgba(48, 53, 56, 1), 750px 160px 0 0 rgba(48, 53, 56, 1),
  760px 160px 0 0 rgba(242, 245, 252, 1), 770px 160px 0 0 rgba(48, 53, 56, 1),
  780px 160px 0 0 rgba(48, 53, 56, 1), 790px 160px 0 0 rgba(48, 53, 56, 1),
  800px 160px 0 0 rgba(48, 53, 56, 1), 810px 160px 0 0 rgba(48, 53, 56, 1),
  820px 160px 0 0 rgba(48, 53, 56, 1), 830px 160px 0 0 rgba(48, 53, 56, 1),
  840px 160px 0 0 rgba(48, 53, 56, 1), 850px 160px 0 0 rgba(48, 53, 56, 1),
  860px 160px 0 0 rgba(48, 53, 56, 1), 870px 160px 0 0 rgba(48, 53, 56, 1),
  880px 160px 0 0 rgba(48, 53, 56, 1), 890px 160px 0 0 rgba(48, 53, 56, 1),
  900px 160px 0 0 rgba(48, 53, 56, 1), 910px 160px 0 0 rgba(48, 53, 56, 1),
  920px 160px 0 0 rgba(48, 53, 56, 1), 930px 160px 0 0 rgba(48, 53, 56, 1),
  940px 160px 0 0 rgba(242, 245, 252, 1), 950px 160px 0 0 rgba(48, 53, 56, 1),
  960px 160px 0 0 rgba(48, 53, 56, 1), 970px 160px 0 0 rgba(48, 53, 56, 1),
  980px 160px 0 0 rgba(48, 53, 56, 1), 990px 160px 0 0 rgba(48, 53, 56, 1),
  1000px 160px 0 0 rgba(48, 53, 56, 1), 10px 170px 0 0 rgba(28, 32, 34, 1),
  20px 170px 0 0 rgba(219, 222, 232, 1), 30px 170px 0 0 rgba(111, 114, 121, 1),
  40px 170px 0 0 rgba(28, 32, 34, 1), 50px 170px 0 0 rgba(48, 53, 56, 1),
  60px 170px 0 0 rgba(48, 53, 56, 1), 70px 170px 0 0 rgba(48, 53, 56, 1),
  80px 170px 0 0 rgba(48, 53, 56, 1), 90px 170px 0 0 rgba(48, 53, 56, 1),
  100px 170px 0 0 rgba(48, 53, 56, 1), 110px 170px 0 0 rgba(48, 53, 56, 1),
  120px 170px 0 0 rgba(48, 53, 56, 1), 130px 170px 0 0 rgba(48, 53, 56, 1),
  140px 170px 0 0 rgba(48, 53, 56, 1), 150px 170px 0 0 rgba(48, 53, 56, 1),
  160px 170px 0 0 rgba(48, 53, 56, 1), 170px 170px 0 0 rgba(48, 53, 56, 1),
  180px 170px 0 0 rgba(48, 53, 56, 1), 190px 170px 0 0 rgba(48, 53, 56, 1),
  200px 170px 0 0 rgba(48, 53, 56, 1), 210px 170px 0 0 rgba(48, 53, 56, 1),
  220px 170px 0 0 rgba(48, 53, 56, 1), 230px 170px 0 0 rgba(48, 53, 56, 1),
  240px 170px 0 0 rgba(48, 53, 56, 1), 250px 170px 0 0 rgba(48, 53, 56, 1),
  260px 170px 0 0 rgba(48, 53, 56, 1), 270px 170px 0 0 rgba(48, 53, 56, 1),
  280px 170px 0 0 rgba(48, 53, 56, 1), 290px 170px 0 0 rgba(48, 53, 56, 1),
  300px 170px 0 0 rgba(48, 53, 56, 1), 310px 170px 0 0 rgba(48, 53, 56, 1),
  320px 170px 0 0 rgba(48, 53, 56, 1), 330px 170px 0 0 rgba(48, 53, 56, 1),
  340px 170px 0 0 rgba(48, 53, 56, 1), 350px 170px 0 0 rgba(48, 53, 56, 1),
  360px 170px 0 0 rgba(48, 53, 56, 1), 370px 170px 0 0 rgba(48, 53, 56, 1),
  380px 170px 0 0 rgba(48, 53, 56, 1), 390px 170px 0 0 rgba(48, 53, 56, 1),
  400px 170px 0 0 rgba(48, 53, 56, 1), 410px 170px 0 0 rgba(48, 53, 56, 1),
  420px 170px 0 0 rgba(48, 53, 56, 1), 430px 170px 0 0 rgba(48, 53, 56, 1),
  440px 170px 0 0 rgba(48, 53, 56, 1), 450px 170px 0 0 rgba(48, 53, 56, 1),
  460px 170px 0 0 rgba(48, 53, 56, 1), 470px 170px 0 0 rgba(48, 53, 56, 1),
  480px 170px 0 0 rgba(48, 53, 56, 1), 490px 170px 0 0 rgba(48, 53, 56, 1),
  500px 170px 0 0 rgba(48, 53, 56, 1), 510px 170px 0 0 rgba(48, 53, 56, 1),
  520px 170px 0 0 rgba(48, 53, 56, 1), 530px 170px 0 0 rgba(48, 53, 56, 1),
  540px 170px 0 0 rgba(48, 53, 56, 1), 550px 170px 0 0 rgba(48, 53, 56, 1),
  560px 170px 0 0 rgba(48, 53, 56, 1), 570px 170px 0 0 rgba(48, 53, 56, 1),
  580px 170px 0 0 rgba(48, 53, 56, 1), 590px 170px 0 0 rgba(48, 53, 56, 1),
  600px 170px 0 0 rgba(48, 53, 56, 1), 610px 170px 0 0 rgba(48, 53, 56, 1),
  620px 170px 0 0 rgba(48, 53, 56, 1), 630px 170px 0 0 rgba(48, 53, 56, 1),
  640px 170px 0 0 rgba(48, 53, 56, 1), 650px 170px 0 0 rgba(48, 53, 56, 1),
  660px 170px 0 0 rgba(48, 53, 56, 1), 670px 170px 0 0 rgba(48, 53, 56, 1),
  680px 170px 0 0 rgba(48, 53, 56, 1), 690px 170px 0 0 rgba(48, 53, 56, 1),
  700px 170px 0 0 rgba(48, 53, 56, 1), 710px 170px 0 0 rgba(48, 53, 56, 1),
  720px 170px 0 0 rgba(48, 53, 56, 1), 730px 170px 0 0 rgba(48, 53, 56, 1),
  740px 170px 0 0 rgba(48, 53, 56, 1), 750px 170px 0 0 rgba(48, 53, 56, 1),
  760px 170px 0 0 rgba(48, 53, 56, 1), 770px 170px 0 0 rgba(48, 53, 56, 1),
  780px 170px 0 0 rgba(48, 53, 56, 1), 790px 170px 0 0 rgba(48, 53, 56, 1),
  800px 170px 0 0 rgba(48, 53, 56, 1), 810px 170px 0 0 rgba(48, 53, 56, 1),
  820px 170px 0 0 rgba(48, 53, 56, 1), 830px 170px 0 0 rgba(48, 53, 56, 1),
  840px 170px 0 0 rgba(48, 53, 56, 1), 850px 170px 0 0 rgba(48, 53, 56, 1),
  860px 170px 0 0 rgba(48, 53, 56, 1), 870px 170px 0 0 rgba(48, 53, 56, 1),
  880px 170px 0 0 rgba(48, 53, 56, 1), 890px 170px 0 0 rgba(48, 53, 56, 1),
  900px 170px 0 0 rgba(48, 53, 56, 1), 910px 170px 0 0 rgba(48, 53, 56, 1),
  920px 170px 0 0 rgba(48, 53, 56, 1), 930px 170px 0 0 rgba(242, 245, 252, 1),
  940px 170px 0 0 rgba(48, 53, 56, 1), 950px 170px 0 0 rgba(48, 53, 56, 1),
  960px 170px 0 0 rgba(48, 53, 56, 1), 970px 170px 0 0 rgba(48, 53, 56, 1),
  980px 170px 0 0 rgba(48, 53, 56, 1), 990px 170px 0 0 rgba(48, 53, 56, 1),
  1000px 170px 0 0 rgba(48, 53, 56, 1), 10px 180px 0 0 rgba(28, 32, 34, 1),
  20px 180px 0 0 rgba(219, 222, 232, 1), 30px 180px 0 0 rgba(111, 114, 121, 1),
  40px 180px 0 0 rgba(28, 32, 34, 1), 50px 180px 0 0 rgba(48, 53, 56, 1),
  60px 180px 0 0 rgba(48, 53, 56, 1), 70px 180px 0 0 rgba(48, 53, 56, 1),
  80px 180px 0 0 rgba(48, 53, 56, 1), 90px 180px 0 0 rgba(48, 53, 56, 1),
  100px 180px 0 0 rgba(48, 53, 56, 1), 110px 180px 0 0 rgba(48, 53, 56, 1),
  120px 180px 0 0 rgba(48, 53, 56, 1), 130px 180px 0 0 rgba(48, 53, 56, 1),
  140px 180px 0 0 rgba(242, 245, 252, 1), 150px 180px 0 0 rgba(48, 53, 56, 1),
  160px 180px 0 0 rgba(48, 53, 56, 1), 170px 180px 0 0 rgba(48, 53, 56, 1),
  180px 180px 0 0 rgba(48, 53, 56, 1), 190px 180px 0 0 rgba(48, 53, 56, 1),
  200px 180px 0 0 rgba(48, 53, 56, 1), 210px 180px 0 0 rgba(48, 53, 56, 1),
  220px 180px 0 0 rgba(48, 53, 56, 1), 230px 180px 0 0 rgba(48, 53, 56, 1),
  240px 180px 0 0 rgba(48, 53, 56, 1), 250px 180px 0 0 rgba(48, 53, 56, 1),
  260px 180px 0 0 rgba(48, 53, 56, 1), 270px 180px 0 0 rgba(48, 53, 56, 1),
  280px 180px 0 0 rgba(48, 53, 56, 1), 290px 180px 0 0 rgba(48, 53, 56, 1),
  300px 180px 0 0 rgba(48, 53, 56, 1), 310px 180px 0 0 rgba(48, 53, 56, 1),
  320px 180px 0 0 rgba(48, 53, 56, 1), 330px 180px 0 0 rgba(48, 53, 56, 1),
  340px 180px 0 0 rgba(48, 53, 56, 1), 350px 180px 0 0 rgba(48, 53, 56, 1),
  360px 180px 0 0 rgba(48, 53, 56, 1), 370px 180px 0 0 rgba(48, 53, 56, 1),
  380px 180px 0 0 rgba(48, 53, 56, 1), 390px 180px 0 0 rgba(48, 53, 56, 1),
  400px 180px 0 0 rgba(48, 53, 56, 1), 410px 180px 0 0 rgba(48, 53, 56, 1),
  420px 180px 0 0 rgba(48, 53, 56, 1), 430px 180px 0 0 rgba(48, 53, 56, 1),
  440px 180px 0 0 rgba(48, 53, 56, 1), 450px 180px 0 0 rgba(48, 53, 56, 1),
  460px 180px 0 0 rgba(48, 53, 56, 1), 470px 180px 0 0 rgba(48, 53, 56, 1),
  480px 180px 0 0 rgba(48, 53, 56, 1), 490px 180px 0 0 rgba(48, 53, 56, 1),
  500px 180px 0 0 rgba(48, 53, 56, 1), 510px 180px 0 0 rgba(48, 53, 56, 1),
  520px 180px 0 0 rgba(48, 53, 56, 1), 530px 180px 0 0 rgba(48, 53, 56, 1),
  540px 180px 0 0 rgba(48, 53, 56, 1), 550px 180px 0 0 rgba(48, 53, 56, 1),
  560px 180px 0 0 rgba(48, 53, 56, 1), 570px 180px 0 0 rgba(48, 53, 56, 1),
  580px 180px 0 0 rgba(48, 53, 56, 1), 590px 180px 0 0 rgba(48, 53, 56, 1),
  600px 180px 0 0 rgba(48, 53, 56, 1), 610px 180px 0 0 rgba(48, 53, 56, 1),
  620px 180px 0 0 rgba(48, 53, 56, 1), 630px 180px 0 0 rgba(48, 53, 56, 1),
  640px 180px 0 0 rgba(48, 53, 56, 1), 650px 180px 0 0 rgba(48, 53, 56, 1),
  660px 180px 0 0 rgba(48, 53, 56, 1), 670px 180px 0 0 rgba(48, 53, 56, 1),
  680px 180px 0 0 rgba(48, 53, 56, 1), 690px 180px 0 0 rgba(48, 53, 56, 1),
  700px 180px 0 0 rgba(48, 53, 56, 1), 710px 180px 0 0 rgba(48, 53, 56, 1),
  720px 180px 0 0 rgba(48, 53, 56, 1), 730px 180px 0 0 rgba(48, 53, 56, 1),
  740px 180px 0 0 rgba(48, 53, 56, 1), 750px 180px 0 0 rgba(48, 53, 56, 1),
  760px 180px 0 0 rgba(242, 245, 252, 1), 770px 180px 0 0 rgba(48, 53, 56, 1),
  780px 180px 0 0 rgba(48, 53, 56, 1), 790px 180px 0 0 rgba(48, 53, 56, 1),
  800px 180px 0 0 rgba(48, 53, 56, 1), 810px 180px 0 0 rgba(48, 53, 56, 1),
  820px 180px 0 0 rgba(48, 53, 56, 1), 830px 180px 0 0 rgba(48, 53, 56, 1),
  840px 180px 0 0 rgba(48, 53, 56, 1), 850px 180px 0 0 rgba(48, 53, 56, 1),
  860px 180px 0 0 rgba(48, 53, 56, 1), 870px 180px 0 0 rgba(48, 53, 56, 1),
  880px 180px 0 0 rgba(48, 53, 56, 1), 890px 180px 0 0 rgba(48, 53, 56, 1),
  900px 180px 0 0 rgba(48, 53, 56, 1), 910px 180px 0 0 rgba(48, 53, 56, 1),
  920px 180px 0 0 rgba(242, 245, 252, 1), 930px 180px 0 0 rgba(48, 53, 56, 1),
  940px 180px 0 0 rgba(48, 53, 56, 1), 950px 180px 0 0 rgba(48, 53, 56, 1),
  960px 180px 0 0 rgba(48, 53, 56, 1), 970px 180px 0 0 rgba(48, 53, 56, 1),
  980px 180px 0 0 rgba(48, 53, 56, 1), 990px 180px 0 0 rgba(48, 53, 56, 1),
  1000px 180px 0 0 rgba(48, 53, 56, 1), 10px 190px 0 0 rgba(28, 32, 34, 1),
  20px 190px 0 0 rgba(219, 222, 232, 1), 30px 190px 0 0 rgba(111, 114, 121, 1),
  40px 190px 0 0 rgba(28, 32, 34, 1), 50px 190px 0 0 rgba(48, 53, 56, 1),
  60px 190px 0 0 rgba(48, 53, 56, 1), 70px 190px 0 0 rgba(48, 53, 56, 1),
  80px 190px 0 0 rgba(48, 53, 56, 1), 90px 190px 0 0 rgba(48, 53, 56, 1),
  100px 190px 0 0 rgba(48, 53, 56, 1), 110px 190px 0 0 rgba(48, 53, 56, 1),
  120px 190px 0 0 rgba(48, 53, 56, 1), 130px 190px 0 0 rgba(48, 53, 56, 1),
  140px 190px 0 0 rgba(242, 245, 252, 1), 150px 190px 0 0 rgba(48, 53, 56, 1),
  160px 190px 0 0 rgba(48, 53, 56, 1), 170px 190px 0 0 rgba(48, 53, 56, 1),
  180px 190px 0 0 rgba(48, 53, 56, 1), 190px 190px 0 0 rgba(48, 53, 56, 1),
  200px 190px 0 0 rgba(48, 53, 56, 1), 210px 190px 0 0 rgba(48, 53, 56, 1),
  220px 190px 0 0 rgba(48, 53, 56, 1), 230px 190px 0 0 rgba(48, 53, 56, 1),
  240px 190px 0 0 rgba(48, 53, 56, 1), 250px 190px 0 0 rgba(48, 53, 56, 1),
  260px 190px 0 0 rgba(48, 53, 56, 1), 270px 190px 0 0 rgba(48, 53, 56, 1),
  280px 190px 0 0 rgba(48, 53, 56, 1), 290px 190px 0 0 rgba(48, 53, 56, 1),
  300px 190px 0 0 rgba(48, 53, 56, 1), 310px 190px 0 0 rgba(48, 53, 56, 1),
  320px 190px 0 0 rgba(48, 53, 56, 1), 330px 190px 0 0 rgba(48, 53, 56, 1),
  340px 190px 0 0 rgba(48, 53, 56, 1), 350px 190px 0 0 rgba(48, 53, 56, 1),
  360px 190px 0 0 rgba(48, 53, 56, 1), 370px 190px 0 0 rgba(48, 53, 56, 1),
  380px 190px 0 0 rgba(48, 53, 56, 1), 390px 190px 0 0 rgba(48, 53, 56, 1),
  400px 190px 0 0 rgba(48, 53, 56, 1), 410px 190px 0 0 rgba(48, 53, 56, 1),
  420px 190px 0 0 rgba(48, 53, 56, 1), 430px 190px 0 0 rgba(48, 53, 56, 1),
  440px 190px 0 0 rgba(48, 53, 56, 1), 450px 190px 0 0 rgba(48, 53, 56, 1),
  460px 190px 0 0 rgba(48, 53, 56, 1), 470px 190px 0 0 rgba(48, 53, 56, 1),
  480px 190px 0 0 rgba(48, 53, 56, 1), 490px 190px 0 0 rgba(48, 53, 56, 1),
  500px 190px 0 0 rgba(48, 53, 56, 1), 510px 190px 0 0 rgba(48, 53, 56, 1),
  520px 190px 0 0 rgba(48, 53, 56, 1), 530px 190px 0 0 rgba(48, 53, 56, 1),
  540px 190px 0 0 rgba(48, 53, 56, 1), 550px 190px 0 0 rgba(48, 53, 56, 1),
  560px 190px 0 0 rgba(48, 53, 56, 1), 570px 190px 0 0 rgba(48, 53, 56, 1),
  580px 190px 0 0 rgba(48, 53, 56, 1), 590px 190px 0 0 rgba(48, 53, 56, 1),
  600px 190px 0 0 rgba(48, 53, 56, 1), 610px 190px 0 0 rgba(48, 53, 56, 1),
  620px 190px 0 0 rgba(48, 53, 56, 1), 630px 190px 0 0 rgba(48, 53, 56, 1),
  640px 190px 0 0 rgba(48, 53, 56, 1), 650px 190px 0 0 rgba(48, 53, 56, 1),
  660px 190px 0 0 rgba(48, 53, 56, 1), 670px 190px 0 0 rgba(48, 53, 56, 1),
  680px 190px 0 0 rgba(48, 53, 56, 1), 690px 190px 0 0 rgba(48, 53, 56, 1),
  700px 190px 0 0 rgba(48, 53, 56, 1), 710px 190px 0 0 rgba(48, 53, 56, 1),
  720px 190px 0 0 rgba(48, 53, 56, 1), 730px 190px 0 0 rgba(48, 53, 56, 1),
  740px 190px 0 0 rgba(48, 53, 56, 1), 750px 190px 0 0 rgba(48, 53, 56, 1),
  760px 190px 0 0 rgba(242, 245, 252, 1), 770px 190px 0 0 rgba(48, 53, 56, 1),
  780px 190px 0 0 rgba(48, 53, 56, 1), 790px 190px 0 0 rgba(48, 53, 56, 1),
  800px 190px 0 0 rgba(48, 53, 56, 1), 810px 190px 0 0 rgba(48, 53, 56, 1),
  820px 190px 0 0 rgba(48, 53, 56, 1), 830px 190px 0 0 rgba(48, 53, 56, 1),
  840px 190px 0 0 rgba(48, 53, 56, 1), 850px 190px 0 0 rgba(48, 53, 56, 1),
  860px 190px 0 0 rgba(48, 53, 56, 1), 870px 190px 0 0 rgba(48, 53, 56, 1),
  880px 190px 0 0 rgba(48, 53, 56, 1), 890px 190px 0 0 rgba(48, 53, 56, 1),
  900px 190px 0 0 rgba(48, 53, 56, 1), 910px 190px 0 0 rgba(242, 245, 252, 1),
  920px 190px 0 0 rgba(48, 53, 56, 1), 930px 190px 0 0 rgba(48, 53, 56, 1),
  940px 190px 0 0 rgba(48, 53, 56, 1), 950px 190px 0 0 rgba(48, 53, 56, 1),
  960px 190px 0 0 rgba(48, 53, 56, 1), 970px 190px 0 0 rgba(48, 53, 56, 1),
  980px 190px 0 0 rgba(48, 53, 56, 1), 990px 190px 0 0 rgba(48, 53, 56, 1),
  1000px 190px 0 0 rgba(48, 53, 56, 1), 10px 200px 0 0 rgba(28, 32, 34, 1),
  20px 200px 0 0 rgba(219, 222, 232, 1), 30px 200px 0 0 rgba(111, 114, 121, 1),
  40px 200px 0 0 rgba(28, 32, 34, 1), 50px 200px 0 0 rgba(48, 53, 56, 1),
  60px 200px 0 0 rgba(48, 53, 56, 1), 70px 200px 0 0 rgba(48, 53, 56, 1),
  80px 200px 0 0 rgba(48, 53, 56, 1), 90px 200px 0 0 rgba(48, 53, 56, 1),
  100px 200px 0 0 rgba(48, 53, 56, 1), 110px 200px 0 0 rgba(48, 53, 56, 1),
  120px 200px 0 0 rgba(48, 53, 56, 1), 130px 200px 0 0 rgba(48, 53, 56, 1),
  140px 200px 0 0 rgba(242, 245, 252, 1), 150px 200px 0 0 rgba(48, 53, 56, 1),
  160px 200px 0 0 rgba(48, 53, 56, 1), 170px 200px 0 0 rgba(48, 53, 56, 1),
  180px 200px 0 0 rgba(48, 53, 56, 1), 190px 200px 0 0 rgba(48, 53, 56, 1),
  200px 200px 0 0 rgba(48, 53, 56, 1), 210px 200px 0 0 rgba(48, 53, 56, 1),
  220px 200px 0 0 rgba(48, 53, 56, 1), 230px 200px 0 0 rgba(48, 53, 56, 1),
  240px 200px 0 0 rgba(48, 53, 56, 1), 250px 200px 0 0 rgba(48, 53, 56, 1),
  260px 200px 0 0 rgba(48, 53, 56, 1), 270px 200px 0 0 rgba(48, 53, 56, 1),
  280px 200px 0 0 rgba(48, 53, 56, 1), 290px 200px 0 0 rgba(48, 53, 56, 1),
  300px 200px 0 0 rgba(48, 53, 56, 1), 310px 200px 0 0 rgba(48, 53, 56, 1),
  320px 200px 0 0 rgba(48, 53, 56, 1), 330px 200px 0 0 rgba(48, 53, 56, 1),
  340px 200px 0 0 rgba(48, 53, 56, 1), 350px 200px 0 0 rgba(48, 53, 56, 1),
  360px 200px 0 0 rgba(48, 53, 56, 1), 370px 200px 0 0 rgba(48, 53, 56, 1),
  380px 200px 0 0 rgba(48, 53, 56, 1), 390px 200px 0 0 rgba(48, 53, 56, 1),
  400px 200px 0 0 rgba(48, 53, 56, 1), 410px 200px 0 0 rgba(48, 53, 56, 1),
  420px 200px 0 0 rgba(48, 53, 56, 1), 430px 200px 0 0 rgba(48, 53, 56, 1),
  440px 200px 0 0 rgba(48, 53, 56, 1), 450px 200px 0 0 rgba(48, 53, 56, 1),
  460px 200px 0 0 rgba(48, 53, 56, 1), 470px 200px 0 0 rgba(48, 53, 56, 1),
  480px 200px 0 0 rgba(48, 53, 56, 1), 490px 200px 0 0 rgba(48, 53, 56, 1),
  500px 200px 0 0 rgba(48, 53, 56, 1), 510px 200px 0 0 rgba(48, 53, 56, 1),
  520px 200px 0 0 rgba(48, 53, 56, 1), 530px 200px 0 0 rgba(48, 53, 56, 1),
  540px 200px 0 0 rgba(48, 53, 56, 1), 550px 200px 0 0 rgba(48, 53, 56, 1),
  560px 200px 0 0 rgba(48, 53, 56, 1), 570px 200px 0 0 rgba(48, 53, 56, 1),
  580px 200px 0 0 rgba(48, 53, 56, 1), 590px 200px 0 0 rgba(48, 53, 56, 1),
  600px 200px 0 0 rgba(48, 53, 56, 1), 610px 200px 0 0 rgba(48, 53, 56, 1),
  620px 200px 0 0 rgba(48, 53, 56, 1), 630px 200px 0 0 rgba(48, 53, 56, 1),
  640px 200px 0 0 rgba(48, 53, 56, 1), 650px 200px 0 0 rgba(48, 53, 56, 1),
  660px 200px 0 0 rgba(48, 53, 56, 1), 670px 200px 0 0 rgba(48, 53, 56, 1),
  680px 200px 0 0 rgba(48, 53, 56, 1), 690px 200px 0 0 rgba(48, 53, 56, 1),
  700px 200px 0 0 rgba(48, 53, 56, 1), 710px 200px 0 0 rgba(48, 53, 56, 1),
  720px 200px 0 0 rgba(48, 53, 56, 1), 730px 200px 0 0 rgba(48, 53, 56, 1),
  740px 200px 0 0 rgba(48, 53, 56, 1), 750px 200px 0 0 rgba(48, 53, 56, 1),
  760px 200px 0 0 rgba(242, 245, 252, 1), 770px 200px 0 0 rgba(48, 53, 56, 1),
  780px 200px 0 0 rgba(48, 53, 56, 1), 790px 200px 0 0 rgba(48, 53, 56, 1),
  800px 200px 0 0 rgba(48, 53, 56, 1), 810px 200px 0 0 rgba(48, 53, 56, 1),
  820px 200px 0 0 rgba(48, 53, 56, 1), 830px 200px 0 0 rgba(48, 53, 56, 1),
  840px 200px 0 0 rgba(48, 53, 56, 1), 850px 200px 0 0 rgba(48, 53, 56, 1),
  860px 200px 0 0 rgba(48, 53, 56, 1), 870px 200px 0 0 rgba(48, 53, 56, 1),
  880px 200px 0 0 rgba(48, 53, 56, 1), 890px 200px 0 0 rgba(48, 53, 56, 1),
  900px 200px 0 0 rgba(242, 245, 252, 1), 910px 200px 0 0 rgba(48, 53, 56, 1),
  920px 200px 0 0 rgba(48, 53, 56, 1), 930px 200px 0 0 rgba(48, 53, 56, 1),
  940px 200px 0 0 rgba(48, 53, 56, 1), 950px 200px 0 0 rgba(48, 53, 56, 1),
  960px 200px 0 0 rgba(48, 53, 56, 1), 970px 200px 0 0 rgba(48, 53, 56, 1),
  980px 200px 0 0 rgba(48, 53, 56, 1), 990px 200px 0 0 rgba(48, 53, 56, 1),
  1000px 200px 0 0 rgba(48, 53, 56, 1), 10px 210px 0 0 rgba(28, 32, 34, 1),
  20px 210px 0 0 rgba(219, 222, 232, 1), 30px 210px 0 0 rgba(111, 114, 121, 1),
  40px 210px 0 0 rgba(28, 32, 34, 1), 50px 210px 0 0 rgba(48, 53, 56, 1),
  60px 210px 0 0 rgba(48, 53, 56, 1), 70px 210px 0 0 rgba(48, 53, 56, 1),
  80px 210px 0 0 rgba(48, 53, 56, 1), 90px 210px 0 0 rgba(48, 53, 56, 1),
  100px 210px 0 0 rgba(48, 53, 56, 1), 110px 210px 0 0 rgba(48, 53, 56, 1),
  120px 210px 0 0 rgba(48, 53, 56, 1), 130px 210px 0 0 rgba(48, 53, 56, 1),
  140px 210px 0 0 rgba(242, 245, 252, 1), 150px 210px 0 0 rgba(48, 53, 56, 1),
  160px 210px 0 0 rgba(48, 53, 56, 1), 170px 210px 0 0 rgba(48, 53, 56, 1),
  180px 210px 0 0 rgba(48, 53, 56, 1), 190px 210px 0 0 rgba(48, 53, 56, 1),
  200px 210px 0 0 rgba(48, 53, 56, 1), 210px 210px 0 0 rgba(48, 53, 56, 1),
  220px 210px 0 0 rgba(48, 53, 56, 1), 230px 210px 0 0 rgba(48, 53, 56, 1),
  240px 210px 0 0 rgba(48, 53, 56, 1), 250px 210px 0 0 rgba(48, 53, 56, 1),
  260px 210px 0 0 rgba(48, 53, 56, 1), 270px 210px 0 0 rgba(48, 53, 56, 1),
  280px 210px 0 0 rgba(48, 53, 56, 1), 290px 210px 0 0 rgba(48, 53, 56, 1),
  300px 210px 0 0 rgba(48, 53, 56, 1), 310px 210px 0 0 rgba(48, 53, 56, 1),
  320px 210px 0 0 rgba(48, 53, 56, 1), 330px 210px 0 0 rgba(48, 53, 56, 1),
  340px 210px 0 0 rgba(48, 53, 56, 1), 350px 210px 0 0 rgba(48, 53, 56, 1),
  360px 210px 0 0 rgba(48, 53, 56, 1), 370px 210px 0 0 rgba(48, 53, 56, 1),
  380px 210px 0 0 rgba(48, 53, 56, 1), 390px 210px 0 0 rgba(48, 53, 56, 1),
  400px 210px 0 0 rgba(48, 53, 56, 1), 410px 210px 0 0 rgba(48, 53, 56, 1),
  420px 210px 0 0 rgba(48, 53, 56, 1), 430px 210px 0 0 rgba(48, 53, 56, 1),
  440px 210px 0 0 rgba(48, 53, 56, 1), 450px 210px 0 0 rgba(48, 53, 56, 1),
  460px 210px 0 0 rgba(48, 53, 56, 1), 470px 210px 0 0 rgba(48, 53, 56, 1),
  480px 210px 0 0 rgba(48, 53, 56, 1), 490px 210px 0 0 rgba(48, 53, 56, 1),
  500px 210px 0 0 rgba(48, 53, 56, 1), 510px 210px 0 0 rgba(48, 53, 56, 1),
  520px 210px 0 0 rgba(48, 53, 56, 1), 530px 210px 0 0 rgba(48, 53, 56, 1),
  540px 210px 0 0 rgba(48, 53, 56, 1), 550px 210px 0 0 rgba(48, 53, 56, 1),
  560px 210px 0 0 rgba(48, 53, 56, 1), 570px 210px 0 0 rgba(48, 53, 56, 1),
  580px 210px 0 0 rgba(48, 53, 56, 1), 590px 210px 0 0 rgba(48, 53, 56, 1),
  600px 210px 0 0 rgba(48, 53, 56, 1), 610px 210px 0 0 rgba(48, 53, 56, 1),
  620px 210px 0 0 rgba(48, 53, 56, 1), 630px 210px 0 0 rgba(48, 53, 56, 1),
  640px 210px 0 0 rgba(48, 53, 56, 1), 650px 210px 0 0 rgba(48, 53, 56, 1),
  660px 210px 0 0 rgba(48, 53, 56, 1), 670px 210px 0 0 rgba(48, 53, 56, 1),
  680px 210px 0 0 rgba(48, 53, 56, 1), 690px 210px 0 0 rgba(48, 53, 56, 1),
  700px 210px 0 0 rgba(48, 53, 56, 1), 710px 210px 0 0 rgba(48, 53, 56, 1),
  720px 210px 0 0 rgba(48, 53, 56, 1), 730px 210px 0 0 rgba(48, 53, 56, 1),
  740px 210px 0 0 rgba(48, 53, 56, 1), 750px 210px 0 0 rgba(48, 53, 56, 1),
  760px 210px 0 0 rgba(242, 245, 252, 1), 770px 210px 0 0 rgba(48, 53, 56, 1),
  780px 210px 0 0 rgba(48, 53, 56, 1), 790px 210px 0 0 rgba(48, 53, 56, 1),
  800px 210px 0 0 rgba(48, 53, 56, 1), 810px 210px 0 0 rgba(48, 53, 56, 1),
  820px 210px 0 0 rgba(48, 53, 56, 1), 830px 210px 0 0 rgba(48, 53, 56, 1),
  840px 210px 0 0 rgba(48, 53, 56, 1), 850px 210px 0 0 rgba(48, 53, 56, 1),
  860px 210px 0 0 rgba(48, 53, 56, 1), 870px 210px 0 0 rgba(48, 53, 56, 1),
  880px 210px 0 0 rgba(48, 53, 56, 1), 890px 210px 0 0 rgba(242, 245, 252, 1),
  900px 210px 0 0 rgba(48, 53, 56, 1), 910px 210px 0 0 rgba(48, 53, 56, 1),
  920px 210px 0 0 rgba(48, 53, 56, 1), 930px 210px 0 0 rgba(48, 53, 56, 1),
  940px 210px 0 0 rgba(48, 53, 56, 1), 950px 210px 0 0 rgba(48, 53, 56, 1),
  960px 210px 0 0 rgba(48, 53, 56, 1), 970px 210px 0 0 rgba(48, 53, 56, 1),
  980px 210px 0 0 rgba(48, 53, 56, 1), 990px 210px 0 0 rgba(48, 53, 56, 1),
  1000px 210px 0 0 rgba(242, 245, 252, 1), 10px 220px 0 0 rgba(28, 32, 34, 1),
  20px 220px 0 0 rgba(219, 222, 232, 1), 30px 220px 0 0 rgba(111, 114, 121, 1),
  40px 220px 0 0 rgba(28, 32, 34, 1), 50px 220px 0 0 rgba(48, 53, 56, 1),
  60px 220px 0 0 rgba(48, 53, 56, 1), 70px 220px 0 0 rgba(48, 53, 56, 1),
  80px 220px 0 0 rgba(48, 53, 56, 1), 90px 220px 0 0 rgba(48, 53, 56, 1),
  100px 220px 0 0 rgba(48, 53, 56, 1), 110px 220px 0 0 rgba(48, 53, 56, 1),
  120px 220px 0 0 rgba(48, 53, 56, 1), 130px 220px 0 0 rgba(48, 53, 56, 1),
  140px 220px 0 0 rgba(242, 245, 252, 1), 150px 220px 0 0 rgba(48, 53, 56, 1),
  160px 220px 0 0 rgba(48, 53, 56, 1), 170px 220px 0 0 rgba(48, 53, 56, 1),
  180px 220px 0 0 rgba(48, 53, 56, 1), 190px 220px 0 0 rgba(48, 53, 56, 1),
  200px 220px 0 0 rgba(48, 53, 56, 1), 210px 220px 0 0 rgba(48, 53, 56, 1),
  220px 220px 0 0 rgba(48, 53, 56, 1), 230px 220px 0 0 rgba(48, 53, 56, 1),
  240px 220px 0 0 rgba(48, 53, 56, 1), 250px 220px 0 0 rgba(48, 53, 56, 1),
  260px 220px 0 0 rgba(48, 53, 56, 1), 270px 220px 0 0 rgba(48, 53, 56, 1),
  280px 220px 0 0 rgba(48, 53, 56, 1), 290px 220px 0 0 rgba(48, 53, 56, 1),
  300px 220px 0 0 rgba(48, 53, 56, 1), 310px 220px 0 0 rgba(48, 53, 56, 1),
  320px 220px 0 0 rgba(48, 53, 56, 1), 330px 220px 0 0 rgba(48, 53, 56, 1),
  340px 220px 0 0 rgba(48, 53, 56, 1), 350px 220px 0 0 rgba(48, 53, 56, 1),
  360px 220px 0 0 rgba(48, 53, 56, 1), 370px 220px 0 0 rgba(48, 53, 56, 1),
  380px 220px 0 0 rgba(48, 53, 56, 1), 390px 220px 0 0 rgba(48, 53, 56, 1),
  400px 220px 0 0 rgba(48, 53, 56, 1), 410px 220px 0 0 rgba(48, 53, 56, 1),
  420px 220px 0 0 rgba(48, 53, 56, 1), 430px 220px 0 0 rgba(48, 53, 56, 1),
  440px 220px 0 0 rgba(48, 53, 56, 1), 450px 220px 0 0 rgba(48, 53, 56, 1),
  460px 220px 0 0 rgba(48, 53, 56, 1), 470px 220px 0 0 rgba(48, 53, 56, 1),
  480px 220px 0 0 rgba(48, 53, 56, 1), 490px 220px 0 0 rgba(48, 53, 56, 1),
  500px 220px 0 0 rgba(48, 53, 56, 1), 510px 220px 0 0 rgba(48, 53, 56, 1),
  520px 220px 0 0 rgba(48, 53, 56, 1), 530px 220px 0 0 rgba(48, 53, 56, 1),
  540px 220px 0 0 rgba(48, 53, 56, 1), 550px 220px 0 0 rgba(48, 53, 56, 1),
  560px 220px 0 0 rgba(48, 53, 56, 1), 570px 220px 0 0 rgba(48, 53, 56, 1),
  580px 220px 0 0 rgba(48, 53, 56, 1), 590px 220px 0 0 rgba(48, 53, 56, 1),
  600px 220px 0 0 rgba(48, 53, 56, 1), 610px 220px 0 0 rgba(48, 53, 56, 1),
  620px 220px 0 0 rgba(48, 53, 56, 1), 630px 220px 0 0 rgba(48, 53, 56, 1),
  640px 220px 0 0 rgba(48, 53, 56, 1), 650px 220px 0 0 rgba(48, 53, 56, 1),
  660px 220px 0 0 rgba(48, 53, 56, 1), 670px 220px 0 0 rgba(48, 53, 56, 1),
  680px 220px 0 0 rgba(48, 53, 56, 1), 690px 220px 0 0 rgba(48, 53, 56, 1),
  700px 220px 0 0 rgba(48, 53, 56, 1), 710px 220px 0 0 rgba(48, 53, 56, 1),
  720px 220px 0 0 rgba(48, 53, 56, 1), 730px 220px 0 0 rgba(48, 53, 56, 1),
  740px 220px 0 0 rgba(48, 53, 56, 1), 750px 220px 0 0 rgba(48, 53, 56, 1),
  760px 220px 0 0 rgba(242, 245, 252, 1), 770px 220px 0 0 rgba(48, 53, 56, 1),
  780px 220px 0 0 rgba(48, 53, 56, 1), 790px 220px 0 0 rgba(48, 53, 56, 1),
  800px 220px 0 0 rgba(48, 53, 56, 1), 810px 220px 0 0 rgba(48, 53, 56, 1),
  820px 220px 0 0 rgba(48, 53, 56, 1), 830px 220px 0 0 rgba(48, 53, 56, 1),
  840px 220px 0 0 rgba(48, 53, 56, 1), 850px 220px 0 0 rgba(48, 53, 56, 1),
  860px 220px 0 0 rgba(48, 53, 56, 1), 870px 220px 0 0 rgba(48, 53, 56, 1),
  880px 220px 0 0 rgba(242, 245, 252, 1), 890px 220px 0 0 rgba(48, 53, 56, 1),
  900px 220px 0 0 rgba(48, 53, 56, 1), 910px 220px 0 0 rgba(48, 53, 56, 1),
  920px 220px 0 0 rgba(48, 53, 56, 1), 930px 220px 0 0 rgba(48, 53, 56, 1),
  940px 220px 0 0 rgba(48, 53, 56, 1), 950px 220px 0 0 rgba(48, 53, 56, 1),
  960px 220px 0 0 rgba(48, 53, 56, 1), 970px 220px 0 0 rgba(48, 53, 56, 1),
  980px 220px 0 0 rgba(48, 53, 56, 1), 990px 220px 0 0 rgba(242, 245, 252, 1),
  1000px 220px 0 0 rgba(48, 53, 56, 1), 10px 230px 0 0 rgba(28, 32, 34, 1),
  20px 230px 0 0 rgba(219, 222, 232, 1), 30px 230px 0 0 rgba(111, 114, 121, 1),
  40px 230px 0 0 rgba(28, 32, 34, 1), 50px 230px 0 0 rgba(48, 53, 56, 1),
  60px 230px 0 0 rgba(48, 53, 56, 1), 70px 230px 0 0 rgba(48, 53, 56, 1),
  80px 230px 0 0 rgba(48, 53, 56, 1), 90px 230px 0 0 rgba(48, 53, 56, 1),
  100px 230px 0 0 rgba(48, 53, 56, 1), 110px 230px 0 0 rgba(48, 53, 56, 1),
  120px 230px 0 0 rgba(48, 53, 56, 1), 130px 230px 0 0 rgba(48, 53, 56, 1),
  140px 230px 0 0 rgba(48, 53, 56, 1), 150px 230px 0 0 rgba(48, 53, 56, 1),
  160px 230px 0 0 rgba(48, 53, 56, 1), 170px 230px 0 0 rgba(48, 53, 56, 1),
  180px 230px 0 0 rgba(48, 53, 56, 1), 190px 230px 0 0 rgba(48, 53, 56, 1),
  200px 230px 0 0 rgba(48, 53, 56, 1), 210px 230px 0 0 rgba(48, 53, 56, 1),
  220px 230px 0 0 rgba(48, 53, 56, 1), 230px 230px 0 0 rgba(48, 53, 56, 1),
  240px 230px 0 0 rgba(48, 53, 56, 1), 250px 230px 0 0 rgba(48, 53, 56, 1),
  260px 230px 0 0 rgba(48, 53, 56, 1), 270px 230px 0 0 rgba(48, 53, 56, 1),
  280px 230px 0 0 rgba(48, 53, 56, 1), 290px 230px 0 0 rgba(48, 53, 56, 1),
  300px 230px 0 0 rgba(48, 53, 56, 1), 310px 230px 0 0 rgba(48, 53, 56, 1),
  320px 230px 0 0 rgba(48, 53, 56, 1), 330px 230px 0 0 rgba(48, 53, 56, 1),
  340px 230px 0 0 rgba(48, 53, 56, 1), 350px 230px 0 0 rgba(48, 53, 56, 1),
  360px 230px 0 0 rgba(48, 53, 56, 1), 370px 230px 0 0 rgba(48, 53, 56, 1),
  380px 230px 0 0 rgba(48, 53, 56, 1), 390px 230px 0 0 rgba(48, 53, 56, 1),
  400px 230px 0 0 rgba(48, 53, 56, 1), 410px 230px 0 0 rgba(48, 53, 56, 1),
  420px 230px 0 0 rgba(48, 53, 56, 1), 430px 230px 0 0 rgba(48, 53, 56, 1),
  440px 230px 0 0 rgba(48, 53, 56, 1), 450px 230px 0 0 rgba(48, 53, 56, 1),
  460px 230px 0 0 rgba(48, 53, 56, 1), 470px 230px 0 0 rgba(48, 53, 56, 1),
  480px 230px 0 0 rgba(48, 53, 56, 1), 490px 230px 0 0 rgba(48, 53, 56, 1),
  500px 230px 0 0 rgba(48, 53, 56, 1), 510px 230px 0 0 rgba(48, 53, 56, 1),
  520px 230px 0 0 rgba(48, 53, 56, 1), 530px 230px 0 0 rgba(48, 53, 56, 1),
  540px 230px 0 0 rgba(48, 53, 56, 1), 550px 230px 0 0 rgba(48, 53, 56, 1),
  560px 230px 0 0 rgba(48, 53, 56, 1), 570px 230px 0 0 rgba(48, 53, 56, 1),
  580px 230px 0 0 rgba(48, 53, 56, 1), 590px 230px 0 0 rgba(48, 53, 56, 1),
  600px 230px 0 0 rgba(48, 53, 56, 1), 610px 230px 0 0 rgba(48, 53, 56, 1),
  620px 230px 0 0 rgba(48, 53, 56, 1), 630px 230px 0 0 rgba(48, 53, 56, 1),
  640px 230px 0 0 rgba(48, 53, 56, 1), 650px 230px 0 0 rgba(48, 53, 56, 1),
  660px 230px 0 0 rgba(48, 53, 56, 1), 670px 230px 0 0 rgba(48, 53, 56, 1),
  680px 230px 0 0 rgba(48, 53, 56, 1), 690px 230px 0 0 rgba(48, 53, 56, 1),
  700px 230px 0 0 rgba(48, 53, 56, 1), 710px 230px 0 0 rgba(48, 53, 56, 1),
  720px 230px 0 0 rgba(48, 53, 56, 1), 730px 230px 0 0 rgba(48, 53, 56, 1),
  740px 230px 0 0 rgba(48, 53, 56, 1), 750px 230px 0 0 rgba(48, 53, 56, 1),
  760px 230px 0 0 rgba(48, 53, 56, 1), 770px 230px 0 0 rgba(48, 53, 56, 1),
  780px 230px 0 0 rgba(48, 53, 56, 1), 790px 230px 0 0 rgba(48, 53, 56, 1),
  800px 230px 0 0 rgba(48, 53, 56, 1), 810px 230px 0 0 rgba(48, 53, 56, 1),
  820px 230px 0 0 rgba(48, 53, 56, 1), 830px 230px 0 0 rgba(48, 53, 56, 1),
  840px 230px 0 0 rgba(48, 53, 56, 1), 850px 230px 0 0 rgba(48, 53, 56, 1),
  860px 230px 0 0 rgba(48, 53, 56, 1), 870px 230px 0 0 rgba(48, 53, 56, 1),
  880px 230px 0 0 rgba(48, 53, 56, 1), 890px 230px 0 0 rgba(48, 53, 56, 1),
  900px 230px 0 0 rgba(48, 53, 56, 1), 910px 230px 0 0 rgba(48, 53, 56, 1),
  920px 230px 0 0 rgba(48, 53, 56, 1), 930px 230px 0 0 rgba(48, 53, 56, 1),
  940px 230px 0 0 rgba(48, 53, 56, 1), 950px 230px 0 0 rgba(48, 53, 56, 1),
  960px 230px 0 0 rgba(48, 53, 56, 1), 970px 230px 0 0 rgba(48, 53, 56, 1),
  980px 230px 0 0 rgba(242, 245, 252, 1), 990px 230px 0 0 rgba(48, 53, 56, 1),
  1000px 230px 0 0 rgba(48, 53, 56, 1), 10px 240px 0 0 rgba(28, 32, 34, 1),
  20px 240px 0 0 rgba(219, 222, 232, 1), 30px 240px 0 0 rgba(111, 114, 121, 1),
  40px 240px 0 0 rgba(28, 32, 34, 1), 50px 240px 0 0 rgba(48, 53, 56, 1),
  60px 240px 0 0 rgba(48, 53, 56, 1), 70px 240px 0 0 rgba(48, 53, 56, 1),
  80px 240px 0 0 rgba(48, 53, 56, 1), 90px 240px 0 0 rgba(48, 53, 56, 1),
  100px 240px 0 0 rgba(48, 53, 56, 1), 110px 240px 0 0 rgba(48, 53, 56, 1),
  120px 240px 0 0 rgba(48, 53, 56, 1), 130px 240px 0 0 rgba(48, 53, 56, 1),
  140px 240px 0 0 rgba(242, 245, 252, 1), 150px 240px 0 0 rgba(48, 53, 56, 1),
  160px 240px 0 0 rgba(48, 53, 56, 1), 170px 240px 0 0 rgba(48, 53, 56, 1),
  180px 240px 0 0 rgba(48, 53, 56, 1), 190px 240px 0 0 rgba(48, 53, 56, 1),
  200px 240px 0 0 rgba(48, 53, 56, 1), 210px 240px 0 0 rgba(48, 53, 56, 1),
  220px 240px 0 0 rgba(48, 53, 56, 1), 230px 240px 0 0 rgba(48, 53, 56, 1),
  240px 240px 0 0 rgba(48, 53, 56, 1), 250px 240px 0 0 rgba(48, 53, 56, 1),
  260px 240px 0 0 rgba(48, 53, 56, 1), 270px 240px 0 0 rgba(48, 53, 56, 1),
  280px 240px 0 0 rgba(48, 53, 56, 1), 290px 240px 0 0 rgba(48, 53, 56, 1),
  300px 240px 0 0 rgba(48, 53, 56, 1), 310px 240px 0 0 rgba(48, 53, 56, 1),
  320px 240px 0 0 rgba(48, 53, 56, 1), 330px 240px 0 0 rgba(48, 53, 56, 1),
  340px 240px 0 0 rgba(48, 53, 56, 1), 350px 240px 0 0 rgba(48, 53, 56, 1),
  360px 240px 0 0 rgba(48, 53, 56, 1), 370px 240px 0 0 rgba(48, 53, 56, 1),
  380px 240px 0 0 rgba(48, 53, 56, 1), 390px 240px 0 0 rgba(48, 53, 56, 1),
  400px 240px 0 0 rgba(48, 53, 56, 1), 410px 240px 0 0 rgba(48, 53, 56, 1),
  420px 240px 0 0 rgba(48, 53, 56, 1), 430px 240px 0 0 rgba(48, 53, 56, 1),
  440px 240px 0 0 rgba(48, 53, 56, 1), 450px 240px 0 0 rgba(48, 53, 56, 1),
  460px 240px 0 0 rgba(48, 53, 56, 1), 470px 240px 0 0 rgba(48, 53, 56, 1),
  480px 240px 0 0 rgba(48, 53, 56, 1), 490px 240px 0 0 rgba(48, 53, 56, 1),
  500px 240px 0 0 rgba(48, 53, 56, 1), 510px 240px 0 0 rgba(48, 53, 56, 1),
  520px 240px 0 0 rgba(48, 53, 56, 1), 530px 240px 0 0 rgba(48, 53, 56, 1),
  540px 240px 0 0 rgba(48, 53, 56, 1), 550px 240px 0 0 rgba(48, 53, 56, 1),
  560px 240px 0 0 rgba(48, 53, 56, 1), 570px 240px 0 0 rgba(48, 53, 56, 1),
  580px 240px 0 0 rgba(48, 53, 56, 1), 590px 240px 0 0 rgba(48, 53, 56, 1),
  600px 240px 0 0 rgba(48, 53, 56, 1), 610px 240px 0 0 rgba(48, 53, 56, 1),
  620px 240px 0 0 rgba(48, 53, 56, 1), 630px 240px 0 0 rgba(48, 53, 56, 1),
  640px 240px 0 0 rgba(48, 53, 56, 1), 650px 240px 0 0 rgba(48, 53, 56, 1),
  660px 240px 0 0 rgba(48, 53, 56, 1), 670px 240px 0 0 rgba(48, 53, 56, 1),
  680px 240px 0 0 rgba(48, 53, 56, 1), 690px 240px 0 0 rgba(48, 53, 56, 1),
  700px 240px 0 0 rgba(48, 53, 56, 1), 710px 240px 0 0 rgba(48, 53, 56, 1),
  720px 240px 0 0 rgba(48, 53, 56, 1), 730px 240px 0 0 rgba(48, 53, 56, 1),
  740px 240px 0 0 rgba(48, 53, 56, 1), 750px 240px 0 0 rgba(48, 53, 56, 1),
  760px 240px 0 0 rgba(242, 245, 252, 1), 770px 240px 0 0 rgba(48, 53, 56, 1),
  780px 240px 0 0 rgba(48, 53, 56, 1), 790px 240px 0 0 rgba(48, 53, 56, 1),
  800px 240px 0 0 rgba(48, 53, 56, 1), 810px 240px 0 0 rgba(48, 53, 56, 1),
  820px 240px 0 0 rgba(48, 53, 56, 1), 830px 240px 0 0 rgba(48, 53, 56, 1),
  840px 240px 0 0 rgba(48, 53, 56, 1), 850px 240px 0 0 rgba(48, 53, 56, 1),
  860px 240px 0 0 rgba(48, 53, 56, 1), 870px 240px 0 0 rgba(48, 53, 56, 1),
  880px 240px 0 0 rgba(48, 53, 56, 1), 890px 240px 0 0 rgba(48, 53, 56, 1),
  900px 240px 0 0 rgba(48, 53, 56, 1), 910px 240px 0 0 rgba(48, 53, 56, 1),
  920px 240px 0 0 rgba(48, 53, 56, 1), 930px 240px 0 0 rgba(48, 53, 56, 1),
  940px 240px 0 0 rgba(48, 53, 56, 1), 950px 240px 0 0 rgba(48, 53, 56, 1),
  960px 240px 0 0 rgba(48, 53, 56, 1), 970px 240px 0 0 rgba(242, 245, 252, 1),
  980px 240px 0 0 rgba(48, 53, 56, 1), 990px 240px 0 0 rgba(48, 53, 56, 1),
  1000px 240px 0 0 rgba(48, 53, 56, 1), 10px 250px 0 0 rgba(28, 32, 34, 1),
  20px 250px 0 0 rgba(219, 222, 232, 1), 30px 250px 0 0 rgba(111, 114, 121, 1),
  40px 250px 0 0 rgba(28, 32, 34, 1), 50px 250px 0 0 rgba(48, 53, 56, 1),
  60px 250px 0 0 rgba(48, 53, 56, 1), 70px 250px 0 0 rgba(48, 53, 56, 1),
  80px 250px 0 0 rgba(48, 53, 56, 1), 90px 250px 0 0 rgba(48, 53, 56, 1),
  100px 250px 0 0 rgba(48, 53, 56, 1), 110px 250px 0 0 rgba(48, 53, 56, 1),
  120px 250px 0 0 rgba(48, 53, 56, 1), 130px 250px 0 0 rgba(48, 53, 56, 1),
  140px 250px 0 0 rgba(242, 245, 252, 1), 150px 250px 0 0 rgba(48, 53, 56, 1),
  160px 250px 0 0 rgba(48, 53, 56, 1), 170px 250px 0 0 rgba(48, 53, 56, 1),
  180px 250px 0 0 rgba(48, 53, 56, 1), 190px 250px 0 0 rgba(48, 53, 56, 1),
  200px 250px 0 0 rgba(48, 53, 56, 1), 210px 250px 0 0 rgba(48, 53, 56, 1),
  220px 250px 0 0 rgba(48, 53, 56, 1), 230px 250px 0 0 rgba(48, 53, 56, 1),
  240px 250px 0 0 rgba(48, 53, 56, 1), 250px 250px 0 0 rgba(48, 53, 56, 1),
  260px 250px 0 0 rgba(48, 53, 56, 1), 270px 250px 0 0 rgba(48, 53, 56, 1),
  280px 250px 0 0 rgba(48, 53, 56, 1), 290px 250px 0 0 rgba(48, 53, 56, 1),
  300px 250px 0 0 rgba(48, 53, 56, 1), 310px 250px 0 0 rgba(48, 53, 56, 1),
  320px 250px 0 0 rgba(48, 53, 56, 1), 330px 250px 0 0 rgba(48, 53, 56, 1),
  340px 250px 0 0 rgba(48, 53, 56, 1), 350px 250px 0 0 rgba(48, 53, 56, 1),
  360px 250px 0 0 rgba(48, 53, 56, 1), 370px 250px 0 0 rgba(48, 53, 56, 1),
  380px 250px 0 0 rgba(48, 53, 56, 1), 390px 250px 0 0 rgba(48, 53, 56, 1),
  400px 250px 0 0 rgba(48, 53, 56, 1), 410px 250px 0 0 rgba(48, 53, 56, 1),
  420px 250px 0 0 rgba(48, 53, 56, 1), 430px 250px 0 0 rgba(48, 53, 56, 1),
  440px 250px 0 0 rgba(48, 53, 56, 1), 450px 250px 0 0 rgba(48, 53, 56, 1),
  460px 250px 0 0 rgba(48, 53, 56, 1), 470px 250px 0 0 rgba(48, 53, 56, 1),
  480px 250px 0 0 rgba(48, 53, 56, 1), 490px 250px 0 0 rgba(48, 53, 56, 1),
  500px 250px 0 0 rgba(48, 53, 56, 1), 510px 250px 0 0 rgba(48, 53, 56, 1),
  520px 250px 0 0 rgba(48, 53, 56, 1), 530px 250px 0 0 rgba(48, 53, 56, 1),
  540px 250px 0 0 rgba(48, 53, 56, 1), 550px 250px 0 0 rgba(48, 53, 56, 1),
  560px 250px 0 0 rgba(48, 53, 56, 1), 570px 250px 0 0 rgba(48, 53, 56, 1),
  580px 250px 0 0 rgba(48, 53, 56, 1), 590px 250px 0 0 rgba(48, 53, 56, 1),
  600px 250px 0 0 rgba(48, 53, 56, 1), 610px 250px 0 0 rgba(48, 53, 56, 1),
  620px 250px 0 0 rgba(48, 53, 56, 1), 630px 250px 0 0 rgba(48, 53, 56, 1),
  640px 250px 0 0 rgba(48, 53, 56, 1), 650px 250px 0 0 rgba(48, 53, 56, 1),
  660px 250px 0 0 rgba(48, 53, 56, 1), 670px 250px 0 0 rgba(48, 53, 56, 1),
  680px 250px 0 0 rgba(48, 53, 56, 1), 690px 250px 0 0 rgba(48, 53, 56, 1),
  700px 250px 0 0 rgba(48, 53, 56, 1), 710px 250px 0 0 rgba(48, 53, 56, 1),
  720px 250px 0 0 rgba(48, 53, 56, 1), 730px 250px 0 0 rgba(48, 53, 56, 1),
  740px 250px 0 0 rgba(48, 53, 56, 1), 750px 250px 0 0 rgba(48, 53, 56, 1),
  760px 250px 0 0 rgba(242, 245, 252, 1), 770px 250px 0 0 rgba(48, 53, 56, 1),
  780px 250px 0 0 rgba(48, 53, 56, 1), 790px 250px 0 0 rgba(48, 53, 56, 1),
  800px 250px 0 0 rgba(48, 53, 56, 1), 810px 250px 0 0 rgba(48, 53, 56, 1),
  820px 250px 0 0 rgba(48, 53, 56, 1), 830px 250px 0 0 rgba(48, 53, 56, 1),
  840px 250px 0 0 rgba(48, 53, 56, 1), 850px 250px 0 0 rgba(48, 53, 56, 1),
  860px 250px 0 0 rgba(48, 53, 56, 1), 870px 250px 0 0 rgba(48, 53, 56, 1),
  880px 250px 0 0 rgba(48, 53, 56, 1), 890px 250px 0 0 rgba(48, 53, 56, 1),
  900px 250px 0 0 rgba(48, 53, 56, 1), 910px 250px 0 0 rgba(48, 53, 56, 1),
  920px 250px 0 0 rgba(48, 53, 56, 1), 930px 250px 0 0 rgba(48, 53, 56, 1),
  940px 250px 0 0 rgba(48, 53, 56, 1), 950px 250px 0 0 rgba(48, 53, 56, 1),
  960px 250px 0 0 rgba(242, 245, 252, 1), 970px 250px 0 0 rgba(48, 53, 56, 1),
  980px 250px 0 0 rgba(48, 53, 56, 1), 990px 250px 0 0 rgba(48, 53, 56, 1),
  1000px 250px 0 0 rgba(48, 53, 56, 1), 10px 260px 0 0 rgba(28, 32, 34, 1),
  20px 260px 0 0 rgba(219, 222, 232, 1), 30px 260px 0 0 rgba(111, 114, 121, 1),
  40px 260px 0 0 rgba(28, 32, 34, 1), 50px 260px 0 0 rgba(48, 53, 56, 1),
  60px 260px 0 0 rgba(48, 53, 56, 1), 70px 260px 0 0 rgba(48, 53, 56, 1),
  80px 260px 0 0 rgba(48, 53, 56, 1), 90px 260px 0 0 rgba(48, 53, 56, 1),
  100px 260px 0 0 rgba(48, 53, 56, 1), 110px 260px 0 0 rgba(48, 53, 56, 1),
  120px 260px 0 0 rgba(48, 53, 56, 1), 130px 260px 0 0 rgba(48, 53, 56, 1),
  140px 260px 0 0 rgba(242, 245, 252, 1), 150px 260px 0 0 rgba(48, 53, 56, 1),
  160px 260px 0 0 rgba(48, 53, 56, 1), 170px 260px 0 0 rgba(48, 53, 56, 1),
  180px 260px 0 0 rgba(48, 53, 56, 1), 190px 260px 0 0 rgba(48, 53, 56, 1),
  200px 260px 0 0 rgba(48, 53, 56, 1), 210px 260px 0 0 rgba(48, 53, 56, 1),
  220px 260px 0 0 rgba(48, 53, 56, 1), 230px 260px 0 0 rgba(48, 53, 56, 1),
  240px 260px 0 0 rgba(48, 53, 56, 1), 250px 260px 0 0 rgba(48, 53, 56, 1),
  260px 260px 0 0 rgba(48, 53, 56, 1), 270px 260px 0 0 rgba(48, 53, 56, 1),
  280px 260px 0 0 rgba(48, 53, 56, 1), 290px 260px 0 0 rgba(48, 53, 56, 1),
  300px 260px 0 0 rgba(48, 53, 56, 1), 310px 260px 0 0 rgba(48, 53, 56, 1),
  320px 260px 0 0 rgba(48, 53, 56, 1), 330px 260px 0 0 rgba(48, 53, 56, 1),
  340px 260px 0 0 rgba(48, 53, 56, 1), 350px 260px 0 0 rgba(48, 53, 56, 1),
  360px 260px 0 0 rgba(48, 53, 56, 1), 370px 260px 0 0 rgba(48, 53, 56, 1),
  380px 260px 0 0 rgba(48, 53, 56, 1), 390px 260px 0 0 rgba(48, 53, 56, 1),
  400px 260px 0 0 rgba(48, 53, 56, 1), 410px 260px 0 0 rgba(48, 53, 56, 1),
  420px 260px 0 0 rgba(48, 53, 56, 1), 430px 260px 0 0 rgba(48, 53, 56, 1),
  440px 260px 0 0 rgba(48, 53, 56, 1), 450px 260px 0 0 rgba(48, 53, 56, 1),
  460px 260px 0 0 rgba(48, 53, 56, 1), 470px 260px 0 0 rgba(48, 53, 56, 1),
  480px 260px 0 0 rgba(48, 53, 56, 1), 490px 260px 0 0 rgba(48, 53, 56, 1),
  500px 260px 0 0 rgba(48, 53, 56, 1), 510px 260px 0 0 rgba(48, 53, 56, 1),
  520px 260px 0 0 rgba(48, 53, 56, 1), 530px 260px 0 0 rgba(48, 53, 56, 1),
  540px 260px 0 0 rgba(48, 53, 56, 1), 550px 260px 0 0 rgba(48, 53, 56, 1),
  560px 260px 0 0 rgba(48, 53, 56, 1), 570px 260px 0 0 rgba(48, 53, 56, 1),
  580px 260px 0 0 rgba(48, 53, 56, 1), 590px 260px 0 0 rgba(48, 53, 56, 1),
  600px 260px 0 0 rgba(48, 53, 56, 1), 610px 260px 0 0 rgba(48, 53, 56, 1),
  620px 260px 0 0 rgba(48, 53, 56, 1), 630px 260px 0 0 rgba(48, 53, 56, 1),
  640px 260px 0 0 rgba(48, 53, 56, 1), 650px 260px 0 0 rgba(48, 53, 56, 1),
  660px 260px 0 0 rgba(48, 53, 56, 1), 670px 260px 0 0 rgba(48, 53, 56, 1),
  680px 260px 0 0 rgba(48, 53, 56, 1), 690px 260px 0 0 rgba(48, 53, 56, 1),
  700px 260px 0 0 rgba(48, 53, 56, 1), 710px 260px 0 0 rgba(48, 53, 56, 1),
  720px 260px 0 0 rgba(48, 53, 56, 1), 730px 260px 0 0 rgba(48, 53, 56, 1),
  740px 260px 0 0 rgba(48, 53, 56, 1), 750px 260px 0 0 rgba(48, 53, 56, 1),
  760px 260px 0 0 rgba(242, 245, 252, 1), 770px 260px 0 0 rgba(48, 53, 56, 1),
  780px 260px 0 0 rgba(48, 53, 56, 1), 790px 260px 0 0 rgba(48, 53, 56, 1),
  800px 260px 0 0 rgba(48, 53, 56, 1), 810px 260px 0 0 rgba(48, 53, 56, 1),
  820px 260px 0 0 rgba(48, 53, 56, 1), 830px 260px 0 0 rgba(48, 53, 56, 1),
  840px 260px 0 0 rgba(48, 53, 56, 1), 850px 260px 0 0 rgba(48, 53, 56, 1),
  860px 260px 0 0 rgba(48, 53, 56, 1), 870px 260px 0 0 rgba(48, 53, 56, 1),
  880px 260px 0 0 rgba(48, 53, 56, 1), 890px 260px 0 0 rgba(48, 53, 56, 1),
  900px 260px 0 0 rgba(48, 53, 56, 1), 910px 260px 0 0 rgba(48, 53, 56, 1),
  920px 260px 0 0 rgba(48, 53, 56, 1), 930px 260px 0 0 rgba(48, 53, 56, 1),
  940px 260px 0 0 rgba(48, 53, 56, 1), 950px 260px 0 0 rgba(242, 245, 252, 1),
  960px 260px 0 0 rgba(48, 53, 56, 1), 970px 260px 0 0 rgba(48, 53, 56, 1),
  980px 260px 0 0 rgba(48, 53, 56, 1), 990px 260px 0 0 rgba(48, 53, 56, 1),
  1000px 260px 0 0 rgba(48, 53, 56, 1), 10px 270px 0 0 rgba(28, 32, 34, 1),
  20px 270px 0 0 rgba(219, 222, 232, 1), 30px 270px 0 0 rgba(111, 114, 121, 1),
  40px 270px 0 0 rgba(28, 32, 34, 1), 50px 270px 0 0 rgba(48, 53, 56, 1),
  60px 270px 0 0 rgba(48, 53, 56, 1), 70px 270px 0 0 rgba(48, 53, 56, 1),
  80px 270px 0 0 rgba(48, 53, 56, 1), 90px 270px 0 0 rgba(48, 53, 56, 1),
  100px 270px 0 0 rgba(48, 53, 56, 1), 110px 270px 0 0 rgba(48, 53, 56, 1),
  120px 270px 0 0 rgba(48, 53, 56, 1), 130px 270px 0 0 rgba(48, 53, 56, 1),
  140px 270px 0 0 rgba(242, 245, 252, 1), 150px 270px 0 0 rgba(48, 53, 56, 1),
  160px 270px 0 0 rgba(48, 53, 56, 1), 170px 270px 0 0 rgba(48, 53, 56, 1),
  180px 270px 0 0 rgba(48, 53, 56, 1), 190px 270px 0 0 rgba(48, 53, 56, 1),
  200px 270px 0 0 rgba(48, 53, 56, 1), 210px 270px 0 0 rgba(48, 53, 56, 1),
  220px 270px 0 0 rgba(48, 53, 56, 1), 230px 270px 0 0 rgba(48, 53, 56, 1),
  240px 270px 0 0 rgba(48, 53, 56, 1), 250px 270px 0 0 rgba(48, 53, 56, 1),
  260px 270px 0 0 rgba(48, 53, 56, 1), 270px 270px 0 0 rgba(48, 53, 56, 1),
  280px 270px 0 0 rgba(48, 53, 56, 1), 290px 270px 0 0 rgba(48, 53, 56, 1),
  300px 270px 0 0 rgba(48, 53, 56, 1), 310px 270px 0 0 rgba(48, 53, 56, 1),
  320px 270px 0 0 rgba(48, 53, 56, 1), 330px 270px 0 0 rgba(48, 53, 56, 1),
  340px 270px 0 0 rgba(48, 53, 56, 1), 350px 270px 0 0 rgba(48, 53, 56, 1),
  360px 270px 0 0 rgba(48, 53, 56, 1), 370px 270px 0 0 rgba(48, 53, 56, 1),
  380px 270px 0 0 rgba(48, 53, 56, 1), 390px 270px 0 0 rgba(48, 53, 56, 1),
  400px 270px 0 0 rgba(48, 53, 56, 1), 410px 270px 0 0 rgba(48, 53, 56, 1),
  420px 270px 0 0 rgba(48, 53, 56, 1), 430px 270px 0 0 rgba(48, 53, 56, 1),
  440px 270px 0 0 rgba(48, 53, 56, 1), 450px 270px 0 0 rgba(48, 53, 56, 1),
  460px 270px 0 0 rgba(48, 53, 56, 1), 470px 270px 0 0 rgba(48, 53, 56, 1),
  480px 270px 0 0 rgba(48, 53, 56, 1), 490px 270px 0 0 rgba(48, 53, 56, 1),
  500px 270px 0 0 rgba(48, 53, 56, 1), 510px 270px 0 0 rgba(48, 53, 56, 1),
  520px 270px 0 0 rgba(48, 53, 56, 1), 530px 270px 0 0 rgba(48, 53, 56, 1),
  540px 270px 0 0 rgba(48, 53, 56, 1), 550px 270px 0 0 rgba(48, 53, 56, 1),
  560px 270px 0 0 rgba(48, 53, 56, 1), 570px 270px 0 0 rgba(48, 53, 56, 1),
  580px 270px 0 0 rgba(48, 53, 56, 1), 590px 270px 0 0 rgba(48, 53, 56, 1),
  600px 270px 0 0 rgba(48, 53, 56, 1), 610px 270px 0 0 rgba(48, 53, 56, 1),
  620px 270px 0 0 rgba(48, 53, 56, 1), 630px 270px 0 0 rgba(48, 53, 56, 1),
  640px 270px 0 0 rgba(48, 53, 56, 1), 650px 270px 0 0 rgba(48, 53, 56, 1),
  660px 270px 0 0 rgba(48, 53, 56, 1), 670px 270px 0 0 rgba(48, 53, 56, 1),
  680px 270px 0 0 rgba(48, 53, 56, 1), 690px 270px 0 0 rgba(48, 53, 56, 1),
  700px 270px 0 0 rgba(48, 53, 56, 1), 710px 270px 0 0 rgba(48, 53, 56, 1),
  720px 270px 0 0 rgba(48, 53, 56, 1), 730px 270px 0 0 rgba(48, 53, 56, 1),
  740px 270px 0 0 rgba(48, 53, 56, 1), 750px 270px 0 0 rgba(48, 53, 56, 1),
  760px 270px 0 0 rgba(242, 245, 252, 1), 770px 270px 0 0 rgba(48, 53, 56, 1),
  780px 270px 0 0 rgba(48, 53, 56, 1), 790px 270px 0 0 rgba(48, 53, 56, 1),
  800px 270px 0 0 rgba(48, 53, 56, 1), 810px 270px 0 0 rgba(48, 53, 56, 1),
  820px 270px 0 0 rgba(48, 53, 56, 1), 830px 270px 0 0 rgba(48, 53, 56, 1),
  840px 270px 0 0 rgba(48, 53, 56, 1), 850px 270px 0 0 rgba(48, 53, 56, 1),
  860px 270px 0 0 rgba(48, 53, 56, 1), 870px 270px 0 0 rgba(48, 53, 56, 1),
  880px 270px 0 0 rgba(48, 53, 56, 1), 890px 270px 0 0 rgba(48, 53, 56, 1),
  900px 270px 0 0 rgba(48, 53, 56, 1), 910px 270px 0 0 rgba(48, 53, 56, 1),
  920px 270px 0 0 rgba(48, 53, 56, 1), 930px 270px 0 0 rgba(48, 53, 56, 1),
  940px 270px 0 0 rgba(242, 245, 252, 1), 950px 270px 0 0 rgba(48, 53, 56, 1),
  960px 270px 0 0 rgba(48, 53, 56, 1), 970px 270px 0 0 rgba(48, 53, 56, 1),
  980px 270px 0 0 rgba(48, 53, 56, 1), 990px 270px 0 0 rgba(48, 53, 56, 1),
  1000px 270px 0 0 rgba(48, 53, 56, 1), 10px 280px 0 0 rgba(28, 32, 34, 1),
  20px 280px 0 0 rgba(219, 222, 232, 1), 30px 280px 0 0 rgba(111, 114, 121, 1),
  40px 280px 0 0 rgba(28, 32, 34, 1), 50px 280px 0 0 rgba(48, 53, 56, 1),
  60px 280px 0 0 rgba(48, 53, 56, 1), 70px 280px 0 0 rgba(48, 53, 56, 1),
  80px 280px 0 0 rgba(48, 53, 56, 1), 90px 280px 0 0 rgba(48, 53, 56, 1),
  100px 280px 0 0 rgba(48, 53, 56, 1), 110px 280px 0 0 rgba(48, 53, 56, 1),
  120px 280px 0 0 rgba(48, 53, 56, 1), 130px 280px 0 0 rgba(48, 53, 56, 1),
  140px 280px 0 0 rgba(242, 245, 252, 1), 150px 280px 0 0 rgba(48, 53, 56, 1),
  160px 280px 0 0 rgba(48, 53, 56, 1), 170px 280px 0 0 rgba(48, 53, 56, 1),
  180px 280px 0 0 rgba(48, 53, 56, 1), 190px 280px 0 0 rgba(48, 53, 56, 1),
  200px 280px 0 0 rgba(48, 53, 56, 1), 210px 280px 0 0 rgba(48, 53, 56, 1),
  220px 280px 0 0 rgba(48, 53, 56, 1), 230px 280px 0 0 rgba(48, 53, 56, 1),
  240px 280px 0 0 rgba(48, 53, 56, 1), 250px 280px 0 0 rgba(48, 53, 56, 1),
  260px 280px 0 0 rgba(48, 53, 56, 1), 270px 280px 0 0 rgba(48, 53, 56, 1),
  280px 280px 0 0 rgba(48, 53, 56, 1), 290px 280px 0 0 rgba(48, 53, 56, 1),
  300px 280px 0 0 rgba(48, 53, 56, 1), 310px 280px 0 0 rgba(48, 53, 56, 1),
  320px 280px 0 0 rgba(48, 53, 56, 1), 330px 280px 0 0 rgba(48, 53, 56, 1),
  340px 280px 0 0 rgba(48, 53, 56, 1), 350px 280px 0 0 rgba(48, 53, 56, 1),
  360px 280px 0 0 rgba(48, 53, 56, 1), 370px 280px 0 0 rgba(48, 53, 56, 1),
  380px 280px 0 0 rgba(48, 53, 56, 1), 390px 280px 0 0 rgba(48, 53, 56, 1),
  400px 280px 0 0 rgba(48, 53, 56, 1), 410px 280px 0 0 rgba(48, 53, 56, 1),
  420px 280px 0 0 rgba(48, 53, 56, 1), 430px 280px 0 0 rgba(48, 53, 56, 1),
  440px 280px 0 0 rgba(48, 53, 56, 1), 450px 280px 0 0 rgba(48, 53, 56, 1),
  460px 280px 0 0 rgba(48, 53, 56, 1), 470px 280px 0 0 rgba(48, 53, 56, 1),
  480px 280px 0 0 rgba(48, 53, 56, 1), 490px 280px 0 0 rgba(48, 53, 56, 1),
  500px 280px 0 0 rgba(48, 53, 56, 1), 510px 280px 0 0 rgba(48, 53, 56, 1),
  520px 280px 0 0 rgba(48, 53, 56, 1), 530px 280px 0 0 rgba(48, 53, 56, 1),
  540px 280px 0 0 rgba(48, 53, 56, 1), 550px 280px 0 0 rgba(48, 53, 56, 1),
  560px 280px 0 0 rgba(48, 53, 56, 1), 570px 280px 0 0 rgba(48, 53, 56, 1),
  580px 280px 0 0 rgba(48, 53, 56, 1), 590px 280px 0 0 rgba(48, 53, 56, 1),
  600px 280px 0 0 rgba(48, 53, 56, 1), 610px 280px 0 0 rgba(48, 53, 56, 1),
  620px 280px 0 0 rgba(48, 53, 56, 1), 630px 280px 0 0 rgba(48, 53, 56, 1),
  640px 280px 0 0 rgba(48, 53, 56, 1), 650px 280px 0 0 rgba(48, 53, 56, 1),
  660px 280px 0 0 rgba(48, 53, 56, 1), 670px 280px 0 0 rgba(48, 53, 56, 1),
  680px 280px 0 0 rgba(48, 53, 56, 1), 690px 280px 0 0 rgba(48, 53, 56, 1),
  700px 280px 0 0 rgba(48, 53, 56, 1), 710px 280px 0 0 rgba(48, 53, 56, 1),
  720px 280px 0 0 rgba(48, 53, 56, 1), 730px 280px 0 0 rgba(48, 53, 56, 1),
  740px 280px 0 0 rgba(48, 53, 56, 1), 750px 280px 0 0 rgba(48, 53, 56, 1),
  760px 280px 0 0 rgba(242, 245, 252, 1), 770px 280px 0 0 rgba(48, 53, 56, 1),
  780px 280px 0 0 rgba(48, 53, 56, 1), 790px 280px 0 0 rgba(48, 53, 56, 1),
  800px 280px 0 0 rgba(48, 53, 56, 1), 810px 280px 0 0 rgba(48, 53, 56, 1),
  820px 280px 0 0 rgba(48, 53, 56, 1), 830px 280px 0 0 rgba(48, 53, 56, 1),
  840px 280px 0 0 rgba(48, 53, 56, 1), 850px 280px 0 0 rgba(48, 53, 56, 1),
  860px 280px 0 0 rgba(48, 53, 56, 1), 870px 280px 0 0 rgba(48, 53, 56, 1),
  880px 280px 0 0 rgba(48, 53, 56, 1), 890px 280px 0 0 rgba(48, 53, 56, 1),
  900px 280px 0 0 rgba(48, 53, 56, 1), 910px 280px 0 0 rgba(48, 53, 56, 1),
  920px 280px 0 0 rgba(48, 53, 56, 1), 930px 280px 0 0 rgba(242, 245, 252, 1),
  940px 280px 0 0 rgba(48, 53, 56, 1), 950px 280px 0 0 rgba(48, 53, 56, 1),
  960px 280px 0 0 rgba(48, 53, 56, 1), 970px 280px 0 0 rgba(48, 53, 56, 1),
  980px 280px 0 0 rgba(48, 53, 56, 1), 990px 280px 0 0 rgba(48, 53, 56, 1),
  1000px 280px 0 0 rgba(48, 53, 56, 1), 10px 290px 0 0 rgba(28, 32, 34, 1),
  20px 290px 0 0 rgba(219, 222, 232, 1), 30px 290px 0 0 rgba(111, 114, 121, 1),
  40px 290px 0 0 rgba(28, 32, 34, 1), 50px 290px 0 0 rgba(48, 53, 56, 1),
  60px 290px 0 0 rgba(48, 53, 56, 1), 70px 290px 0 0 rgba(48, 53, 56, 1),
  80px 290px 0 0 rgba(48, 53, 56, 1), 90px 290px 0 0 rgba(48, 53, 56, 1),
  100px 290px 0 0 rgba(48, 53, 56, 1), 110px 290px 0 0 rgba(48, 53, 56, 1),
  120px 290px 0 0 rgba(48, 53, 56, 1), 130px 290px 0 0 rgba(48, 53, 56, 1),
  140px 290px 0 0 rgba(48, 53, 56, 1), 150px 290px 0 0 rgba(48, 53, 56, 1),
  160px 290px 0 0 rgba(48, 53, 56, 1), 170px 290px 0 0 rgba(48, 53, 56, 1),
  180px 290px 0 0 rgba(48, 53, 56, 1), 190px 290px 0 0 rgba(48, 53, 56, 1),
  200px 290px 0 0 rgba(48, 53, 56, 1), 210px 290px 0 0 rgba(48, 53, 56, 1),
  220px 290px 0 0 rgba(48, 53, 56, 1), 230px 290px 0 0 rgba(48, 53, 56, 1),
  240px 290px 0 0 rgba(48, 53, 56, 1), 250px 290px 0 0 rgba(48, 53, 56, 1),
  260px 290px 0 0 rgba(48, 53, 56, 1), 270px 290px 0 0 rgba(48, 53, 56, 1),
  280px 290px 0 0 rgba(48, 53, 56, 1), 290px 290px 0 0 rgba(48, 53, 56, 1),
  300px 290px 0 0 rgba(48, 53, 56, 1), 310px 290px 0 0 rgba(48, 53, 56, 1),
  320px 290px 0 0 rgba(48, 53, 56, 1), 330px 290px 0 0 rgba(48, 53, 56, 1),
  340px 290px 0 0 rgba(48, 53, 56, 1), 350px 290px 0 0 rgba(48, 53, 56, 1),
  360px 290px 0 0 rgba(48, 53, 56, 1), 370px 290px 0 0 rgba(48, 53, 56, 1),
  380px 290px 0 0 rgba(48, 53, 56, 1), 390px 290px 0 0 rgba(48, 53, 56, 1),
  400px 290px 0 0 rgba(48, 53, 56, 1), 410px 290px 0 0 rgba(48, 53, 56, 1),
  420px 290px 0 0 rgba(48, 53, 56, 1), 430px 290px 0 0 rgba(48, 53, 56, 1),
  440px 290px 0 0 rgba(48, 53, 56, 1), 450px 290px 0 0 rgba(48, 53, 56, 1),
  460px 290px 0 0 rgba(48, 53, 56, 1), 470px 290px 0 0 rgba(48, 53, 56, 1),
  480px 290px 0 0 rgba(48, 53, 56, 1), 490px 290px 0 0 rgba(48, 53, 56, 1),
  500px 290px 0 0 rgba(48, 53, 56, 1), 510px 290px 0 0 rgba(48, 53, 56, 1),
  520px 290px 0 0 rgba(48, 53, 56, 1), 530px 290px 0 0 rgba(48, 53, 56, 1),
  540px 290px 0 0 rgba(48, 53, 56, 1), 550px 290px 0 0 rgba(48, 53, 56, 1),
  560px 290px 0 0 rgba(48, 53, 56, 1), 570px 290px 0 0 rgba(48, 53, 56, 1),
  580px 290px 0 0 rgba(48, 53, 56, 1), 590px 290px 0 0 rgba(48, 53, 56, 1),
  600px 290px 0 0 rgba(48, 53, 56, 1), 610px 290px 0 0 rgba(48, 53, 56, 1),
  620px 290px 0 0 rgba(48, 53, 56, 1), 630px 290px 0 0 rgba(48, 53, 56, 1),
  640px 290px 0 0 rgba(48, 53, 56, 1), 650px 290px 0 0 rgba(48, 53, 56, 1),
  660px 290px 0 0 rgba(48, 53, 56, 1), 670px 290px 0 0 rgba(48, 53, 56, 1),
  680px 290px 0 0 rgba(48, 53, 56, 1), 690px 290px 0 0 rgba(48, 53, 56, 1),
  700px 290px 0 0 rgba(48, 53, 56, 1), 710px 290px 0 0 rgba(48, 53, 56, 1),
  720px 290px 0 0 rgba(48, 53, 56, 1), 730px 290px 0 0 rgba(48, 53, 56, 1),
  740px 290px 0 0 rgba(48, 53, 56, 1), 750px 290px 0 0 rgba(48, 53, 56, 1),
  760px 290px 0 0 rgba(48, 53, 56, 1), 770px 290px 0 0 rgba(48, 53, 56, 1),
  780px 290px 0 0 rgba(48, 53, 56, 1), 790px 290px 0 0 rgba(48, 53, 56, 1),
  800px 290px 0 0 rgba(48, 53, 56, 1), 810px 290px 0 0 rgba(48, 53, 56, 1),
  820px 290px 0 0 rgba(48, 53, 56, 1), 830px 290px 0 0 rgba(48, 53, 56, 1),
  840px 290px 0 0 rgba(48, 53, 56, 1), 850px 290px 0 0 rgba(48, 53, 56, 1),
  860px 290px 0 0 rgba(48, 53, 56, 1), 870px 290px 0 0 rgba(48, 53, 56, 1),
  880px 290px 0 0 rgba(48, 53, 56, 1), 890px 290px 0 0 rgba(48, 53, 56, 1),
  900px 290px 0 0 rgba(48, 53, 56, 1), 910px 290px 0 0 rgba(48, 53, 56, 1),
  920px 290px 0 0 rgba(242, 245, 252, 1), 930px 290px 0 0 rgba(48, 53, 56, 1),
  940px 290px 0 0 rgba(48, 53, 56, 1), 950px 290px 0 0 rgba(48, 53, 56, 1),
  960px 290px 0 0 rgba(48, 53, 56, 1), 970px 290px 0 0 rgba(48, 53, 56, 1),
  980px 290px 0 0 rgba(48, 53, 56, 1), 990px 290px 0 0 rgba(48, 53, 56, 1),
  1000px 290px 0 0 rgba(48, 53, 56, 1), 10px 300px 0 0 rgba(28, 32, 34, 1),
  20px 300px 0 0 rgba(219, 222, 232, 1), 30px 300px 0 0 rgba(111, 114, 121, 1),
  40px 300px 0 0 rgba(28, 32, 34, 1), 50px 300px 0 0 rgba(48, 53, 56, 1),
  60px 300px 0 0 rgba(48, 53, 56, 1), 70px 300px 0 0 rgba(48, 53, 56, 1),
  80px 300px 0 0 rgba(48, 53, 56, 1), 90px 300px 0 0 rgba(48, 53, 56, 1),
  100px 300px 0 0 rgba(48, 53, 56, 1), 110px 300px 0 0 rgba(48, 53, 56, 1),
  120px 300px 0 0 rgba(48, 53, 56, 1), 130px 300px 0 0 rgba(48, 53, 56, 1),
  140px 300px 0 0 rgba(242, 245, 252, 1), 150px 300px 0 0 rgba(48, 53, 56, 1),
  160px 300px 0 0 rgba(48, 53, 56, 1), 170px 300px 0 0 rgba(48, 53, 56, 1),
  180px 300px 0 0 rgba(48, 53, 56, 1), 190px 300px 0 0 rgba(48, 53, 56, 1),
  200px 300px 0 0 rgba(48, 53, 56, 1), 210px 300px 0 0 rgba(48, 53, 56, 1),
  220px 300px 0 0 rgba(48, 53, 56, 1), 230px 300px 0 0 rgba(48, 53, 56, 1),
  240px 300px 0 0 rgba(48, 53, 56, 1), 250px 300px 0 0 rgba(48, 53, 56, 1),
  260px 300px 0 0 rgba(48, 53, 56, 1), 270px 300px 0 0 rgba(48, 53, 56, 1),
  280px 300px 0 0 rgba(48, 53, 56, 1), 290px 300px 0 0 rgba(48, 53, 56, 1),
  300px 300px 0 0 rgba(48, 53, 56, 1), 310px 300px 0 0 rgba(48, 53, 56, 1),
  320px 300px 0 0 rgba(48, 53, 56, 1), 330px 300px 0 0 rgba(48, 53, 56, 1),
  340px 300px 0 0 rgba(48, 53, 56, 1), 350px 300px 0 0 rgba(48, 53, 56, 1),
  360px 300px 0 0 rgba(48, 53, 56, 1), 370px 300px 0 0 rgba(48, 53, 56, 1),
  380px 300px 0 0 rgba(48, 53, 56, 1), 390px 300px 0 0 rgba(48, 53, 56, 1),
  400px 300px 0 0 rgba(48, 53, 56, 1), 410px 300px 0 0 rgba(48, 53, 56, 1),
  420px 300px 0 0 rgba(48, 53, 56, 1), 430px 300px 0 0 rgba(48, 53, 56, 1),
  440px 300px 0 0 rgba(48, 53, 56, 1), 450px 300px 0 0 rgba(48, 53, 56, 1),
  460px 300px 0 0 rgba(48, 53, 56, 1), 470px 300px 0 0 rgba(48, 53, 56, 1),
  480px 300px 0 0 rgba(48, 53, 56, 1), 490px 300px 0 0 rgba(48, 53, 56, 1),
  500px 300px 0 0 rgba(48, 53, 56, 1), 510px 300px 0 0 rgba(48, 53, 56, 1),
  520px 300px 0 0 rgba(48, 53, 56, 1), 530px 300px 0 0 rgba(48, 53, 56, 1),
  540px 300px 0 0 rgba(48, 53, 56, 1), 550px 300px 0 0 rgba(48, 53, 56, 1),
  560px 300px 0 0 rgba(48, 53, 56, 1), 570px 300px 0 0 rgba(48, 53, 56, 1),
  580px 300px 0 0 rgba(48, 53, 56, 1), 590px 300px 0 0 rgba(48, 53, 56, 1),
  600px 300px 0 0 rgba(48, 53, 56, 1), 610px 300px 0 0 rgba(48, 53, 56, 1),
  620px 300px 0 0 rgba(48, 53, 56, 1), 630px 300px 0 0 rgba(48, 53, 56, 1),
  640px 300px 0 0 rgba(48, 53, 56, 1), 650px 300px 0 0 rgba(48, 53, 56, 1),
  660px 300px 0 0 rgba(48, 53, 56, 1), 670px 300px 0 0 rgba(48, 53, 56, 1),
  680px 300px 0 0 rgba(48, 53, 56, 1), 690px 300px 0 0 rgba(48, 53, 56, 1),
  700px 300px 0 0 rgba(48, 53, 56, 1), 710px 300px 0 0 rgba(48, 53, 56, 1),
  720px 300px 0 0 rgba(48, 53, 56, 1), 730px 300px 0 0 rgba(48, 53, 56, 1),
  740px 300px 0 0 rgba(48, 53, 56, 1), 750px 300px 0 0 rgba(48, 53, 56, 1),
  760px 300px 0 0 rgba(242, 245, 252, 1), 770px 300px 0 0 rgba(48, 53, 56, 1),
  780px 300px 0 0 rgba(48, 53, 56, 1), 790px 300px 0 0 rgba(48, 53, 56, 1),
  800px 300px 0 0 rgba(48, 53, 56, 1), 810px 300px 0 0 rgba(48, 53, 56, 1),
  820px 300px 0 0 rgba(48, 53, 56, 1), 830px 300px 0 0 rgba(48, 53, 56, 1),
  840px 300px 0 0 rgba(48, 53, 56, 1), 850px 300px 0 0 rgba(48, 53, 56, 1),
  860px 300px 0 0 rgba(48, 53, 56, 1), 870px 300px 0 0 rgba(48, 53, 56, 1),
  880px 300px 0 0 rgba(48, 53, 56, 1), 890px 300px 0 0 rgba(48, 53, 56, 1),
  900px 300px 0 0 rgba(48, 53, 56, 1), 910px 300px 0 0 rgba(242, 245, 252, 1),
  920px 300px 0 0 rgba(48, 53, 56, 1), 930px 300px 0 0 rgba(48, 53, 56, 1),
  940px 300px 0 0 rgba(48, 53, 56, 1), 950px 300px 0 0 rgba(48, 53, 56, 1),
  960px 300px 0 0 rgba(48, 53, 56, 1), 970px 300px 0 0 rgba(48, 53, 56, 1),
  980px 300px 0 0 rgba(48, 53, 56, 1), 990px 300px 0 0 rgba(48, 53, 56, 1),
  1000px 300px 0 0 rgba(48, 53, 56, 1), 10px 310px 0 0 rgba(28, 32, 34, 1),
  20px 310px 0 0 rgba(219, 222, 232, 1), 30px 310px 0 0 rgba(111, 114, 121, 1),
  40px 310px 0 0 rgba(28, 32, 34, 1), 50px 310px 0 0 rgba(48, 53, 56, 1),
  60px 310px 0 0 rgba(48, 53, 56, 1), 70px 310px 0 0 rgba(48, 53, 56, 1),
  80px 310px 0 0 rgba(48, 53, 56, 1), 90px 310px 0 0 rgba(48, 53, 56, 1),
  100px 310px 0 0 rgba(48, 53, 56, 1), 110px 310px 0 0 rgba(48, 53, 56, 1),
  120px 310px 0 0 rgba(48, 53, 56, 1), 130px 310px 0 0 rgba(48, 53, 56, 1),
  140px 310px 0 0 rgba(242, 245, 252, 1), 150px 310px 0 0 rgba(48, 53, 56, 1),
  160px 310px 0 0 rgba(48, 53, 56, 1), 170px 310px 0 0 rgba(48, 53, 56, 1),
  180px 310px 0 0 rgba(48, 53, 56, 1), 190px 310px 0 0 rgba(48, 53, 56, 1),
  200px 310px 0 0 rgba(48, 53, 56, 1), 210px 310px 0 0 rgba(48, 53, 56, 1),
  220px 310px 0 0 rgba(48, 53, 56, 1), 230px 310px 0 0 rgba(48, 53, 56, 1),
  240px 310px 0 0 rgba(48, 53, 56, 1), 250px 310px 0 0 rgba(48, 53, 56, 1),
  260px 310px 0 0 rgba(48, 53, 56, 1), 270px 310px 0 0 rgba(48, 53, 56, 1),
  280px 310px 0 0 rgba(48, 53, 56, 1), 290px 310px 0 0 rgba(48, 53, 56, 1),
  300px 310px 0 0 rgba(48, 53, 56, 1), 310px 310px 0 0 rgba(48, 53, 56, 1),
  320px 310px 0 0 rgba(48, 53, 56, 1), 330px 310px 0 0 rgba(48, 53, 56, 1),
  340px 310px 0 0 rgba(48, 53, 56, 1), 350px 310px 0 0 rgba(48, 53, 56, 1),
  360px 310px 0 0 rgba(48, 53, 56, 1), 370px 310px 0 0 rgba(48, 53, 56, 1),
  380px 310px 0 0 rgba(48, 53, 56, 1), 390px 310px 0 0 rgba(48, 53, 56, 1),
  400px 310px 0 0 rgba(48, 53, 56, 1), 410px 310px 0 0 rgba(48, 53, 56, 1),
  420px 310px 0 0 rgba(48, 53, 56, 1), 430px 310px 0 0 rgba(48, 53, 56, 1),
  440px 310px 0 0 rgba(48, 53, 56, 1), 450px 310px 0 0 rgba(48, 53, 56, 1),
  460px 310px 0 0 rgba(48, 53, 56, 1), 470px 310px 0 0 rgba(48, 53, 56, 1),
  480px 310px 0 0 rgba(48, 53, 56, 1), 490px 310px 0 0 rgba(48, 53, 56, 1),
  500px 310px 0 0 rgba(48, 53, 56, 1), 510px 310px 0 0 rgba(48, 53, 56, 1),
  520px 310px 0 0 rgba(48, 53, 56, 1), 530px 310px 0 0 rgba(48, 53, 56, 1),
  540px 310px 0 0 rgba(48, 53, 56, 1), 550px 310px 0 0 rgba(48, 53, 56, 1),
  560px 310px 0 0 rgba(48, 53, 56, 1), 570px 310px 0 0 rgba(48, 53, 56, 1),
  580px 310px 0 0 rgba(48, 53, 56, 1), 590px 310px 0 0 rgba(48, 53, 56, 1),
  600px 310px 0 0 rgba(48, 53, 56, 1), 610px 310px 0 0 rgba(48, 53, 56, 1),
  620px 310px 0 0 rgba(48, 53, 56, 1), 630px 310px 0 0 rgba(48, 53, 56, 1),
  640px 310px 0 0 rgba(48, 53, 56, 1), 650px 310px 0 0 rgba(48, 53, 56, 1),
  660px 310px 0 0 rgba(48, 53, 56, 1), 670px 310px 0 0 rgba(48, 53, 56, 1),
  680px 310px 0 0 rgba(48, 53, 56, 1), 690px 310px 0 0 rgba(48, 53, 56, 1),
  700px 310px 0 0 rgba(48, 53, 56, 1), 710px 310px 0 0 rgba(48, 53, 56, 1),
  720px 310px 0 0 rgba(48, 53, 56, 1), 730px 310px 0 0 rgba(48, 53, 56, 1),
  740px 310px 0 0 rgba(48, 53, 56, 1), 750px 310px 0 0 rgba(48, 53, 56, 1),
  760px 310px 0 0 rgba(242, 245, 252, 1), 770px 310px 0 0 rgba(48, 53, 56, 1),
  780px 310px 0 0 rgba(48, 53, 56, 1), 790px 310px 0 0 rgba(48, 53, 56, 1),
  800px 310px 0 0 rgba(48, 53, 56, 1), 810px 310px 0 0 rgba(48, 53, 56, 1),
  820px 310px 0 0 rgba(48, 53, 56, 1), 830px 310px 0 0 rgba(48, 53, 56, 1),
  840px 310px 0 0 rgba(48, 53, 56, 1), 850px 310px 0 0 rgba(48, 53, 56, 1),
  860px 310px 0 0 rgba(48, 53, 56, 1), 870px 310px 0 0 rgba(48, 53, 56, 1),
  880px 310px 0 0 rgba(48, 53, 56, 1), 890px 310px 0 0 rgba(48, 53, 56, 1),
  900px 310px 0 0 rgba(242, 245, 252, 1), 910px 310px 0 0 rgba(48, 53, 56, 1),
  920px 310px 0 0 rgba(48, 53, 56, 1), 930px 310px 0 0 rgba(48, 53, 56, 1),
  940px 310px 0 0 rgba(48, 53, 56, 1), 950px 310px 0 0 rgba(48, 53, 56, 1),
  960px 310px 0 0 rgba(48, 53, 56, 1), 970px 310px 0 0 rgba(48, 53, 56, 1),
  980px 310px 0 0 rgba(48, 53, 56, 1), 990px 310px 0 0 rgba(48, 53, 56, 1),
  1000px 310px 0 0 rgba(48, 53, 56, 1), 10px 320px 0 0 rgba(28, 32, 34, 1),
  20px 320px 0 0 rgba(219, 222, 232, 1), 30px 320px 0 0 rgba(111, 114, 121, 1),
  40px 320px 0 0 rgba(28, 32, 34, 1), 50px 320px 0 0 rgba(48, 53, 56, 1),
  60px 320px 0 0 rgba(48, 53, 56, 1), 70px 320px 0 0 rgba(48, 53, 56, 1),
  80px 320px 0 0 rgba(48, 53, 56, 1), 90px 320px 0 0 rgba(48, 53, 56, 1),
  100px 320px 0 0 rgba(48, 53, 56, 1), 110px 320px 0 0 rgba(48, 53, 56, 1),
  120px 320px 0 0 rgba(48, 53, 56, 1), 130px 320px 0 0 rgba(48, 53, 56, 1),
  140px 320px 0 0 rgba(242, 245, 252, 1), 150px 320px 0 0 rgba(48, 53, 56, 1),
  160px 320px 0 0 rgba(48, 53, 56, 1), 170px 320px 0 0 rgba(48, 53, 56, 1),
  180px 320px 0 0 rgba(48, 53, 56, 1), 190px 320px 0 0 rgba(48, 53, 56, 1),
  200px 320px 0 0 rgba(48, 53, 56, 1), 210px 320px 0 0 rgba(48, 53, 56, 1),
  220px 320px 0 0 rgba(48, 53, 56, 1), 230px 320px 0 0 rgba(48, 53, 56, 1),
  240px 320px 0 0 rgba(48, 53, 56, 1), 250px 320px 0 0 rgba(48, 53, 56, 1),
  260px 320px 0 0 rgba(48, 53, 56, 1), 270px 320px 0 0 rgba(48, 53, 56, 1),
  280px 320px 0 0 rgba(48, 53, 56, 1), 290px 320px 0 0 rgba(48, 53, 56, 1),
  300px 320px 0 0 rgba(48, 53, 56, 1), 310px 320px 0 0 rgba(48, 53, 56, 1),
  320px 320px 0 0 rgba(48, 53, 56, 1), 330px 320px 0 0 rgba(48, 53, 56, 1),
  340px 320px 0 0 rgba(48, 53, 56, 1), 350px 320px 0 0 rgba(48, 53, 56, 1),
  360px 320px 0 0 rgba(48, 53, 56, 1), 370px 320px 0 0 rgba(48, 53, 56, 1),
  380px 320px 0 0 rgba(48, 53, 56, 1), 390px 320px 0 0 rgba(48, 53, 56, 1),
  400px 320px 0 0 rgba(48, 53, 56, 1), 410px 320px 0 0 rgba(48, 53, 56, 1),
  420px 320px 0 0 rgba(48, 53, 56, 1), 430px 320px 0 0 rgba(48, 53, 56, 1),
  440px 320px 0 0 rgba(48, 53, 56, 1), 450px 320px 0 0 rgba(48, 53, 56, 1),
  460px 320px 0 0 rgba(48, 53, 56, 1), 470px 320px 0 0 rgba(48, 53, 56, 1),
  480px 320px 0 0 rgba(48, 53, 56, 1), 490px 320px 0 0 rgba(48, 53, 56, 1),
  500px 320px 0 0 rgba(48, 53, 56, 1), 510px 320px 0 0 rgba(48, 53, 56, 1),
  520px 320px 0 0 rgba(48, 53, 56, 1), 530px 320px 0 0 rgba(48, 53, 56, 1),
  540px 320px 0 0 rgba(48, 53, 56, 1), 550px 320px 0 0 rgba(48, 53, 56, 1),
  560px 320px 0 0 rgba(48, 53, 56, 1), 570px 320px 0 0 rgba(48, 53, 56, 1),
  580px 320px 0 0 rgba(48, 53, 56, 1), 590px 320px 0 0 rgba(48, 53, 56, 1),
  600px 320px 0 0 rgba(48, 53, 56, 1), 610px 320px 0 0 rgba(48, 53, 56, 1),
  620px 320px 0 0 rgba(48, 53, 56, 1), 630px 320px 0 0 rgba(48, 53, 56, 1),
  640px 320px 0 0 rgba(48, 53, 56, 1), 650px 320px 0 0 rgba(48, 53, 56, 1),
  660px 320px 0 0 rgba(48, 53, 56, 1), 670px 320px 0 0 rgba(48, 53, 56, 1),
  680px 320px 0 0 rgba(48, 53, 56, 1), 690px 320px 0 0 rgba(48, 53, 56, 1),
  700px 320px 0 0 rgba(48, 53, 56, 1), 710px 320px 0 0 rgba(48, 53, 56, 1),
  720px 320px 0 0 rgba(48, 53, 56, 1), 730px 320px 0 0 rgba(48, 53, 56, 1),
  740px 320px 0 0 rgba(48, 53, 56, 1), 750px 320px 0 0 rgba(48, 53, 56, 1),
  760px 320px 0 0 rgba(242, 245, 252, 1), 770px 320px 0 0 rgba(48, 53, 56, 1),
  780px 320px 0 0 rgba(48, 53, 56, 1), 790px 320px 0 0 rgba(48, 53, 56, 1),
  800px 320px 0 0 rgba(48, 53, 56, 1), 810px 320px 0 0 rgba(48, 53, 56, 1),
  820px 320px 0 0 rgba(48, 53, 56, 1), 830px 320px 0 0 rgba(48, 53, 56, 1),
  840px 320px 0 0 rgba(48, 53, 56, 1), 850px 320px 0 0 rgba(48, 53, 56, 1),
  860px 320px 0 0 rgba(48, 53, 56, 1), 870px 320px 0 0 rgba(48, 53, 56, 1),
  880px 320px 0 0 rgba(48, 53, 56, 1), 890px 320px 0 0 rgba(242, 245, 252, 1),
  900px 320px 0 0 rgba(48, 53, 56, 1), 910px 320px 0 0 rgba(48, 53, 56, 1),
  920px 320px 0 0 rgba(48, 53, 56, 1), 930px 320px 0 0 rgba(48, 53, 56, 1),
  940px 320px 0 0 rgba(48, 53, 56, 1), 950px 320px 0 0 rgba(48, 53, 56, 1),
  960px 320px 0 0 rgba(48, 53, 56, 1), 970px 320px 0 0 rgba(48, 53, 56, 1),
  980px 320px 0 0 rgba(48, 53, 56, 1), 990px 320px 0 0 rgba(48, 53, 56, 1),
  1000px 320px 0 0 rgba(48, 53, 56, 1), 10px 330px 0 0 rgba(28, 32, 34, 1),
  20px 330px 0 0 rgba(219, 222, 232, 1), 30px 330px 0 0 rgba(111, 114, 121, 1),
  40px 330px 0 0 rgba(28, 32, 34, 1), 50px 330px 0 0 rgba(48, 53, 56, 1),
  60px 330px 0 0 rgba(48, 53, 56, 1), 70px 330px 0 0 rgba(48, 53, 56, 1),
  80px 330px 0 0 rgba(48, 53, 56, 1), 90px 330px 0 0 rgba(48, 53, 56, 1),
  100px 330px 0 0 rgba(48, 53, 56, 1), 110px 330px 0 0 rgba(48, 53, 56, 1),
  120px 330px 0 0 rgba(48, 53, 56, 1), 130px 330px 0 0 rgba(48, 53, 56, 1),
  140px 330px 0 0 rgba(242, 245, 252, 1), 150px 330px 0 0 rgba(48, 53, 56, 1),
  160px 330px 0 0 rgba(48, 53, 56, 1), 170px 330px 0 0 rgba(48, 53, 56, 1),
  180px 330px 0 0 rgba(48, 53, 56, 1), 190px 330px 0 0 rgba(48, 53, 56, 1),
  200px 330px 0 0 rgba(48, 53, 56, 1), 210px 330px 0 0 rgba(48, 53, 56, 1),
  220px 330px 0 0 rgba(48, 53, 56, 1), 230px 330px 0 0 rgba(48, 53, 56, 1),
  240px 330px 0 0 rgba(48, 53, 56, 1), 250px 330px 0 0 rgba(48, 53, 56, 1),
  260px 330px 0 0 rgba(48, 53, 56, 1), 270px 330px 0 0 rgba(48, 53, 56, 1),
  280px 330px 0 0 rgba(48, 53, 56, 1), 290px 330px 0 0 rgba(48, 53, 56, 1),
  300px 330px 0 0 rgba(48, 53, 56, 1), 310px 330px 0 0 rgba(48, 53, 56, 1),
  320px 330px 0 0 rgba(48, 53, 56, 1), 330px 330px 0 0 rgba(48, 53, 56, 1),
  340px 330px 0 0 rgba(48, 53, 56, 1), 350px 330px 0 0 rgba(48, 53, 56, 1),
  360px 330px 0 0 rgba(48, 53, 56, 1), 370px 330px 0 0 rgba(48, 53, 56, 1),
  380px 330px 0 0 rgba(48, 53, 56, 1), 390px 330px 0 0 rgba(48, 53, 56, 1),
  400px 330px 0 0 rgba(48, 53, 56, 1), 410px 330px 0 0 rgba(48, 53, 56, 1),
  420px 330px 0 0 rgba(48, 53, 56, 1), 430px 330px 0 0 rgba(48, 53, 56, 1),
  440px 330px 0 0 rgba(48, 53, 56, 1), 450px 330px 0 0 rgba(48, 53, 56, 1),
  460px 330px 0 0 rgba(48, 53, 56, 1), 470px 330px 0 0 rgba(48, 53, 56, 1),
  480px 330px 0 0 rgba(48, 53, 56, 1), 490px 330px 0 0 rgba(48, 53, 56, 1),
  500px 330px 0 0 rgba(48, 53, 56, 1), 510px 330px 0 0 rgba(48, 53, 56, 1),
  520px 330px 0 0 rgba(48, 53, 56, 1), 530px 330px 0 0 rgba(48, 53, 56, 1),
  540px 330px 0 0 rgba(48, 53, 56, 1), 550px 330px 0 0 rgba(48, 53, 56, 1),
  560px 330px 0 0 rgba(48, 53, 56, 1), 570px 330px 0 0 rgba(48, 53, 56, 1),
  580px 330px 0 0 rgba(48, 53, 56, 1), 590px 330px 0 0 rgba(48, 53, 56, 1),
  600px 330px 0 0 rgba(48, 53, 56, 1), 610px 330px 0 0 rgba(48, 53, 56, 1),
  620px 330px 0 0 rgba(48, 53, 56, 1), 630px 330px 0 0 rgba(48, 53, 56, 1),
  640px 330px 0 0 rgba(48, 53, 56, 1), 650px 330px 0 0 rgba(48, 53, 56, 1),
  660px 330px 0 0 rgba(48, 53, 56, 1), 670px 330px 0 0 rgba(48, 53, 56, 1),
  680px 330px 0 0 rgba(48, 53, 56, 1), 690px 330px 0 0 rgba(48, 53, 56, 1),
  700px 330px 0 0 rgba(48, 53, 56, 1), 710px 330px 0 0 rgba(48, 53, 56, 1),
  720px 330px 0 0 rgba(48, 53, 56, 1), 730px 330px 0 0 rgba(48, 53, 56, 1),
  740px 330px 0 0 rgba(48, 53, 56, 1), 750px 330px 0 0 rgba(48, 53, 56, 1),
  760px 330px 0 0 rgba(242, 245, 252, 1), 770px 330px 0 0 rgba(48, 53, 56, 1),
  780px 330px 0 0 rgba(48, 53, 56, 1), 790px 330px 0 0 rgba(48, 53, 56, 1),
  800px 330px 0 0 rgba(48, 53, 56, 1), 810px 330px 0 0 rgba(48, 53, 56, 1),
  820px 330px 0 0 rgba(48, 53, 56, 1), 830px 330px 0 0 rgba(48, 53, 56, 1),
  840px 330px 0 0 rgba(48, 53, 56, 1), 850px 330px 0 0 rgba(48, 53, 56, 1),
  860px 330px 0 0 rgba(48, 53, 56, 1), 870px 330px 0 0 rgba(48, 53, 56, 1),
  880px 330px 0 0 rgba(242, 245, 252, 1), 890px 330px 0 0 rgba(48, 53, 56, 1),
  900px 330px 0 0 rgba(48, 53, 56, 1), 910px 330px 0 0 rgba(48, 53, 56, 1),
  920px 330px 0 0 rgba(48, 53, 56, 1), 930px 330px 0 0 rgba(48, 53, 56, 1),
  940px 330px 0 0 rgba(48, 53, 56, 1), 950px 330px 0 0 rgba(48, 53, 56, 1),
  960px 330px 0 0 rgba(48, 53, 56, 1), 970px 330px 0 0 rgba(48, 53, 56, 1),
  980px 330px 0 0 rgba(48, 53, 56, 1), 990px 330px 0 0 rgba(48, 53, 56, 1),
  1000px 330px 0 0 rgba(48, 53, 56, 1), 10px 340px 0 0 rgba(28, 32, 34, 1),
  20px 340px 0 0 rgba(219, 222, 232, 1), 30px 340px 0 0 rgba(111, 114, 121, 1),
  40px 340px 0 0 rgba(28, 32, 34, 1), 50px 340px 0 0 rgba(48, 53, 56, 1),
  60px 340px 0 0 rgba(48, 53, 56, 1), 70px 340px 0 0 rgba(48, 53, 56, 1),
  80px 340px 0 0 rgba(48, 53, 56, 1), 90px 340px 0 0 rgba(48, 53, 56, 1),
  100px 340px 0 0 rgba(48, 53, 56, 1), 110px 340px 0 0 rgba(48, 53, 56, 1),
  120px 340px 0 0 rgba(48, 53, 56, 1), 130px 340px 0 0 rgba(48, 53, 56, 1),
  140px 340px 0 0 rgba(242, 245, 252, 1), 150px 340px 0 0 rgba(48, 53, 56, 1),
  160px 340px 0 0 rgba(48, 53, 56, 1), 170px 340px 0 0 rgba(48, 53, 56, 1),
  180px 340px 0 0 rgba(48, 53, 56, 1), 190px 340px 0 0 rgba(48, 53, 56, 1),
  200px 340px 0 0 rgba(48, 53, 56, 1), 210px 340px 0 0 rgba(48, 53, 56, 1),
  220px 340px 0 0 rgba(48, 53, 56, 1), 230px 340px 0 0 rgba(48, 53, 56, 1),
  240px 340px 0 0 rgba(48, 53, 56, 1), 250px 340px 0 0 rgba(48, 53, 56, 1),
  260px 340px 0 0 rgba(48, 53, 56, 1), 270px 340px 0 0 rgba(48, 53, 56, 1),
  280px 340px 0 0 rgba(48, 53, 56, 1), 290px 340px 0 0 rgba(48, 53, 56, 1),
  300px 340px 0 0 rgba(48, 53, 56, 1), 310px 340px 0 0 rgba(48, 53, 56, 1),
  320px 340px 0 0 rgba(48, 53, 56, 1), 330px 340px 0 0 rgba(48, 53, 56, 1),
  340px 340px 0 0 rgba(48, 53, 56, 1), 350px 340px 0 0 rgba(48, 53, 56, 1),
  360px 340px 0 0 rgba(48, 53, 56, 1), 370px 340px 0 0 rgba(48, 53, 56, 1),
  380px 340px 0 0 rgba(48, 53, 56, 1), 390px 340px 0 0 rgba(48, 53, 56, 1),
  400px 340px 0 0 rgba(48, 53, 56, 1), 410px 340px 0 0 rgba(48, 53, 56, 1),
  420px 340px 0 0 rgba(48, 53, 56, 1), 430px 340px 0 0 rgba(48, 53, 56, 1),
  440px 340px 0 0 rgba(48, 53, 56, 1), 450px 340px 0 0 rgba(48, 53, 56, 1),
  460px 340px 0 0 rgba(48, 53, 56, 1), 470px 340px 0 0 rgba(48, 53, 56, 1),
  480px 340px 0 0 rgba(48, 53, 56, 1), 490px 340px 0 0 rgba(48, 53, 56, 1),
  500px 340px 0 0 rgba(48, 53, 56, 1), 510px 340px 0 0 rgba(48, 53, 56, 1),
  520px 340px 0 0 rgba(48, 53, 56, 1), 530px 340px 0 0 rgba(48, 53, 56, 1),
  540px 340px 0 0 rgba(48, 53, 56, 1), 550px 340px 0 0 rgba(48, 53, 56, 1),
  560px 340px 0 0 rgba(48, 53, 56, 1), 570px 340px 0 0 rgba(48, 53, 56, 1),
  580px 340px 0 0 rgba(48, 53, 56, 1), 590px 340px 0 0 rgba(48, 53, 56, 1),
  600px 340px 0 0 rgba(48, 53, 56, 1), 610px 340px 0 0 rgba(48, 53, 56, 1),
  620px 340px 0 0 rgba(48, 53, 56, 1), 630px 340px 0 0 rgba(48, 53, 56, 1),
  640px 340px 0 0 rgba(48, 53, 56, 1), 650px 340px 0 0 rgba(48, 53, 56, 1),
  660px 340px 0 0 rgba(48, 53, 56, 1), 670px 340px 0 0 rgba(48, 53, 56, 1),
  680px 340px 0 0 rgba(48, 53, 56, 1), 690px 340px 0 0 rgba(48, 53, 56, 1),
  700px 340px 0 0 rgba(48, 53, 56, 1), 710px 340px 0 0 rgba(48, 53, 56, 1),
  720px 340px 0 0 rgba(48, 53, 56, 1), 730px 340px 0 0 rgba(48, 53, 56, 1),
  740px 340px 0 0 rgba(48, 53, 56, 1), 750px 340px 0 0 rgba(48, 53, 56, 1),
  760px 340px 0 0 rgba(242, 245, 252, 1), 770px 340px 0 0 rgba(48, 53, 56, 1),
  780px 340px 0 0 rgba(48, 53, 56, 1), 790px 340px 0 0 rgba(48, 53, 56, 1),
  800px 340px 0 0 rgba(48, 53, 56, 1), 810px 340px 0 0 rgba(48, 53, 56, 1),
  820px 340px 0 0 rgba(48, 53, 56, 1), 830px 340px 0 0 rgba(48, 53, 56, 1),
  840px 340px 0 0 rgba(48, 53, 56, 1), 850px 340px 0 0 rgba(48, 53, 56, 1),
  860px 340px 0 0 rgba(48, 53, 56, 1), 870px 340px 0 0 rgba(242, 245, 252, 1),
  880px 340px 0 0 rgba(48, 53, 56, 1), 890px 340px 0 0 rgba(48, 53, 56, 1),
  900px 340px 0 0 rgba(48, 53, 56, 1), 910px 340px 0 0 rgba(48, 53, 56, 1),
  920px 340px 0 0 rgba(48, 53, 56, 1), 930px 340px 0 0 rgba(48, 53, 56, 1),
  940px 340px 0 0 rgba(48, 53, 56, 1), 950px 340px 0 0 rgba(48, 53, 56, 1),
  960px 340px 0 0 rgba(48, 53, 56, 1), 970px 340px 0 0 rgba(48, 53, 56, 1),
  980px 340px 0 0 rgba(48, 53, 56, 1), 990px 340px 0 0 rgba(48, 53, 56, 1),
  1000px 340px 0 0 rgba(48, 53, 56, 1), 10px 350px 0 0 rgba(28, 32, 34, 1),
  20px 350px 0 0 rgba(219, 222, 232, 1), 30px 350px 0 0 rgba(111, 114, 121, 1),
  40px 350px 0 0 rgba(28, 32, 34, 1), 50px 350px 0 0 rgba(48, 53, 56, 1),
  60px 350px 0 0 rgba(48, 53, 56, 1), 70px 350px 0 0 rgba(48, 53, 56, 1),
  80px 350px 0 0 rgba(48, 53, 56, 1), 90px 350px 0 0 rgba(48, 53, 56, 1),
  100px 350px 0 0 rgba(48, 53, 56, 1), 110px 350px 0 0 rgba(48, 53, 56, 1),
  120px 350px 0 0 rgba(48, 53, 56, 1), 130px 350px 0 0 rgba(48, 53, 56, 1),
  140px 350px 0 0 rgba(242, 245, 252, 1), 150px 350px 0 0 rgba(48, 53, 56, 1),
  160px 350px 0 0 rgba(48, 53, 56, 1), 170px 350px 0 0 rgba(48, 53, 56, 1),
  180px 350px 0 0 rgba(48, 53, 56, 1), 190px 350px 0 0 rgba(48, 53, 56, 1),
  200px 350px 0 0 rgba(48, 53, 56, 1), 210px 350px 0 0 rgba(48, 53, 56, 1),
  220px 350px 0 0 rgba(48, 53, 56, 1), 230px 350px 0 0 rgba(48, 53, 56, 1),
  240px 350px 0 0 rgba(48, 53, 56, 1), 250px 350px 0 0 rgba(48, 53, 56, 1),
  260px 350px 0 0 rgba(48, 53, 56, 1), 270px 350px 0 0 rgba(48, 53, 56, 1),
  280px 350px 0 0 rgba(48, 53, 56, 1), 290px 350px 0 0 rgba(48, 53, 56, 1),
  300px 350px 0 0 rgba(48, 53, 56, 1), 310px 350px 0 0 rgba(48, 53, 56, 1),
  320px 350px 0 0 rgba(48, 53, 56, 1), 330px 350px 0 0 rgba(48, 53, 56, 1),
  340px 350px 0 0 rgba(48, 53, 56, 1), 350px 350px 0 0 rgba(48, 53, 56, 1),
  360px 350px 0 0 rgba(48, 53, 56, 1), 370px 350px 0 0 rgba(48, 53, 56, 1),
  380px 350px 0 0 rgba(48, 53, 56, 1), 390px 350px 0 0 rgba(48, 53, 56, 1),
  400px 350px 0 0 rgba(48, 53, 56, 1), 410px 350px 0 0 rgba(48, 53, 56, 1),
  420px 350px 0 0 rgba(48, 53, 56, 1), 430px 350px 0 0 rgba(48, 53, 56, 1),
  440px 350px 0 0 rgba(48, 53, 56, 1), 450px 350px 0 0 rgba(48, 53, 56, 1),
  460px 350px 0 0 rgba(48, 53, 56, 1), 470px 350px 0 0 rgba(48, 53, 56, 1),
  480px 350px 0 0 rgba(48, 53, 56, 1), 490px 350px 0 0 rgba(48, 53, 56, 1),
  500px 350px 0 0 rgba(48, 53, 56, 1), 510px 350px 0 0 rgba(48, 53, 56, 1),
  520px 350px 0 0 rgba(48, 53, 56, 1), 530px 350px 0 0 rgba(48, 53, 56, 1),
  540px 350px 0 0 rgba(48, 53, 56, 1), 550px 350px 0 0 rgba(48, 53, 56, 1),
  560px 350px 0 0 rgba(48, 53, 56, 1), 570px 350px 0 0 rgba(48, 53, 56, 1),
  580px 350px 0 0 rgba(48, 53, 56, 1), 590px 350px 0 0 rgba(48, 53, 56, 1),
  600px 350px 0 0 rgba(48, 53, 56, 1), 610px 350px 0 0 rgba(48, 53, 56, 1),
  620px 350px 0 0 rgba(48, 53, 56, 1), 630px 350px 0 0 rgba(48, 53, 56, 1),
  640px 350px 0 0 rgba(48, 53, 56, 1), 650px 350px 0 0 rgba(48, 53, 56, 1),
  660px 350px 0 0 rgba(48, 53, 56, 1), 670px 350px 0 0 rgba(48, 53, 56, 1),
  680px 350px 0 0 rgba(48, 53, 56, 1), 690px 350px 0 0 rgba(48, 53, 56, 1),
  700px 350px 0 0 rgba(48, 53, 56, 1), 710px 350px 0 0 rgba(48, 53, 56, 1),
  720px 350px 0 0 rgba(48, 53, 56, 1), 730px 350px 0 0 rgba(48, 53, 56, 1),
  740px 350px 0 0 rgba(48, 53, 56, 1), 750px 350px 0 0 rgba(48, 53, 56, 1),
  760px 350px 0 0 rgba(242, 245, 252, 1), 770px 350px 0 0 rgba(48, 53, 56, 1),
  780px 350px 0 0 rgba(48, 53, 56, 1), 790px 350px 0 0 rgba(48, 53, 56, 1),
  800px 350px 0 0 rgba(48, 53, 56, 1), 810px 350px 0 0 rgba(48, 53, 56, 1),
  820px 350px 0 0 rgba(48, 53, 56, 1), 830px 350px 0 0 rgba(48, 53, 56, 1),
  840px 350px 0 0 rgba(48, 53, 56, 1), 850px 350px 0 0 rgba(48, 53, 56, 1),
  860px 350px 0 0 rgba(242, 245, 252, 1), 870px 350px 0 0 rgba(48, 53, 56, 1),
  880px 350px 0 0 rgba(48, 53, 56, 1), 890px 350px 0 0 rgba(48, 53, 56, 1),
  900px 350px 0 0 rgba(48, 53, 56, 1), 910px 350px 0 0 rgba(48, 53, 56, 1),
  920px 350px 0 0 rgba(48, 53, 56, 1), 930px 350px 0 0 rgba(48, 53, 56, 1),
  940px 350px 0 0 rgba(48, 53, 56, 1), 950px 350px 0 0 rgba(48, 53, 56, 1),
  960px 350px 0 0 rgba(48, 53, 56, 1), 970px 350px 0 0 rgba(48, 53, 56, 1),
  980px 350px 0 0 rgba(48, 53, 56, 1), 990px 350px 0 0 rgba(48, 53, 56, 1),
  1000px 350px 0 0 rgba(48, 53, 56, 1), 10px 360px 0 0 rgba(28, 32, 34, 1),
  20px 360px 0 0 rgba(219, 222, 232, 1), 30px 360px 0 0 rgba(111, 114, 121, 1),
  40px 360px 0 0 rgba(28, 32, 34, 1), 50px 360px 0 0 rgba(48, 53, 56, 1),
  60px 360px 0 0 rgba(48, 53, 56, 1), 70px 360px 0 0 rgba(48, 53, 56, 1),
  80px 360px 0 0 rgba(48, 53, 56, 1), 90px 360px 0 0 rgba(48, 53, 56, 1),
  100px 360px 0 0 rgba(48, 53, 56, 1), 110px 360px 0 0 rgba(48, 53, 56, 1),
  120px 360px 0 0 rgba(48, 53, 56, 1), 130px 360px 0 0 rgba(48, 53, 56, 1),
  140px 360px 0 0 rgba(242, 245, 252, 1), 150px 360px 0 0 rgba(48, 53, 56, 1),
  160px 360px 0 0 rgba(48, 53, 56, 1), 170px 360px 0 0 rgba(48, 53, 56, 1),
  180px 360px 0 0 rgba(48, 53, 56, 1), 190px 360px 0 0 rgba(48, 53, 56, 1),
  200px 360px 0 0 rgba(48, 53, 56, 1), 210px 360px 0 0 rgba(48, 53, 56, 1),
  220px 360px 0 0 rgba(48, 53, 56, 1), 230px 360px 0 0 rgba(48, 53, 56, 1),
  240px 360px 0 0 rgba(48, 53, 56, 1), 250px 360px 0 0 rgba(48, 53, 56, 1),
  260px 360px 0 0 rgba(48, 53, 56, 1), 270px 360px 0 0 rgba(48, 53, 56, 1),
  280px 360px 0 0 rgba(48, 53, 56, 1), 290px 360px 0 0 rgba(48, 53, 56, 1),
  300px 360px 0 0 rgba(48, 53, 56, 1), 310px 360px 0 0 rgba(48, 53, 56, 1),
  320px 360px 0 0 rgba(48, 53, 56, 1), 330px 360px 0 0 rgba(48, 53, 56, 1),
  340px 360px 0 0 rgba(48, 53, 56, 1), 350px 360px 0 0 rgba(48, 53, 56, 1),
  360px 360px 0 0 rgba(48, 53, 56, 1), 370px 360px 0 0 rgba(48, 53, 56, 1),
  380px 360px 0 0 rgba(48, 53, 56, 1), 390px 360px 0 0 rgba(48, 53, 56, 1),
  400px 360px 0 0 rgba(48, 53, 56, 1), 410px 360px 0 0 rgba(48, 53, 56, 1),
  420px 360px 0 0 rgba(48, 53, 56, 1), 430px 360px 0 0 rgba(48, 53, 56, 1),
  440px 360px 0 0 rgba(48, 53, 56, 1), 450px 360px 0 0 rgba(48, 53, 56, 1),
  460px 360px 0 0 rgba(48, 53, 56, 1), 470px 360px 0 0 rgba(48, 53, 56, 1),
  480px 360px 0 0 rgba(48, 53, 56, 1), 490px 360px 0 0 rgba(48, 53, 56, 1),
  500px 360px 0 0 rgba(48, 53, 56, 1), 510px 360px 0 0 rgba(48, 53, 56, 1),
  520px 360px 0 0 rgba(48, 53, 56, 1), 530px 360px 0 0 rgba(48, 53, 56, 1),
  540px 360px 0 0 rgba(48, 53, 56, 1), 550px 360px 0 0 rgba(48, 53, 56, 1),
  560px 360px 0 0 rgba(48, 53, 56, 1), 570px 360px 0 0 rgba(48, 53, 56, 1),
  580px 360px 0 0 rgba(48, 53, 56, 1), 590px 360px 0 0 rgba(48, 53, 56, 1),
  600px 360px 0 0 rgba(48, 53, 56, 1), 610px 360px 0 0 rgba(48, 53, 56, 1),
  620px 360px 0 0 rgba(48, 53, 56, 1), 630px 360px 0 0 rgba(48, 53, 56, 1),
  640px 360px 0 0 rgba(48, 53, 56, 1), 650px 360px 0 0 rgba(48, 53, 56, 1),
  660px 360px 0 0 rgba(48, 53, 56, 1), 670px 360px 0 0 rgba(48, 53, 56, 1),
  680px 360px 0 0 rgba(48, 53, 56, 1), 690px 360px 0 0 rgba(48, 53, 56, 1),
  700px 360px 0 0 rgba(48, 53, 56, 1), 710px 360px 0 0 rgba(48, 53, 56, 1),
  720px 360px 0 0 rgba(48, 53, 56, 1), 730px 360px 0 0 rgba(48, 53, 56, 1),
  740px 360px 0 0 rgba(48, 53, 56, 1), 750px 360px 0 0 rgba(48, 53, 56, 1),
  760px 360px 0 0 rgba(242, 245, 252, 1), 770px 360px 0 0 rgba(48, 53, 56, 1),
  780px 360px 0 0 rgba(48, 53, 56, 1), 790px 360px 0 0 rgba(48, 53, 56, 1),
  800px 360px 0 0 rgba(48, 53, 56, 1), 810px 360px 0 0 rgba(48, 53, 56, 1),
  820px 360px 0 0 rgba(48, 53, 56, 1), 830px 360px 0 0 rgba(48, 53, 56, 1),
  840px 360px 0 0 rgba(48, 53, 56, 1), 850px 360px 0 0 rgba(242, 245, 252, 1),
  860px 360px 0 0 rgba(48, 53, 56, 1), 870px 360px 0 0 rgba(48, 53, 56, 1),
  880px 360px 0 0 rgba(48, 53, 56, 1), 890px 360px 0 0 rgba(48, 53, 56, 1),
  900px 360px 0 0 rgba(48, 53, 56, 1), 910px 360px 0 0 rgba(48, 53, 56, 1),
  920px 360px 0 0 rgba(48, 53, 56, 1), 930px 360px 0 0 rgba(48, 53, 56, 1),
  940px 360px 0 0 rgba(48, 53, 56, 1), 950px 360px 0 0 rgba(48, 53, 56, 1),
  960px 360px 0 0 rgba(48, 53, 56, 1), 970px 360px 0 0 rgba(48, 53, 56, 1),
  980px 360px 0 0 rgba(48, 53, 56, 1), 990px 360px 0 0 rgba(48, 53, 56, 1),
  1000px 360px 0 0 rgba(48, 53, 56, 1), 10px 370px 0 0 rgba(28, 32, 34, 1),
  20px 370px 0 0 rgba(219, 222, 232, 1), 30px 370px 0 0 rgba(111, 114, 121, 1),
  40px 370px 0 0 rgba(28, 32, 34, 1), 50px 370px 0 0 rgba(48, 53, 56, 1),
  60px 370px 0 0 rgba(48, 53, 56, 1), 70px 370px 0 0 rgba(48, 53, 56, 1),
  80px 370px 0 0 rgba(48, 53, 56, 1), 90px 370px 0 0 rgba(48, 53, 56, 1),
  100px 370px 0 0 rgba(48, 53, 56, 1), 110px 370px 0 0 rgba(48, 53, 56, 1),
  120px 370px 0 0 rgba(48, 53, 56, 1), 130px 370px 0 0 rgba(48, 53, 56, 1),
  140px 370px 0 0 rgba(48, 53, 56, 1), 150px 370px 0 0 rgba(48, 53, 56, 1),
  160px 370px 0 0 rgba(48, 53, 56, 1), 170px 370px 0 0 rgba(48, 53, 56, 1),
  180px 370px 0 0 rgba(48, 53, 56, 1), 190px 370px 0 0 rgba(48, 53, 56, 1),
  200px 370px 0 0 rgba(48, 53, 56, 1), 210px 370px 0 0 rgba(48, 53, 56, 1),
  220px 370px 0 0 rgba(48, 53, 56, 1), 230px 370px 0 0 rgba(48, 53, 56, 1),
  240px 370px 0 0 rgba(48, 53, 56, 1), 250px 370px 0 0 rgba(48, 53, 56, 1),
  260px 370px 0 0 rgba(48, 53, 56, 1), 270px 370px 0 0 rgba(48, 53, 56, 1),
  280px 370px 0 0 rgba(48, 53, 56, 1), 290px 370px 0 0 rgba(48, 53, 56, 1),
  300px 370px 0 0 rgba(48, 53, 56, 1), 310px 370px 0 0 rgba(48, 53, 56, 1),
  320px 370px 0 0 rgba(48, 53, 56, 1), 330px 370px 0 0 rgba(48, 53, 56, 1),
  340px 370px 0 0 rgba(48, 53, 56, 1), 350px 370px 0 0 rgba(48, 53, 56, 1),
  360px 370px 0 0 rgba(48, 53, 56, 1), 370px 370px 0 0 rgba(48, 53, 56, 1),
  380px 370px 0 0 rgba(48, 53, 56, 1), 390px 370px 0 0 rgba(48, 53, 56, 1),
  400px 370px 0 0 rgba(48, 53, 56, 1), 410px 370px 0 0 rgba(48, 53, 56, 1),
  420px 370px 0 0 rgba(48, 53, 56, 1), 430px 370px 0 0 rgba(48, 53, 56, 1),
  440px 370px 0 0 rgba(48, 53, 56, 1), 450px 370px 0 0 rgba(48, 53, 56, 1),
  460px 370px 0 0 rgba(48, 53, 56, 1), 470px 370px 0 0 rgba(48, 53, 56, 1),
  480px 370px 0 0 rgba(48, 53, 56, 1), 490px 370px 0 0 rgba(48, 53, 56, 1),
  500px 370px 0 0 rgba(48, 53, 56, 1), 510px 370px 0 0 rgba(48, 53, 56, 1),
  520px 370px 0 0 rgba(48, 53, 56, 1), 530px 370px 0 0 rgba(48, 53, 56, 1),
  540px 370px 0 0 rgba(48, 53, 56, 1), 550px 370px 0 0 rgba(48, 53, 56, 1),
  560px 370px 0 0 rgba(48, 53, 56, 1), 570px 370px 0 0 rgba(48, 53, 56, 1),
  580px 370px 0 0 rgba(48, 53, 56, 1), 590px 370px 0 0 rgba(48, 53, 56, 1),
  600px 370px 0 0 rgba(48, 53, 56, 1), 610px 370px 0 0 rgba(48, 53, 56, 1),
  620px 370px 0 0 rgba(48, 53, 56, 1), 630px 370px 0 0 rgba(48, 53, 56, 1),
  640px 370px 0 0 rgba(48, 53, 56, 1), 650px 370px 0 0 rgba(48, 53, 56, 1),
  660px 370px 0 0 rgba(48, 53, 56, 1), 670px 370px 0 0 rgba(48, 53, 56, 1),
  680px 370px 0 0 rgba(48, 53, 56, 1), 690px 370px 0 0 rgba(48, 53, 56, 1),
  700px 370px 0 0 rgba(48, 53, 56, 1), 710px 370px 0 0 rgba(48, 53, 56, 1),
  720px 370px 0 0 rgba(48, 53, 56, 1), 730px 370px 0 0 rgba(48, 53, 56, 1),
  740px 370px 0 0 rgba(48, 53, 56, 1), 750px 370px 0 0 rgba(48, 53, 56, 1),
  760px 370px 0 0 rgba(48, 53, 56, 1), 770px 370px 0 0 rgba(48, 53, 56, 1),
  780px 370px 0 0 rgba(48, 53, 56, 1), 790px 370px 0 0 rgba(48, 53, 56, 1),
  800px 370px 0 0 rgba(48, 53, 56, 1), 810px 370px 0 0 rgba(48, 53, 56, 1),
  820px 370px 0 0 rgba(48, 53, 56, 1), 830px 370px 0 0 rgba(48, 53, 56, 1),
  840px 370px 0 0 rgba(242, 245, 252, 1), 850px 370px 0 0 rgba(48, 53, 56, 1),
  860px 370px 0 0 rgba(48, 53, 56, 1), 870px 370px 0 0 rgba(48, 53, 56, 1),
  880px 370px 0 0 rgba(48, 53, 56, 1), 890px 370px 0 0 rgba(48, 53, 56, 1),
  900px 370px 0 0 rgba(48, 53, 56, 1), 910px 370px 0 0 rgba(48, 53, 56, 1),
  920px 370px 0 0 rgba(48, 53, 56, 1), 930px 370px 0 0 rgba(48, 53, 56, 1),
  940px 370px 0 0 rgba(48, 53, 56, 1), 950px 370px 0 0 rgba(48, 53, 56, 1),
  960px 370px 0 0 rgba(48, 53, 56, 1), 970px 370px 0 0 rgba(48, 53, 56, 1),
  980px 370px 0 0 rgba(48, 53, 56, 1), 990px 370px 0 0 rgba(48, 53, 56, 1),
  1000px 370px 0 0 rgba(48, 53, 56, 1), 10px 380px 0 0 rgba(28, 32, 34, 1),
  20px 380px 0 0 rgba(219, 222, 232, 1), 30px 380px 0 0 rgba(111, 114, 121, 1),
  40px 380px 0 0 rgba(28, 32, 34, 1), 50px 380px 0 0 rgba(48, 53, 56, 1),
  60px 380px 0 0 rgba(48, 53, 56, 1), 70px 380px 0 0 rgba(48, 53, 56, 1),
  80px 380px 0 0 rgba(48, 53, 56, 1), 90px 380px 0 0 rgba(48, 53, 56, 1),
  100px 380px 0 0 rgba(48, 53, 56, 1), 110px 380px 0 0 rgba(48, 53, 56, 1),
  120px 380px 0 0 rgba(48, 53, 56, 1), 130px 380px 0 0 rgba(48, 53, 56, 1),
  140px 380px 0 0 rgba(48, 53, 56, 1), 150px 380px 0 0 rgba(48, 53, 56, 1),
  160px 380px 0 0 rgba(242, 245, 252, 1), 170px 380px 0 0 rgba(242, 245, 252, 1),
  180px 380px 0 0 rgba(242, 245, 252, 1), 190px 380px 0 0 rgba(242, 245, 252, 1),
  200px 380px 0 0 rgba(48, 53, 56, 1), 210px 380px 0 0 rgba(48, 53, 56, 1),
  220px 380px 0 0 rgba(48, 53, 56, 1), 230px 380px 0 0 rgba(242, 245, 252, 1),
  240px 380px 0 0 rgba(242, 245, 252, 1), 250px 380px 0 0 rgba(242, 245, 252, 1),
  260px 380px 0 0 rgba(242, 245, 252, 1), 270px 380px 0 0 rgba(48, 53, 56, 1),
  280px 380px 0 0 rgba(48, 53, 56, 1), 290px 380px 0 0 rgba(242, 245, 252, 1),
  300px 380px 0 0 rgba(242, 245, 252, 1), 310px 380px 0 0 rgba(242, 245, 252, 1),
  320px 380px 0 0 rgba(242, 245, 252, 1), 330px 380px 0 0 rgba(48, 53, 56, 1),
  340px 380px 0 0 rgba(48, 53, 56, 1), 350px 380px 0 0 rgba(48, 53, 56, 1),
  360px 380px 0 0 rgba(242, 245, 252, 1), 370px 380px 0 0 rgba(242, 245, 252, 1),
  380px 380px 0 0 rgba(242, 245, 252, 1), 390px 380px 0 0 rgba(242, 245, 252, 1),
  400px 380px 0 0 rgba(48, 53, 56, 1), 410px 380px 0 0 rgba(48, 53, 56, 1),
  420px 380px 0 0 rgba(48, 53, 56, 1), 430px 380px 0 0 rgba(242, 245, 252, 1),
  440px 380px 0 0 rgba(242, 245, 252, 1), 450px 380px 0 0 rgba(242, 245, 252, 1),
  460px 380px 0 0 rgba(242, 245, 252, 1), 470px 380px 0 0 rgba(48, 53, 56, 1),
  480px 380px 0 0 rgba(48, 53, 56, 1), 490px 380px 0 0 rgba(48, 53, 56, 1),
  500px 380px 0 0 rgba(242, 245, 252, 1), 510px 380px 0 0 rgba(242, 245, 252, 1),
  520px 380px 0 0 rgba(242, 245, 252, 1), 530px 380px 0 0 rgba(242, 245, 252, 1),
  540px 380px 0 0 rgba(48, 53, 56, 1), 550px 380px 0 0 rgba(48, 53, 56, 1),
  560px 380px 0 0 rgba(48, 53, 56, 1), 570px 380px 0 0 rgba(242, 245, 252, 1),
  580px 380px 0 0 rgba(242, 245, 252, 1), 590px 380px 0 0 rgba(242, 245, 252, 1),
  600px 380px 0 0 rgba(242, 245, 252, 1), 610px 380px 0 0 rgba(48, 53, 56, 1),
  620px 380px 0 0 rgba(48, 53, 56, 1), 630px 380px 0 0 rgba(48, 53, 56, 1),
  640px 380px 0 0 rgba(242, 245, 252, 1), 650px 380px 0 0 rgba(242, 245, 252, 1),
  660px 380px 0 0 rgba(242, 245, 252, 1), 670px 380px 0 0 rgba(242, 245, 252, 1),
  680px 380px 0 0 rgba(48, 53, 56, 1), 690px 380px 0 0 rgba(48, 53, 56, 1),
  700px 380px 0 0 rgba(48, 53, 56, 1), 710px 380px 0 0 rgba(242, 245, 252, 1),
  720px 380px 0 0 rgba(242, 245, 252, 1), 730px 380px 0 0 rgba(242, 245, 252, 1),
  740px 380px 0 0 rgba(242, 245, 252, 1), 750px 380px 0 0 rgba(48, 53, 56, 1),
  760px 380px 0 0 rgba(48, 53, 56, 1), 770px 380px 0 0 rgba(48, 53, 56, 1),
  780px 380px 0 0 rgba(48, 53, 56, 1), 790px 380px 0 0 rgba(48, 53, 56, 1),
  800px 380px 0 0 rgba(48, 53, 56, 1), 810px 380px 0 0 rgba(48, 53, 56, 1),
  820px 380px 0 0 rgba(48, 53, 56, 1), 830px 380px 0 0 rgba(48, 53, 56, 1),
  840px 380px 0 0 rgba(48, 53, 56, 1), 850px 380px 0 0 rgba(48, 53, 56, 1),
  860px 380px 0 0 rgba(48, 53, 56, 1), 870px 380px 0 0 rgba(48, 53, 56, 1),
  880px 380px 0 0 rgba(48, 53, 56, 1), 890px 380px 0 0 rgba(48, 53, 56, 1),
  900px 380px 0 0 rgba(48, 53, 56, 1), 910px 380px 0 0 rgba(48, 53, 56, 1),
  920px 380px 0 0 rgba(48, 53, 56, 1), 930px 380px 0 0 rgba(48, 53, 56, 1),
  940px 380px 0 0 rgba(48, 53, 56, 1), 950px 380px 0 0 rgba(48, 53, 56, 1),
  960px 380px 0 0 rgba(48, 53, 56, 1), 970px 380px 0 0 rgba(48, 53, 56, 1),
  980px 380px 0 0 rgba(48, 53, 56, 1), 990px 380px 0 0 rgba(48, 53, 56, 1),
  1000px 380px 0 0 rgba(48, 53, 56, 1), 10px 390px 0 0 rgba(28, 32, 34, 1),
  20px 390px 0 0 rgba(219, 222, 232, 1), 30px 390px 0 0 rgba(111, 114, 121, 1),
  40px 390px 0 0 rgba(28, 32, 34, 1), 50px 390px 0 0 rgba(48, 53, 56, 1),
  60px 390px 0 0 rgba(48, 53, 56, 1), 70px 390px 0 0 rgba(48, 53, 56, 1),
  80px 390px 0 0 rgba(48, 53, 56, 1), 90px 390px 0 0 rgba(48, 53, 56, 1),
  100px 390px 0 0 rgba(48, 53, 56, 1), 110px 390px 0 0 rgba(48, 53, 56, 1),
  120px 390px 0 0 rgba(48, 53, 56, 1), 130px 390px 0 0 rgba(48, 53, 56, 1),
  140px 390px 0 0 rgba(48, 53, 56, 1), 150px 390px 0 0 rgba(48, 53, 56, 1),
  160px 390px 0 0 rgba(48, 53, 56, 1), 170px 390px 0 0 rgba(48, 53, 56, 1),
  180px 390px 0 0 rgba(48, 53, 56, 1), 190px 390px 0 0 rgba(48, 53, 56, 1),
  200px 390px 0 0 rgba(48, 53, 56, 1), 210px 390px 0 0 rgba(48, 53, 56, 1),
  220px 390px 0 0 rgba(48, 53, 56, 1), 230px 390px 0 0 rgba(48, 53, 56, 1),
  240px 390px 0 0 rgba(48, 53, 56, 1), 250px 390px 0 0 rgba(48, 53, 56, 1),
  260px 390px 0 0 rgba(48, 53, 56, 1), 270px 390px 0 0 rgba(48, 53, 56, 1),
  280px 390px 0 0 rgba(48, 53, 56, 1), 290px 390px 0 0 rgba(48, 53, 56, 1),
  300px 390px 0 0 rgba(48, 53, 56, 1), 310px 390px 0 0 rgba(48, 53, 56, 1),
  320px 390px 0 0 rgba(48, 53, 56, 1), 330px 390px 0 0 rgba(48, 53, 56, 1),
  340px 390px 0 0 rgba(48, 53, 56, 1), 350px 390px 0 0 rgba(48, 53, 56, 1),
  360px 390px 0 0 rgba(48, 53, 56, 1), 370px 390px 0 0 rgba(48, 53, 56, 1),
  380px 390px 0 0 rgba(48, 53, 56, 1), 390px 390px 0 0 rgba(48, 53, 56, 1),
  400px 390px 0 0 rgba(48, 53, 56, 1), 410px 390px 0 0 rgba(48, 53, 56, 1),
  420px 390px 0 0 rgba(48, 53, 56, 1), 430px 390px 0 0 rgba(48, 53, 56, 1),
  440px 390px 0 0 rgba(48, 53, 56, 1), 450px 390px 0 0 rgba(48, 53, 56, 1),
  460px 390px 0 0 rgba(48, 53, 56, 1), 470px 390px 0 0 rgba(48, 53, 56, 1),
  480px 390px 0 0 rgba(48, 53, 56, 1), 490px 390px 0 0 rgba(48, 53, 56, 1),
  500px 390px 0 0 rgba(48, 53, 56, 1), 510px 390px 0 0 rgba(48, 53, 56, 1),
  520px 390px 0 0 rgba(48, 53, 56, 1), 530px 390px 0 0 rgba(48, 53, 56, 1),
  540px 390px 0 0 rgba(48, 53, 56, 1), 550px 390px 0 0 rgba(48, 53, 56, 1),
  560px 390px 0 0 rgba(48, 53, 56, 1), 570px 390px 0 0 rgba(48, 53, 56, 1),
  580px 390px 0 0 rgba(48, 53, 56, 1), 590px 390px 0 0 rgba(48, 53, 56, 1),
  600px 390px 0 0 rgba(48, 53, 56, 1), 610px 390px 0 0 rgba(48, 53, 56, 1),
  620px 390px 0 0 rgba(48, 53, 56, 1), 630px 390px 0 0 rgba(48, 53, 56, 1),
  640px 390px 0 0 rgba(48, 53, 56, 1), 650px 390px 0 0 rgba(48, 53, 56, 1),
  660px 390px 0 0 rgba(48, 53, 56, 1), 670px 390px 0 0 rgba(48, 53, 56, 1),
  680px 390px 0 0 rgba(48, 53, 56, 1), 690px 390px 0 0 rgba(48, 53, 56, 1),
  700px 390px 0 0 rgba(48, 53, 56, 1), 710px 390px 0 0 rgba(48, 53, 56, 1),
  720px 390px 0 0 rgba(48, 53, 56, 1), 730px 390px 0 0 rgba(48, 53, 56, 1),
  740px 390px 0 0 rgba(48, 53, 56, 1), 750px 390px 0 0 rgba(48, 53, 56, 1),
  760px 390px 0 0 rgba(48, 53, 56, 1), 770px 390px 0 0 rgba(48, 53, 56, 1),
  780px 390px 0 0 rgba(48, 53, 56, 1), 790px 390px 0 0 rgba(48, 53, 56, 1),
  800px 390px 0 0 rgba(48, 53, 56, 1), 810px 390px 0 0 rgba(48, 53, 56, 1),
  820px 390px 0 0 rgba(48, 53, 56, 1), 830px 390px 0 0 rgba(48, 53, 56, 1),
  840px 390px 0 0 rgba(48, 53, 56, 1), 850px 390px 0 0 rgba(48, 53, 56, 1),
  860px 390px 0 0 rgba(48, 53, 56, 1), 870px 390px 0 0 rgba(48, 53, 56, 1),
  880px 390px 0 0 rgba(48, 53, 56, 1), 890px 390px 0 0 rgba(48, 53, 56, 1),
  900px 390px 0 0 rgba(48, 53, 56, 1), 910px 390px 0 0 rgba(48, 53, 56, 1),
  920px 390px 0 0 rgba(48, 53, 56, 1), 930px 390px 0 0 rgba(48, 53, 56, 1),
  940px 390px 0 0 rgba(48, 53, 56, 1), 950px 390px 0 0 rgba(48, 53, 56, 1),
  960px 390px 0 0 rgba(48, 53, 56, 1), 970px 390px 0 0 rgba(48, 53, 56, 1),
  980px 390px 0 0 rgba(48, 53, 56, 1), 990px 390px 0 0 rgba(48, 53, 56, 1),
  1000px 390px 0 0 rgba(48, 53, 56, 1), 10px 400px 0 0 rgba(28, 32, 34, 1),
  20px 400px 0 0 rgba(219, 222, 232, 1), 30px 400px 0 0 rgba(111, 114, 121, 1),
  40px 400px 0 0 rgba(28, 32, 34, 1), 50px 400px 0 0 rgba(48, 53, 56, 1),
  60px 400px 0 0 rgba(48, 53, 56, 1), 70px 400px 0 0 rgba(48, 53, 56, 1),
  80px 400px 0 0 rgba(48, 53, 56, 1), 90px 400px 0 0 rgba(48, 53, 56, 1),
  100px 400px 0 0 rgba(48, 53, 56, 1), 110px 400px 0 0 rgba(48, 53, 56, 1),
  120px 400px 0 0 rgba(48, 53, 56, 1), 130px 400px 0 0 rgba(48, 53, 56, 1),
  140px 400px 0 0 rgba(48, 53, 56, 1), 150px 400px 0 0 rgba(48, 53, 56, 1),
  160px 400px 0 0 rgba(48, 53, 56, 1), 170px 400px 0 0 rgba(48, 53, 56, 1),
  180px 400px 0 0 rgba(48, 53, 56, 1), 190px 400px 0 0 rgba(48, 53, 56, 1),
  200px 400px 0 0 rgba(48, 53, 56, 1), 210px 400px 0 0 rgba(48, 53, 56, 1),
  220px 400px 0 0 rgba(48, 53, 56, 1), 230px 400px 0 0 rgba(48, 53, 56, 1),
  240px 400px 0 0 rgba(48, 53, 56, 1), 250px 400px 0 0 rgba(48, 53, 56, 1),
  260px 400px 0 0 rgba(48, 53, 56, 1), 270px 400px 0 0 rgba(48, 53, 56, 1),
  280px 400px 0 0 rgba(48, 53, 56, 1), 290px 400px 0 0 rgba(48, 53, 56, 1),
  300px 400px 0 0 rgba(48, 53, 56, 1), 310px 400px 0 0 rgba(48, 53, 56, 1),
  320px 400px 0 0 rgba(48, 53, 56, 1), 330px 400px 0 0 rgba(48, 53, 56, 1),
  340px 400px 0 0 rgba(48, 53, 56, 1), 350px 400px 0 0 rgba(48, 53, 56, 1),
  360px 400px 0 0 rgba(48, 53, 56, 1), 370px 400px 0 0 rgba(48, 53, 56, 1),
  380px 400px 0 0 rgba(48, 53, 56, 1), 390px 400px 0 0 rgba(48, 53, 56, 1),
  400px 400px 0 0 rgba(48, 53, 56, 1), 410px 400px 0 0 rgba(48, 53, 56, 1),
  420px 400px 0 0 rgba(48, 53, 56, 1), 430px 400px 0 0 rgba(48, 53, 56, 1),
  440px 400px 0 0 rgba(48, 53, 56, 1), 450px 400px 0 0 rgba(48, 53, 56, 1),
  460px 400px 0 0 rgba(48, 53, 56, 1), 470px 400px 0 0 rgba(48, 53, 56, 1),
  480px 400px 0 0 rgba(48, 53, 56, 1), 490px 400px 0 0 rgba(48, 53, 56, 1),
  500px 400px 0 0 rgba(48, 53, 56, 1), 510px 400px 0 0 rgba(48, 53, 56, 1),
  520px 400px 0 0 rgba(48, 53, 56, 1), 530px 400px 0 0 rgba(48, 53, 56, 1),
  540px 400px 0 0 rgba(48, 53, 56, 1), 550px 400px 0 0 rgba(48, 53, 56, 1),
  560px 400px 0 0 rgba(48, 53, 56, 1), 570px 400px 0 0 rgba(48, 53, 56, 1),
  580px 400px 0 0 rgba(48, 53, 56, 1), 590px 400px 0 0 rgba(48, 53, 56, 1),
  600px 400px 0 0 rgba(48, 53, 56, 1), 610px 400px 0 0 rgba(48, 53, 56, 1),
  620px 400px 0 0 rgba(48, 53, 56, 1), 630px 400px 0 0 rgba(48, 53, 56, 1),
  640px 400px 0 0 rgba(48, 53, 56, 1), 650px 400px 0 0 rgba(48, 53, 56, 1),
  660px 400px 0 0 rgba(48, 53, 56, 1), 670px 400px 0 0 rgba(48, 53, 56, 1),
  680px 400px 0 0 rgba(48, 53, 56, 1), 690px 400px 0 0 rgba(48, 53, 56, 1),
  700px 400px 0 0 rgba(48, 53, 56, 1), 710px 400px 0 0 rgba(48, 53, 56, 1),
  720px 400px 0 0 rgba(48, 53, 56, 1), 730px 400px 0 0 rgba(48, 53, 56, 1),
  740px 400px 0 0 rgba(48, 53, 56, 1), 750px 400px 0 0 rgba(48, 53, 56, 1),
  760px 400px 0 0 rgba(48, 53, 56, 1), 770px 400px 0 0 rgba(48, 53, 56, 1),
  780px 400px 0 0 rgba(48, 53, 56, 1), 790px 400px 0 0 rgba(48, 53, 56, 1),
  800px 400px 0 0 rgba(48, 53, 56, 1), 810px 400px 0 0 rgba(48, 53, 56, 1),
  820px 400px 0 0 rgba(48, 53, 56, 1), 830px 400px 0 0 rgba(48, 53, 56, 1),
  840px 400px 0 0 rgba(48, 53, 56, 1), 850px 400px 0 0 rgba(48, 53, 56, 1),
  860px 400px 0 0 rgba(48, 53, 56, 1), 870px 400px 0 0 rgba(48, 53, 56, 1),
  880px 400px 0 0 rgba(48, 53, 56, 1), 890px 400px 0 0 rgba(48, 53, 56, 1),
  900px 400px 0 0 rgba(48, 53, 56, 1), 910px 400px 0 0 rgba(48, 53, 56, 1),
  920px 400px 0 0 rgba(48, 53, 56, 1), 930px 400px 0 0 rgba(48, 53, 56, 1),
  940px 400px 0 0 rgba(48, 53, 56, 1), 950px 400px 0 0 rgba(48, 53, 56, 1),
  960px 400px 0 0 rgba(48, 53, 56, 1), 970px 400px 0 0 rgba(48, 53, 56, 1),
  980px 400px 0 0 rgba(48, 53, 56, 1), 990px 400px 0 0 rgba(48, 53, 56, 1),
  1000px 400px 0 0 rgba(48, 53, 56, 1), 10px 410px 0 0 rgba(28, 32, 34, 1),
  20px 410px 0 0 rgba(219, 222, 232, 1), 30px 410px 0 0 rgba(111, 114, 121, 1),
  40px 410px 0 0 rgba(28, 32, 34, 1), 50px 410px 0 0 rgba(48, 53, 56, 1),
  60px 410px 0 0 rgba(48, 53, 56, 1), 70px 410px 0 0 rgba(48, 53, 56, 1),
  80px 410px 0 0 rgba(48, 53, 56, 1), 90px 410px 0 0 rgba(48, 53, 56, 1),
  100px 410px 0 0 rgba(48, 53, 56, 1), 110px 410px 0 0 rgba(48, 53, 56, 1),
  120px 410px 0 0 rgba(48, 53, 56, 1), 130px 410px 0 0 rgba(48, 53, 56, 1),
  140px 410px 0 0 rgba(48, 53, 56, 1), 150px 410px 0 0 rgba(48, 53, 56, 1),
  160px 410px 0 0 rgba(48, 53, 56, 1), 170px 410px 0 0 rgba(48, 53, 56, 1),
  180px 410px 0 0 rgba(48, 53, 56, 1), 190px 410px 0 0 rgba(48, 53, 56, 1),
  200px 410px 0 0 rgba(48, 53, 56, 1), 210px 410px 0 0 rgba(48, 53, 56, 1),
  220px 410px 0 0 rgba(48, 53, 56, 1), 230px 410px 0 0 rgba(48, 53, 56, 1),
  240px 410px 0 0 rgba(48, 53, 56, 1), 250px 410px 0 0 rgba(48, 53, 56, 1),
  260px 410px 0 0 rgba(48, 53, 56, 1), 270px 410px 0 0 rgba(48, 53, 56, 1),
  280px 410px 0 0 rgba(48, 53, 56, 1), 290px 410px 0 0 rgba(48, 53, 56, 1),
  300px 410px 0 0 rgba(48, 53, 56, 1), 310px 410px 0 0 rgba(48, 53, 56, 1),
  320px 410px 0 0 rgba(48, 53, 56, 1), 330px 410px 0 0 rgba(48, 53, 56, 1),
  340px 410px 0 0 rgba(48, 53, 56, 1), 350px 410px 0 0 rgba(48, 53, 56, 1),
  360px 410px 0 0 rgba(48, 53, 56, 1), 370px 410px 0 0 rgba(48, 53, 56, 1),
  380px 410px 0 0 rgba(48, 53, 56, 1), 390px 410px 0 0 rgba(48, 53, 56, 1),
  400px 410px 0 0 rgba(48, 53, 56, 1), 410px 410px 0 0 rgba(48, 53, 56, 1),
  420px 410px 0 0 rgba(48, 53, 56, 1), 430px 410px 0 0 rgba(48, 53, 56, 1),
  440px 410px 0 0 rgba(48, 53, 56, 1), 450px 410px 0 0 rgba(48, 53, 56, 1),
  460px 410px 0 0 rgba(48, 53, 56, 1), 470px 410px 0 0 rgba(48, 53, 56, 1),
  480px 410px 0 0 rgba(48, 53, 56, 1), 490px 410px 0 0 rgba(48, 53, 56, 1),
  500px 410px 0 0 rgba(48, 53, 56, 1), 510px 410px 0 0 rgba(48, 53, 56, 1),
  520px 410px 0 0 rgba(48, 53, 56, 1), 530px 410px 0 0 rgba(48, 53, 56, 1),
  540px 410px 0 0 rgba(48, 53, 56, 1), 550px 410px 0 0 rgba(48, 53, 56, 1),
  560px 410px 0 0 rgba(48, 53, 56, 1), 570px 410px 0 0 rgba(48, 53, 56, 1),
  580px 410px 0 0 rgba(48, 53, 56, 1), 590px 410px 0 0 rgba(48, 53, 56, 1),
  600px 410px 0 0 rgba(48, 53, 56, 1), 610px 410px 0 0 rgba(48, 53, 56, 1),
  620px 410px 0 0 rgba(48, 53, 56, 1), 630px 410px 0 0 rgba(48, 53, 56, 1),
  640px 410px 0 0 rgba(48, 53, 56, 1), 650px 410px 0 0 rgba(48, 53, 56, 1),
  660px 410px 0 0 rgba(48, 53, 56, 1), 670px 410px 0 0 rgba(48, 53, 56, 1),
  680px 410px 0 0 rgba(48, 53, 56, 1), 690px 410px 0 0 rgba(48, 53, 56, 1),
  700px 410px 0 0 rgba(48, 53, 56, 1), 710px 410px 0 0 rgba(48, 53, 56, 1),
  720px 410px 0 0 rgba(48, 53, 56, 1), 730px 410px 0 0 rgba(48, 53, 56, 1),
  740px 410px 0 0 rgba(48, 53, 56, 1), 750px 410px 0 0 rgba(48, 53, 56, 1),
  760px 410px 0 0 rgba(48, 53, 56, 1), 770px 410px 0 0 rgba(48, 53, 56, 1),
  780px 410px 0 0 rgba(48, 53, 56, 1), 790px 410px 0 0 rgba(48, 53, 56, 1),
  800px 410px 0 0 rgba(48, 53, 56, 1), 810px 410px 0 0 rgba(48, 53, 56, 1),
  820px 410px 0 0 rgba(48, 53, 56, 1), 830px 410px 0 0 rgba(48, 53, 56, 1),
  840px 410px 0 0 rgba(48, 53, 56, 1), 850px 410px 0 0 rgba(48, 53, 56, 1),
  860px 410px 0 0 rgba(48, 53, 56, 1), 870px 410px 0 0 rgba(48, 53, 56, 1),
  880px 410px 0 0 rgba(48, 53, 56, 1), 890px 410px 0 0 rgba(48, 53, 56, 1),
  900px 410px 0 0 rgba(48, 53, 56, 1), 910px 410px 0 0 rgba(48, 53, 56, 1),
  920px 410px 0 0 rgba(48, 53, 56, 1), 930px 410px 0 0 rgba(48, 53, 56, 1),
  940px 410px 0 0 rgba(48, 53, 56, 1), 950px 410px 0 0 rgba(48, 53, 56, 1),
  960px 410px 0 0 rgba(48, 53, 56, 1), 970px 410px 0 0 rgba(48, 53, 56, 1),
  980px 410px 0 0 rgba(48, 53, 56, 1), 990px 410px 0 0 rgba(48, 53, 56, 1),
  1000px 410px 0 0 rgba(48, 53, 56, 1), 10px 420px 0 0 rgba(28, 32, 34, 1),
  20px 420px 0 0 rgba(219, 222, 232, 1), 30px 420px 0 0 rgba(111, 114, 121, 1),
  40px 420px 0 0 rgba(28, 32, 34, 1), 50px 420px 0 0 rgba(48, 53, 56, 1),
  60px 420px 0 0 rgba(48, 53, 56, 1), 70px 420px 0 0 rgba(48, 53, 56, 1),
  80px 420px 0 0 rgba(48, 53, 56, 1), 90px 420px 0 0 rgba(48, 53, 56, 1),
  100px 420px 0 0 rgba(48, 53, 56, 1), 110px 420px 0 0 rgba(48, 53, 56, 1),
  120px 420px 0 0 rgba(48, 53, 56, 1), 130px 420px 0 0 rgba(48, 53, 56, 1),
  140px 420px 0 0 rgba(48, 53, 56, 1), 150px 420px 0 0 rgba(48, 53, 56, 1),
  160px 420px 0 0 rgba(48, 53, 56, 1), 170px 420px 0 0 rgba(48, 53, 56, 1),
  180px 420px 0 0 rgba(48, 53, 56, 1), 190px 420px 0 0 rgba(48, 53, 56, 1),
  200px 420px 0 0 rgba(48, 53, 56, 1), 210px 420px 0 0 rgba(48, 53, 56, 1),
  220px 420px 0 0 rgba(48, 53, 56, 1), 230px 420px 0 0 rgba(48, 53, 56, 1),
  240px 420px 0 0 rgba(48, 53, 56, 1), 250px 420px 0 0 rgba(48, 53, 56, 1),
  260px 420px 0 0 rgba(48, 53, 56, 1), 270px 420px 0 0 rgba(48, 53, 56, 1),
  280px 420px 0 0 rgba(48, 53, 56, 1), 290px 420px 0 0 rgba(48, 53, 56, 1),
  300px 420px 0 0 rgba(48, 53, 56, 1), 310px 420px 0 0 rgba(48, 53, 56, 1),
  320px 420px 0 0 rgba(48, 53, 56, 1), 330px 420px 0 0 rgba(48, 53, 56, 1),
  340px 420px 0 0 rgba(48, 53, 56, 1), 350px 420px 0 0 rgba(48, 53, 56, 1),
  360px 420px 0 0 rgba(48, 53, 56, 1), 370px 420px 0 0 rgba(48, 53, 56, 1),
  380px 420px 0 0 rgba(48, 53, 56, 1), 390px 420px 0 0 rgba(48, 53, 56, 1),
  400px 420px 0 0 rgba(48, 53, 56, 1), 410px 420px 0 0 rgba(48, 53, 56, 1),
  420px 420px 0 0 rgba(48, 53, 56, 1), 430px 420px 0 0 rgba(48, 53, 56, 1),
  440px 420px 0 0 rgba(48, 53, 56, 1), 450px 420px 0 0 rgba(48, 53, 56, 1),
  460px 420px 0 0 rgba(48, 53, 56, 1), 470px 420px 0 0 rgba(48, 53, 56, 1),
  480px 420px 0 0 rgba(48, 53, 56, 1), 490px 420px 0 0 rgba(48, 53, 56, 1),
  500px 420px 0 0 rgba(48, 53, 56, 1), 510px 420px 0 0 rgba(48, 53, 56, 1),
  520px 420px 0 0 rgba(48, 53, 56, 1), 530px 420px 0 0 rgba(48, 53, 56, 1),
  540px 420px 0 0 rgba(48, 53, 56, 1), 550px 420px 0 0 rgba(48, 53, 56, 1),
  560px 420px 0 0 rgba(48, 53, 56, 1), 570px 420px 0 0 rgba(48, 53, 56, 1),
  580px 420px 0 0 rgba(48, 53, 56, 1), 590px 420px 0 0 rgba(48, 53, 56, 1),
  600px 420px 0 0 rgba(48, 53, 56, 1), 610px 420px 0 0 rgba(48, 53, 56, 1),
  620px 420px 0 0 rgba(48, 53, 56, 1), 630px 420px 0 0 rgba(48, 53, 56, 1),
  640px 420px 0 0 rgba(48, 53, 56, 1), 650px 420px 0 0 rgba(48, 53, 56, 1),
  660px 420px 0 0 rgba(48, 53, 56, 1), 670px 420px 0 0 rgba(48, 53, 56, 1),
  680px 420px 0 0 rgba(48, 53, 56, 1), 690px 420px 0 0 rgba(48, 53, 56, 1),
  700px 420px 0 0 rgba(48, 53, 56, 1), 710px 420px 0 0 rgba(48, 53, 56, 1),
  720px 420px 0 0 rgba(48, 53, 56, 1), 730px 420px 0 0 rgba(48, 53, 56, 1),
  740px 420px 0 0 rgba(48, 53, 56, 1), 750px 420px 0 0 rgba(48, 53, 56, 1),
  760px 420px 0 0 rgba(48, 53, 56, 1), 770px 420px 0 0 rgba(48, 53, 56, 1),
  780px 420px 0 0 rgba(48, 53, 56, 1), 790px 420px 0 0 rgba(48, 53, 56, 1),
  800px 420px 0 0 rgba(48, 53, 56, 1), 810px 420px 0 0 rgba(48, 53, 56, 1),
  820px 420px 0 0 rgba(48, 53, 56, 1), 830px 420px 0 0 rgba(48, 53, 56, 1),
  840px 420px 0 0 rgba(48, 53, 56, 1), 850px 420px 0 0 rgba(48, 53, 56, 1),
  860px 420px 0 0 rgba(48, 53, 56, 1), 870px 420px 0 0 rgba(48, 53, 56, 1),
  880px 420px 0 0 rgba(48, 53, 56, 1), 890px 420px 0 0 rgba(48, 53, 56, 1),
  900px 420px 0 0 rgba(48, 53, 56, 1), 910px 420px 0 0 rgba(48, 53, 56, 1),
  920px 420px 0 0 rgba(48, 53, 56, 1), 930px 420px 0 0 rgba(48, 53, 56, 1),
  940px 420px 0 0 rgba(48, 53, 56, 1), 950px 420px 0 0 rgba(48, 53, 56, 1),
  960px 420px 0 0 rgba(48, 53, 56, 1), 970px 420px 0 0 rgba(48, 53, 56, 1),
  980px 420px 0 0 rgba(48, 53, 56, 1), 990px 420px 0 0 rgba(48, 53, 56, 1),
  1000px 420px 0 0 rgba(48, 53, 56, 1), 10px 430px 0 0 rgba(28, 32, 34, 1),
  20px 430px 0 0 rgba(219, 222, 232, 1), 30px 430px 0 0 rgba(111, 114, 121, 1),
  40px 430px 0 0 rgba(28, 32, 34, 1), 50px 430px 0 0 rgba(48, 53, 56, 1),
  60px 430px 0 0 rgba(48, 53, 56, 1), 70px 430px 0 0 rgba(48, 53, 56, 1),
  80px 430px 0 0 rgba(48, 53, 56, 1), 90px 430px 0 0 rgba(48, 53, 56, 1),
  100px 430px 0 0 rgba(48, 53, 56, 1), 110px 430px 0 0 rgba(48, 53, 56, 1),
  120px 430px 0 0 rgba(48, 53, 56, 1), 130px 430px 0 0 rgba(48, 53, 56, 1),
  140px 430px 0 0 rgba(48, 53, 56, 1), 150px 430px 0 0 rgba(48, 53, 56, 1),
  160px 430px 0 0 rgba(48, 53, 56, 1), 170px 430px 0 0 rgba(48, 53, 56, 1),
  180px 430px 0 0 rgba(48, 53, 56, 1), 190px 430px 0 0 rgba(48, 53, 56, 1),
  200px 430px 0 0 rgba(48, 53, 56, 1), 210px 430px 0 0 rgba(48, 53, 56, 1),
  220px 430px 0 0 rgba(48, 53, 56, 1), 230px 430px 0 0 rgba(48, 53, 56, 1),
  240px 430px 0 0 rgba(48, 53, 56, 1), 250px 430px 0 0 rgba(48, 53, 56, 1),
  260px 430px 0 0 rgba(48, 53, 56, 1), 270px 430px 0 0 rgba(48, 53, 56, 1),
  280px 430px 0 0 rgba(48, 53, 56, 1), 290px 430px 0 0 rgba(48, 53, 56, 1),
  300px 430px 0 0 rgba(48, 53, 56, 1), 310px 430px 0 0 rgba(48, 53, 56, 1),
  320px 430px 0 0 rgba(48, 53, 56, 1), 330px 430px 0 0 rgba(48, 53, 56, 1),
  340px 430px 0 0 rgba(48, 53, 56, 1), 350px 430px 0 0 rgba(48, 53, 56, 1),
  360px 430px 0 0 rgba(48, 53, 56, 1), 370px 430px 0 0 rgba(48, 53, 56, 1),
  380px 430px 0 0 rgba(48, 53, 56, 1), 390px 430px 0 0 rgba(48, 53, 56, 1),
  400px 430px 0 0 rgba(48, 53, 56, 1), 410px 430px 0 0 rgba(48, 53, 56, 1),
  420px 430px 0 0 rgba(48, 53, 56, 1), 430px 430px 0 0 rgba(48, 53, 56, 1),
  440px 430px 0 0 rgba(48, 53, 56, 1), 450px 430px 0 0 rgba(48, 53, 56, 1),
  460px 430px 0 0 rgba(48, 53, 56, 1), 470px 430px 0 0 rgba(48, 53, 56, 1),
  480px 430px 0 0 rgba(48, 53, 56, 1), 490px 430px 0 0 rgba(48, 53, 56, 1),
  500px 430px 0 0 rgba(48, 53, 56, 1), 510px 430px 0 0 rgba(48, 53, 56, 1),
  520px 430px 0 0 rgba(48, 53, 56, 1), 530px 430px 0 0 rgba(48, 53, 56, 1),
  540px 430px 0 0 rgba(48, 53, 56, 1), 550px 430px 0 0 rgba(48, 53, 56, 1),
  560px 430px 0 0 rgba(48, 53, 56, 1), 570px 430px 0 0 rgba(48, 53, 56, 1),
  580px 430px 0 0 rgba(48, 53, 56, 1), 590px 430px 0 0 rgba(48, 53, 56, 1),
  600px 430px 0 0 rgba(48, 53, 56, 1), 610px 430px 0 0 rgba(48, 53, 56, 1),
  620px 430px 0 0 rgba(48, 53, 56, 1), 630px 430px 0 0 rgba(48, 53, 56, 1),
  640px 430px 0 0 rgba(48, 53, 56, 1), 650px 430px 0 0 rgba(48, 53, 56, 1),
  660px 430px 0 0 rgba(48, 53, 56, 1), 670px 430px 0 0 rgba(48, 53, 56, 1),
  680px 430px 0 0 rgba(48, 53, 56, 1), 690px 430px 0 0 rgba(48, 53, 56, 1),
  700px 430px 0 0 rgba(48, 53, 56, 1), 710px 430px 0 0 rgba(48, 53, 56, 1),
  720px 430px 0 0 rgba(48, 53, 56, 1), 730px 430px 0 0 rgba(48, 53, 56, 1),
  740px 430px 0 0 rgba(48, 53, 56, 1), 750px 430px 0 0 rgba(48, 53, 56, 1),
  760px 430px 0 0 rgba(48, 53, 56, 1), 770px 430px 0 0 rgba(48, 53, 56, 1),
  780px 430px 0 0 rgba(48, 53, 56, 1), 790px 430px 0 0 rgba(48, 53, 56, 1),
  800px 430px 0 0 rgba(48, 53, 56, 1), 810px 430px 0 0 rgba(48, 53, 56, 1),
  820px 430px 0 0 rgba(48, 53, 56, 1), 830px 430px 0 0 rgba(48, 53, 56, 1),
  840px 430px 0 0 rgba(48, 53, 56, 1), 850px 430px 0 0 rgba(48, 53, 56, 1),
  860px 430px 0 0 rgba(48, 53, 56, 1), 870px 430px 0 0 rgba(48, 53, 56, 1),
  880px 430px 0 0 rgba(48, 53, 56, 1), 890px 430px 0 0 rgba(48, 53, 56, 1),
  900px 430px 0 0 rgba(48, 53, 56, 1), 910px 430px 0 0 rgba(48, 53, 56, 1),
  920px 430px 0 0 rgba(48, 53, 56, 1), 930px 430px 0 0 rgba(48, 53, 56, 1),
  940px 430px 0 0 rgba(48, 53, 56, 1), 950px 430px 0 0 rgba(48, 53, 56, 1),
  960px 430px 0 0 rgba(48, 53, 56, 1), 970px 430px 0 0 rgba(48, 53, 56, 1),
  980px 430px 0 0 rgba(48, 53, 56, 1), 990px 430px 0 0 rgba(48, 53, 56, 1),
  1000px 430px 0 0 rgba(48, 53, 56, 1), 10px 440px 0 0 rgba(28, 32, 34, 1),
  20px 440px 0 0 rgba(219, 222, 232, 1), 30px 440px 0 0 rgba(111, 114, 121, 1),
  40px 440px 0 0 rgba(28, 32, 34, 1), 50px 440px 0 0 rgba(48, 53, 56, 1),
  60px 440px 0 0 rgba(48, 53, 56, 1), 70px 440px 0 0 rgba(48, 53, 56, 1),
  80px 440px 0 0 rgba(48, 53, 56, 1), 90px 440px 0 0 rgba(48, 53, 56, 1),
  100px 440px 0 0 rgba(48, 53, 56, 1), 110px 440px 0 0 rgba(48, 53, 56, 1),
  120px 440px 0 0 rgba(48, 53, 56, 1), 130px 440px 0 0 rgba(48, 53, 56, 1),
  140px 440px 0 0 rgba(48, 53, 56, 1), 150px 440px 0 0 rgba(48, 53, 56, 1),
  160px 440px 0 0 rgba(48, 53, 56, 1), 170px 440px 0 0 rgba(48, 53, 56, 1),
  180px 440px 0 0 rgba(48, 53, 56, 1), 190px 440px 0 0 rgba(48, 53, 56, 1),
  200px 440px 0 0 rgba(48, 53, 56, 1), 210px 440px 0 0 rgba(48, 53, 56, 1),
  220px 440px 0 0 rgba(48, 53, 56, 1), 230px 440px 0 0 rgba(48, 53, 56, 1),
  240px 440px 0 0 rgba(48, 53, 56, 1), 250px 440px 0 0 rgba(48, 53, 56, 1),
  260px 440px 0 0 rgba(48, 53, 56, 1), 270px 440px 0 0 rgba(48, 53, 56, 1),
  280px 440px 0 0 rgba(48, 53, 56, 1), 290px 440px 0 0 rgba(48, 53, 56, 1),
  300px 440px 0 0 rgba(48, 53, 56, 1), 310px 440px 0 0 rgba(48, 53, 56, 1),
  320px 440px 0 0 rgba(48, 53, 56, 1), 330px 440px 0 0 rgba(48, 53, 56, 1),
  340px 440px 0 0 rgba(48, 53, 56, 1), 350px 440px 0 0 rgba(48, 53, 56, 1),
  360px 440px 0 0 rgba(48, 53, 56, 1), 370px 440px 0 0 rgba(48, 53, 56, 1),
  380px 440px 0 0 rgba(48, 53, 56, 1), 390px 440px 0 0 rgba(48, 53, 56, 1),
  400px 440px 0 0 rgba(48, 53, 56, 1), 410px 440px 0 0 rgba(48, 53, 56, 1),
  420px 440px 0 0 rgba(48, 53, 56, 1), 430px 440px 0 0 rgba(48, 53, 56, 1),
  440px 440px 0 0 rgba(48, 53, 56, 1), 450px 440px 0 0 rgba(48, 53, 56, 1),
  460px 440px 0 0 rgba(48, 53, 56, 1), 470px 440px 0 0 rgba(48, 53, 56, 1),
  480px 440px 0 0 rgba(48, 53, 56, 1), 490px 440px 0 0 rgba(48, 53, 56, 1),
  500px 440px 0 0 rgba(48, 53, 56, 1), 510px 440px 0 0 rgba(48, 53, 56, 1),
  520px 440px 0 0 rgba(48, 53, 56, 1), 530px 440px 0 0 rgba(48, 53, 56, 1),
  540px 440px 0 0 rgba(48, 53, 56, 1), 550px 440px 0 0 rgba(48, 53, 56, 1),
  560px 440px 0 0 rgba(48, 53, 56, 1), 570px 440px 0 0 rgba(48, 53, 56, 1),
  580px 440px 0 0 rgba(48, 53, 56, 1), 590px 440px 0 0 rgba(48, 53, 56, 1),
  600px 440px 0 0 rgba(48, 53, 56, 1), 610px 440px 0 0 rgba(48, 53, 56, 1),
  620px 440px 0 0 rgba(48, 53, 56, 1), 630px 440px 0 0 rgba(48, 53, 56, 1),
  640px 440px 0 0 rgba(48, 53, 56, 1), 650px 440px 0 0 rgba(48, 53, 56, 1),
  660px 440px 0 0 rgba(48, 53, 56, 1), 670px 440px 0 0 rgba(48, 53, 56, 1),
  680px 440px 0 0 rgba(48, 53, 56, 1), 690px 440px 0 0 rgba(48, 53, 56, 1),
  700px 440px 0 0 rgba(48, 53, 56, 1), 710px 440px 0 0 rgba(48, 53, 56, 1),
  720px 440px 0 0 rgba(48, 53, 56, 1), 730px 440px 0 0 rgba(48, 53, 56, 1),
  740px 440px 0 0 rgba(48, 53, 56, 1), 750px 440px 0 0 rgba(48, 53, 56, 1),
  760px 440px 0 0 rgba(48, 53, 56, 1), 770px 440px 0 0 rgba(48, 53, 56, 1),
  780px 440px 0 0 rgba(48, 53, 56, 1), 790px 440px 0 0 rgba(48, 53, 56, 1),
  800px 440px 0 0 rgba(48, 53, 56, 1), 810px 440px 0 0 rgba(48, 53, 56, 1),
  820px 440px 0 0 rgba(48, 53, 56, 1), 830px 440px 0 0 rgba(48, 53, 56, 1),
  840px 440px 0 0 rgba(48, 53, 56, 1), 850px 440px 0 0 rgba(48, 53, 56, 1),
  860px 440px 0 0 rgba(48, 53, 56, 1), 870px 440px 0 0 rgba(48, 53, 56, 1),
  880px 440px 0 0 rgba(48, 53, 56, 1), 890px 440px 0 0 rgba(48, 53, 56, 1),
  900px 440px 0 0 rgba(48, 53, 56, 1), 910px 440px 0 0 rgba(48, 53, 56, 1),
  920px 440px 0 0 rgba(48, 53, 56, 1), 930px 440px 0 0 rgba(48, 53, 56, 1),
  940px 440px 0 0 rgba(48, 53, 56, 1), 950px 440px 0 0 rgba(48, 53, 56, 1),
  960px 440px 0 0 rgba(48, 53, 56, 1), 970px 440px 0 0 rgba(48, 53, 56, 1),
  980px 440px 0 0 rgba(48, 53, 56, 1), 990px 440px 0 0 rgba(48, 53, 56, 1),
  1000px 440px 0 0 rgba(48, 53, 56, 1), 10px 450px 0 0 rgba(28, 32, 34, 1),
  20px 450px 0 0 rgba(219, 222, 232, 1), 30px 450px 0 0 rgba(111, 114, 121, 1),
  40px 450px 0 0 rgba(28, 32, 34, 1), 50px 450px 0 0 rgba(48, 53, 56, 1),
  60px 450px 0 0 rgba(48, 53, 56, 1), 70px 450px 0 0 rgba(48, 53, 56, 1),
  80px 450px 0 0 rgba(48, 53, 56, 1), 90px 450px 0 0 rgba(48, 53, 56, 1),
  100px 450px 0 0 rgba(48, 53, 56, 1), 110px 450px 0 0 rgba(48, 53, 56, 1),
  120px 450px 0 0 rgba(48, 53, 56, 1), 130px 450px 0 0 rgba(48, 53, 56, 1),
  140px 450px 0 0 rgba(48, 53, 56, 1), 150px 450px 0 0 rgba(48, 53, 56, 1),
  160px 450px 0 0 rgba(48, 53, 56, 1), 170px 450px 0 0 rgba(48, 53, 56, 1),
  180px 450px 0 0 rgba(48, 53, 56, 1), 190px 450px 0 0 rgba(48, 53, 56, 1),
  200px 450px 0 0 rgba(48, 53, 56, 1), 210px 450px 0 0 rgba(48, 53, 56, 1),
  220px 450px 0 0 rgba(48, 53, 56, 1), 230px 450px 0 0 rgba(48, 53, 56, 1),
  240px 450px 0 0 rgba(48, 53, 56, 1), 250px 450px 0 0 rgba(48, 53, 56, 1),
  260px 450px 0 0 rgba(48, 53, 56, 1), 270px 450px 0 0 rgba(48, 53, 56, 1),
  280px 450px 0 0 rgba(48, 53, 56, 1), 290px 450px 0 0 rgba(48, 53, 56, 1),
  300px 450px 0 0 rgba(48, 53, 56, 1), 310px 450px 0 0 rgba(48, 53, 56, 1),
  320px 450px 0 0 rgba(48, 53, 56, 1), 330px 450px 0 0 rgba(48, 53, 56, 1),
  340px 450px 0 0 rgba(48, 53, 56, 1), 350px 450px 0 0 rgba(48, 53, 56, 1),
  360px 450px 0 0 rgba(48, 53, 56, 1), 370px 450px 0 0 rgba(48, 53, 56, 1),
  380px 450px 0 0 rgba(48, 53, 56, 1), 390px 450px 0 0 rgba(48, 53, 56, 1),
  400px 450px 0 0 rgba(48, 53, 56, 1), 410px 450px 0 0 rgba(48, 53, 56, 1),
  420px 450px 0 0 rgba(48, 53, 56, 1), 430px 450px 0 0 rgba(48, 53, 56, 1),
  440px 450px 0 0 rgba(48, 53, 56, 1), 450px 450px 0 0 rgba(48, 53, 56, 1),
  460px 450px 0 0 rgba(48, 53, 56, 1), 470px 450px 0 0 rgba(48, 53, 56, 1),
  480px 450px 0 0 rgba(48, 53, 56, 1), 490px 450px 0 0 rgba(48, 53, 56, 1),
  500px 450px 0 0 rgba(48, 53, 56, 1), 510px 450px 0 0 rgba(48, 53, 56, 1),
  520px 450px 0 0 rgba(48, 53, 56, 1), 530px 450px 0 0 rgba(48, 53, 56, 1),
  540px 450px 0 0 rgba(48, 53, 56, 1), 550px 450px 0 0 rgba(48, 53, 56, 1),
  560px 450px 0 0 rgba(48, 53, 56, 1), 570px 450px 0 0 rgba(48, 53, 56, 1),
  580px 450px 0 0 rgba(48, 53, 56, 1), 590px 450px 0 0 rgba(48, 53, 56, 1),
  600px 450px 0 0 rgba(48, 53, 56, 1), 610px 450px 0 0 rgba(48, 53, 56, 1),
  620px 450px 0 0 rgba(48, 53, 56, 1), 630px 450px 0 0 rgba(48, 53, 56, 1),
  640px 450px 0 0 rgba(48, 53, 56, 1), 650px 450px 0 0 rgba(48, 53, 56, 1),
  660px 450px 0 0 rgba(48, 53, 56, 1), 670px 450px 0 0 rgba(48, 53, 56, 1),
  680px 450px 0 0 rgba(48, 53, 56, 1), 690px 450px 0 0 rgba(48, 53, 56, 1),
  700px 450px 0 0 rgba(48, 53, 56, 1), 710px 450px 0 0 rgba(48, 53, 56, 1),
  720px 450px 0 0 rgba(48, 53, 56, 1), 730px 450px 0 0 rgba(48, 53, 56, 1),
  740px 450px 0 0 rgba(48, 53, 56, 1), 750px 450px 0 0 rgba(48, 53, 56, 1),
  760px 450px 0 0 rgba(48, 53, 56, 1), 770px 450px 0 0 rgba(48, 53, 56, 1),
  780px 450px 0 0 rgba(48, 53, 56, 1), 790px 450px 0 0 rgba(48, 53, 56, 1),
  800px 450px 0 0 rgba(48, 53, 56, 1), 810px 450px 0 0 rgba(48, 53, 56, 1),
  820px 450px 0 0 rgba(48, 53, 56, 1), 830px 450px 0 0 rgba(48, 53, 56, 1),
  840px 450px 0 0 rgba(48, 53, 56, 1), 850px 450px 0 0 rgba(48, 53, 56, 1),
  860px 450px 0 0 rgba(48, 53, 56, 1), 870px 450px 0 0 rgba(48, 53, 56, 1),
  880px 450px 0 0 rgba(48, 53, 56, 1), 890px 450px 0 0 rgba(48, 53, 56, 1),
  900px 450px 0 0 rgba(48, 53, 56, 1), 910px 450px 0 0 rgba(48, 53, 56, 1),
  920px 450px 0 0 rgba(48, 53, 56, 1), 930px 450px 0 0 rgba(48, 53, 56, 1),
  940px 450px 0 0 rgba(48, 53, 56, 1), 950px 450px 0 0 rgba(48, 53, 56, 1),
  960px 450px 0 0 rgba(48, 53, 56, 1), 970px 450px 0 0 rgba(48, 53, 56, 1),
  980px 450px 0 0 rgba(48, 53, 56, 1), 990px 450px 0 0 rgba(48, 53, 56, 1),
  1000px 450px 0 0 rgba(48, 53, 56, 1), 10px 460px 0 0 rgba(28, 32, 34, 1),
  20px 460px 0 0 rgba(219, 222, 232, 1), 30px 460px 0 0 rgba(111, 114, 121, 1),
  40px 460px 0 0 rgba(28, 32, 34, 1), 50px 460px 0 0 rgba(48, 53, 56, 1),
  60px 460px 0 0 rgba(48, 53, 56, 1), 70px 460px 0 0 rgba(48, 53, 56, 1),
  80px 460px 0 0 rgba(48, 53, 56, 1), 90px 460px 0 0 rgba(48, 53, 56, 1),
  100px 460px 0 0 rgba(48, 53, 56, 1), 110px 460px 0 0 rgba(48, 53, 56, 1),
  120px 460px 0 0 rgba(48, 53, 56, 1), 130px 460px 0 0 rgba(48, 53, 56, 1),
  140px 460px 0 0 rgba(48, 53, 56, 1), 150px 460px 0 0 rgba(48, 53, 56, 1),
  160px 460px 0 0 rgba(48, 53, 56, 1), 170px 460px 0 0 rgba(48, 53, 56, 1),
  180px 460px 0 0 rgba(48, 53, 56, 1), 190px 460px 0 0 rgba(48, 53, 56, 1),
  200px 460px 0 0 rgba(48, 53, 56, 1), 210px 460px 0 0 rgba(48, 53, 56, 1),
  220px 460px 0 0 rgba(48, 53, 56, 1), 230px 460px 0 0 rgba(48, 53, 56, 1),
  240px 460px 0 0 rgba(48, 53, 56, 1), 250px 460px 0 0 rgba(48, 53, 56, 1),
  260px 460px 0 0 rgba(48, 53, 56, 1), 270px 460px 0 0 rgba(48, 53, 56, 1),
  280px 460px 0 0 rgba(48, 53, 56, 1), 290px 460px 0 0 rgba(48, 53, 56, 1),
  300px 460px 0 0 rgba(48, 53, 56, 1), 310px 460px 0 0 rgba(48, 53, 56, 1),
  320px 460px 0 0 rgba(48, 53, 56, 1), 330px 460px 0 0 rgba(48, 53, 56, 1),
  340px 460px 0 0 rgba(48, 53, 56, 1), 350px 460px 0 0 rgba(48, 53, 56, 1),
  360px 460px 0 0 rgba(48, 53, 56, 1), 370px 460px 0 0 rgba(48, 53, 56, 1),
  380px 460px 0 0 rgba(48, 53, 56, 1), 390px 460px 0 0 rgba(48, 53, 56, 1),
  400px 460px 0 0 rgba(48, 53, 56, 1), 410px 460px 0 0 rgba(48, 53, 56, 1),
  420px 460px 0 0 rgba(48, 53, 56, 1), 430px 460px 0 0 rgba(48, 53, 56, 1),
  440px 460px 0 0 rgba(48, 53, 56, 1), 450px 460px 0 0 rgba(48, 53, 56, 1),
  460px 460px 0 0 rgba(48, 53, 56, 1), 470px 460px 0 0 rgba(48, 53, 56, 1),
  480px 460px 0 0 rgba(48, 53, 56, 1), 490px 460px 0 0 rgba(48, 53, 56, 1),
  500px 460px 0 0 rgba(48, 53, 56, 1), 510px 460px 0 0 rgba(48, 53, 56, 1),
  520px 460px 0 0 rgba(48, 53, 56, 1), 530px 460px 0 0 rgba(48, 53, 56, 1),
  540px 460px 0 0 rgba(48, 53, 56, 1), 550px 460px 0 0 rgba(48, 53, 56, 1),
  560px 460px 0 0 rgba(48, 53, 56, 1), 570px 460px 0 0 rgba(48, 53, 56, 1),
  580px 460px 0 0 rgba(48, 53, 56, 1), 590px 460px 0 0 rgba(48, 53, 56, 1),
  600px 460px 0 0 rgba(48, 53, 56, 1), 610px 460px 0 0 rgba(48, 53, 56, 1),
  620px 460px 0 0 rgba(48, 53, 56, 1), 630px 460px 0 0 rgba(48, 53, 56, 1),
  640px 460px 0 0 rgba(48, 53, 56, 1), 650px 460px 0 0 rgba(48, 53, 56, 1),
  660px 460px 0 0 rgba(48, 53, 56, 1), 670px 460px 0 0 rgba(48, 53, 56, 1),
  680px 460px 0 0 rgba(48, 53, 56, 1), 690px 460px 0 0 rgba(48, 53, 56, 1),
  700px 460px 0 0 rgba(48, 53, 56, 1), 710px 460px 0 0 rgba(48, 53, 56, 1),
  720px 460px 0 0 rgba(48, 53, 56, 1), 730px 460px 0 0 rgba(48, 53, 56, 1),
  740px 460px 0 0 rgba(48, 53, 56, 1), 750px 460px 0 0 rgba(48, 53, 56, 1),
  760px 460px 0 0 rgba(48, 53, 56, 1), 770px 460px 0 0 rgba(48, 53, 56, 1),
  780px 460px 0 0 rgba(48, 53, 56, 1), 790px 460px 0 0 rgba(48, 53, 56, 1),
  800px 460px 0 0 rgba(48, 53, 56, 1), 810px 460px 0 0 rgba(48, 53, 56, 1),
  820px 460px 0 0 rgba(48, 53, 56, 1), 830px 460px 0 0 rgba(48, 53, 56, 1),
  840px 460px 0 0 rgba(48, 53, 56, 1), 850px 460px 0 0 rgba(48, 53, 56, 1),
  860px 460px 0 0 rgba(48, 53, 56, 1), 870px 460px 0 0 rgba(48, 53, 56, 1),
  880px 460px 0 0 rgba(48, 53, 56, 1), 890px 460px 0 0 rgba(48, 53, 56, 1),
  900px 460px 0 0 rgba(48, 53, 56, 1), 910px 460px 0 0 rgba(48, 53, 56, 1),
  920px 460px 0 0 rgba(48, 53, 56, 1), 930px 460px 0 0 rgba(48, 53, 56, 1),
  940px 460px 0 0 rgba(48, 53, 56, 1), 950px 460px 0 0 rgba(48, 53, 56, 1),
  960px 460px 0 0 rgba(48, 53, 56, 1), 970px 460px 0 0 rgba(48, 53, 56, 1),
  980px 460px 0 0 rgba(48, 53, 56, 1), 990px 460px 0 0 rgba(48, 53, 56, 1),
  1000px 460px 0 0 rgba(48, 53, 56, 1), 10px 470px 0 0 rgba(28, 32, 34, 1),
  20px 470px 0 0 rgba(219, 222, 232, 1), 30px 470px 0 0 rgba(111, 114, 121, 1),
  40px 470px 0 0 rgba(28, 32, 34, 1), 50px 470px 0 0 rgba(48, 53, 56, 1),
  60px 470px 0 0 rgba(48, 53, 56, 1), 70px 470px 0 0 rgba(48, 53, 56, 1),
  80px 470px 0 0 rgba(48, 53, 56, 1), 90px 470px 0 0 rgba(48, 53, 56, 1),
  100px 470px 0 0 rgba(48, 53, 56, 1), 110px 470px 0 0 rgba(48, 53, 56, 1),
  120px 470px 0 0 rgba(48, 53, 56, 1), 130px 470px 0 0 rgba(48, 53, 56, 1),
  140px 470px 0 0 rgba(48, 53, 56, 1), 150px 470px 0 0 rgba(48, 53, 56, 1),
  160px 470px 0 0 rgba(48, 53, 56, 1), 170px 470px 0 0 rgba(48, 53, 56, 1),
  180px 470px 0 0 rgba(48, 53, 56, 1), 190px 470px 0 0 rgba(48, 53, 56, 1),
  200px 470px 0 0 rgba(48, 53, 56, 1), 210px 470px 0 0 rgba(48, 53, 56, 1),
  220px 470px 0 0 rgba(48, 53, 56, 1), 230px 470px 0 0 rgba(48, 53, 56, 1),
  240px 470px 0 0 rgba(48, 53, 56, 1), 250px 470px 0 0 rgba(48, 53, 56, 1),
  260px 470px 0 0 rgba(48, 53, 56, 1), 270px 470px 0 0 rgba(48, 53, 56, 1),
  280px 470px 0 0 rgba(48, 53, 56, 1), 290px 470px 0 0 rgba(48, 53, 56, 1),
  300px 470px 0 0 rgba(48, 53, 56, 1), 310px 470px 0 0 rgba(48, 53, 56, 1),
  320px 470px 0 0 rgba(48, 53, 56, 1), 330px 470px 0 0 rgba(48, 53, 56, 1),
  340px 470px 0 0 rgba(48, 53, 56, 1), 350px 470px 0 0 rgba(48, 53, 56, 1),
  360px 470px 0 0 rgba(48, 53, 56, 1), 370px 470px 0 0 rgba(48, 53, 56, 1),
  380px 470px 0 0 rgba(48, 53, 56, 1), 390px 470px 0 0 rgba(48, 53, 56, 1),
  400px 470px 0 0 rgba(48, 53, 56, 1), 410px 470px 0 0 rgba(48, 53, 56, 1),
  420px 470px 0 0 rgba(48, 53, 56, 1), 430px 470px 0 0 rgba(48, 53, 56, 1),
  440px 470px 0 0 rgba(48, 53, 56, 1), 450px 470px 0 0 rgba(48, 53, 56, 1),
  460px 470px 0 0 rgba(48, 53, 56, 1), 470px 470px 0 0 rgba(48, 53, 56, 1),
  480px 470px 0 0 rgba(48, 53, 56, 1), 490px 470px 0 0 rgba(48, 53, 56, 1),
  500px 470px 0 0 rgba(48, 53, 56, 1), 510px 470px 0 0 rgba(48, 53, 56, 1),
  520px 470px 0 0 rgba(48, 53, 56, 1), 530px 470px 0 0 rgba(48, 53, 56, 1),
  540px 470px 0 0 rgba(48, 53, 56, 1), 550px 470px 0 0 rgba(48, 53, 56, 1),
  560px 470px 0 0 rgba(48, 53, 56, 1), 570px 470px 0 0 rgba(48, 53, 56, 1),
  580px 470px 0 0 rgba(48, 53, 56, 1), 590px 470px 0 0 rgba(48, 53, 56, 1),
  600px 470px 0 0 rgba(48, 53, 56, 1), 610px 470px 0 0 rgba(48, 53, 56, 1),
  620px 470px 0 0 rgba(48, 53, 56, 1), 630px 470px 0 0 rgba(48, 53, 56, 1),
  640px 470px 0 0 rgba(48, 53, 56, 1), 650px 470px 0 0 rgba(48, 53, 56, 1),
  660px 470px 0 0 rgba(48, 53, 56, 1), 670px 470px 0 0 rgba(48, 53, 56, 1),
  680px 470px 0 0 rgba(48, 53, 56, 1), 690px 470px 0 0 rgba(48, 53, 56, 1),
  700px 470px 0 0 rgba(48, 53, 56, 1), 710px 470px 0 0 rgba(48, 53, 56, 1),
  720px 470px 0 0 rgba(48, 53, 56, 1), 730px 470px 0 0 rgba(48, 53, 56, 1),
  740px 470px 0 0 rgba(48, 53, 56, 1), 750px 470px 0 0 rgba(48, 53, 56, 1),
  760px 470px 0 0 rgba(48, 53, 56, 1), 770px 470px 0 0 rgba(48, 53, 56, 1),
  780px 470px 0 0 rgba(48, 53, 56, 1), 790px 470px 0 0 rgba(48, 53, 56, 1),
  800px 470px 0 0 rgba(48, 53, 56, 1), 810px 470px 0 0 rgba(48, 53, 56, 1),
  820px 470px 0 0 rgba(48, 53, 56, 1), 830px 470px 0 0 rgba(48, 53, 56, 1),
  840px 470px 0 0 rgba(48, 53, 56, 1), 850px 470px 0 0 rgba(48, 53, 56, 1),
  860px 470px 0 0 rgba(48, 53, 56, 1), 870px 470px 0 0 rgba(48, 53, 56, 1),
  880px 470px 0 0 rgba(48, 53, 56, 1), 890px 470px 0 0 rgba(48, 53, 56, 1),
  900px 470px 0 0 rgba(48, 53, 56, 1), 910px 470px 0 0 rgba(48, 53, 56, 1),
  920px 470px 0 0 rgba(48, 53, 56, 1), 930px 470px 0 0 rgba(48, 53, 56, 1),
  940px 470px 0 0 rgba(48, 53, 56, 1), 950px 470px 0 0 rgba(48, 53, 56, 1),
  960px 470px 0 0 rgba(48, 53, 56, 1), 970px 470px 0 0 rgba(48, 53, 56, 1),
  980px 470px 0 0 rgba(48, 53, 56, 1), 990px 470px 0 0 rgba(48, 53, 56, 1),
  1000px 470px 0 0 rgba(48, 53, 56, 1), 10px 480px 0 0 rgba(28, 32, 34, 1),
  20px 480px 0 0 rgba(219, 222, 232, 1), 30px 480px 0 0 rgba(111, 114, 121, 1),
  40px 480px 0 0 rgba(28, 32, 34, 1), 50px 480px 0 0 rgba(48, 53, 56, 1),
  60px 480px 0 0 rgba(48, 53, 56, 1), 70px 480px 0 0 rgba(48, 53, 56, 1),
  80px 480px 0 0 rgba(48, 53, 56, 1), 90px 480px 0 0 rgba(48, 53, 56, 1),
  100px 480px 0 0 rgba(48, 53, 56, 1), 110px 480px 0 0 rgba(48, 53, 56, 1),
  120px 480px 0 0 rgba(48, 53, 56, 1), 130px 480px 0 0 rgba(48, 53, 56, 1),
  140px 480px 0 0 rgba(48, 53, 56, 1), 150px 480px 0 0 rgba(48, 53, 56, 1),
  160px 480px 0 0 rgba(48, 53, 56, 1), 170px 480px 0 0 rgba(48, 53, 56, 1),
  180px 480px 0 0 rgba(48, 53, 56, 1), 190px 480px 0 0 rgba(48, 53, 56, 1),
  200px 480px 0 0 rgba(48, 53, 56, 1), 210px 480px 0 0 rgba(48, 53, 56, 1),
  220px 480px 0 0 rgba(48, 53, 56, 1), 230px 480px 0 0 rgba(48, 53, 56, 1),
  240px 480px 0 0 rgba(48, 53, 56, 1), 250px 480px 0 0 rgba(48, 53, 56, 1),
  260px 480px 0 0 rgba(48, 53, 56, 1), 270px 480px 0 0 rgba(48, 53, 56, 1),
  280px 480px 0 0 rgba(48, 53, 56, 1), 290px 480px 0 0 rgba(48, 53, 56, 1),
  300px 480px 0 0 rgba(48, 53, 56, 1), 310px 480px 0 0 rgba(48, 53, 56, 1),
  320px 480px 0 0 rgba(48, 53, 56, 1), 330px 480px 0 0 rgba(48, 53, 56, 1),
  340px 480px 0 0 rgba(48, 53, 56, 1), 350px 480px 0 0 rgba(48, 53, 56, 1),
  360px 480px 0 0 rgba(48, 53, 56, 1), 370px 480px 0 0 rgba(48, 53, 56, 1),
  380px 480px 0 0 rgba(48, 53, 56, 1), 390px 480px 0 0 rgba(48, 53, 56, 1),
  400px 480px 0 0 rgba(48, 53, 56, 1), 410px 480px 0 0 rgba(48, 53, 56, 1),
  420px 480px 0 0 rgba(48, 53, 56, 1), 430px 480px 0 0 rgba(48, 53, 56, 1),
  440px 480px 0 0 rgba(48, 53, 56, 1), 450px 480px 0 0 rgba(48, 53, 56, 1),
  460px 480px 0 0 rgba(48, 53, 56, 1), 470px 480px 0 0 rgba(48, 53, 56, 1),
  480px 480px 0 0 rgba(48, 53, 56, 1), 490px 480px 0 0 rgba(48, 53, 56, 1),
  500px 480px 0 0 rgba(48, 53, 56, 1), 510px 480px 0 0 rgba(48, 53, 56, 1),
  520px 480px 0 0 rgba(48, 53, 56, 1), 530px 480px 0 0 rgba(48, 53, 56, 1),
  540px 480px 0 0 rgba(48, 53, 56, 1), 550px 480px 0 0 rgba(48, 53, 56, 1),
  560px 480px 0 0 rgba(48, 53, 56, 1), 570px 480px 0 0 rgba(48, 53, 56, 1),
  580px 480px 0 0 rgba(48, 53, 56, 1), 590px 480px 0 0 rgba(48, 53, 56, 1),
  600px 480px 0 0 rgba(48, 53, 56, 1), 610px 480px 0 0 rgba(48, 53, 56, 1),
  620px 480px 0 0 rgba(48, 53, 56, 1), 630px 480px 0 0 rgba(48, 53, 56, 1),
  640px 480px 0 0 rgba(48, 53, 56, 1), 650px 480px 0 0 rgba(48, 53, 56, 1),
  660px 480px 0 0 rgba(48, 53, 56, 1), 670px 480px 0 0 rgba(48, 53, 56, 1),
  680px 480px 0 0 rgba(48, 53, 56, 1), 690px 480px 0 0 rgba(48, 53, 56, 1),
  700px 480px 0 0 rgba(48, 53, 56, 1), 710px 480px 0 0 rgba(48, 53, 56, 1),
  720px 480px 0 0 rgba(48, 53, 56, 1), 730px 480px 0 0 rgba(48, 53, 56, 1),
  740px 480px 0 0 rgba(48, 53, 56, 1), 750px 480px 0 0 rgba(48, 53, 56, 1),
  760px 480px 0 0 rgba(48, 53, 56, 1), 770px 480px 0 0 rgba(48, 53, 56, 1),
  780px 480px 0 0 rgba(48, 53, 56, 1), 790px 480px 0 0 rgba(48, 53, 56, 1),
  800px 480px 0 0 rgba(48, 53, 56, 1), 810px 480px 0 0 rgba(48, 53, 56, 1),
  820px 480px 0 0 rgba(48, 53, 56, 1), 830px 480px 0 0 rgba(48, 53, 56, 1),
  840px 480px 0 0 rgba(48, 53, 56, 1), 850px 480px 0 0 rgba(48, 53, 56, 1),
  860px 480px 0 0 rgba(48, 53, 56, 1), 870px 480px 0 0 rgba(48, 53, 56, 1),
  880px 480px 0 0 rgba(48, 53, 56, 1), 890px 480px 0 0 rgba(48, 53, 56, 1),
  900px 480px 0 0 rgba(48, 53, 56, 1), 910px 480px 0 0 rgba(48, 53, 56, 1),
  920px 480px 0 0 rgba(48, 53, 56, 1), 930px 480px 0 0 rgba(48, 53, 56, 1),
  940px 480px 0 0 rgba(48, 53, 56, 1), 950px 480px 0 0 rgba(48, 53, 56, 1),
  960px 480px 0 0 rgba(48, 53, 56, 1), 970px 480px 0 0 rgba(48, 53, 56, 1),
  980px 480px 0 0 rgba(48, 53, 56, 1), 990px 480px 0 0 rgba(48, 53, 56, 1),
  1000px 480px 0 0 rgba(48, 53, 56, 1), 10px 490px 0 0 rgba(28, 32, 34, 1),
  20px 490px 0 0 rgba(219, 222, 232, 1), 30px 490px 0 0 rgba(111, 114, 121, 1),
  40px 490px 0 0 rgba(28, 32, 34, 1), 50px 490px 0 0 rgba(48, 53, 56, 1),
  60px 490px 0 0 rgba(48, 53, 56, 1), 70px 490px 0 0 rgba(48, 53, 56, 1),
  80px 490px 0 0 rgba(48, 53, 56, 1), 90px 490px 0 0 rgba(48, 53, 56, 1),
  100px 490px 0 0 rgba(48, 53, 56, 1), 110px 490px 0 0 rgba(48, 53, 56, 1),
  120px 490px 0 0 rgba(48, 53, 56, 1), 130px 490px 0 0 rgba(48, 53, 56, 1),
  140px 490px 0 0 rgba(48, 53, 56, 1), 150px 490px 0 0 rgba(48, 53, 56, 1),
  160px 490px 0 0 rgba(48, 53, 56, 1), 170px 490px 0 0 rgba(48, 53, 56, 1),
  180px 490px 0 0 rgba(48, 53, 56, 1), 190px 490px 0 0 rgba(48, 53, 56, 1),
  200px 490px 0 0 rgba(48, 53, 56, 1), 210px 490px 0 0 rgba(48, 53, 56, 1),
  220px 490px 0 0 rgba(48, 53, 56, 1), 230px 490px 0 0 rgba(48, 53, 56, 1),
  240px 490px 0 0 rgba(48, 53, 56, 1), 250px 490px 0 0 rgba(48, 53, 56, 1),
  260px 490px 0 0 rgba(48, 53, 56, 1), 270px 490px 0 0 rgba(48, 53, 56, 1),
  280px 490px 0 0 rgba(48, 53, 56, 1), 290px 490px 0 0 rgba(48, 53, 56, 1),
  300px 490px 0 0 rgba(48, 53, 56, 1), 310px 490px 0 0 rgba(48, 53, 56, 1),
  320px 490px 0 0 rgba(48, 53, 56, 1), 330px 490px 0 0 rgba(48, 53, 56, 1),
  340px 490px 0 0 rgba(48, 53, 56, 1), 350px 490px 0 0 rgba(48, 53, 56, 1),
  360px 490px 0 0 rgba(48, 53, 56, 1), 370px 490px 0 0 rgba(48, 53, 56, 1),
  380px 490px 0 0 rgba(48, 53, 56, 1), 390px 490px 0 0 rgba(48, 53, 56, 1),
  400px 490px 0 0 rgba(48, 53, 56, 1), 410px 490px 0 0 rgba(48, 53, 56, 1),
  420px 490px 0 0 rgba(48, 53, 56, 1), 430px 490px 0 0 rgba(48, 53, 56, 1),
  440px 490px 0 0 rgba(48, 53, 56, 1), 450px 490px 0 0 rgba(48, 53, 56, 1),
  460px 490px 0 0 rgba(48, 53, 56, 1), 470px 490px 0 0 rgba(48, 53, 56, 1),
  480px 490px 0 0 rgba(48, 53, 56, 1), 490px 490px 0 0 rgba(48, 53, 56, 1),
  500px 490px 0 0 rgba(48, 53, 56, 1), 510px 490px 0 0 rgba(48, 53, 56, 1),
  520px 490px 0 0 rgba(48, 53, 56, 1), 530px 490px 0 0 rgba(48, 53, 56, 1),
  540px 490px 0 0 rgba(48, 53, 56, 1), 550px 490px 0 0 rgba(48, 53, 56, 1),
  560px 490px 0 0 rgba(48, 53, 56, 1), 570px 490px 0 0 rgba(48, 53, 56, 1),
  580px 490px 0 0 rgba(48, 53, 56, 1), 590px 490px 0 0 rgba(48, 53, 56, 1),
  600px 490px 0 0 rgba(48, 53, 56, 1), 610px 490px 0 0 rgba(48, 53, 56, 1),
  620px 490px 0 0 rgba(48, 53, 56, 1), 630px 490px 0 0 rgba(48, 53, 56, 1),
  640px 490px 0 0 rgba(48, 53, 56, 1), 650px 490px 0 0 rgba(48, 53, 56, 1),
  660px 490px 0 0 rgba(48, 53, 56, 1), 670px 490px 0 0 rgba(48, 53, 56, 1),
  680px 490px 0 0 rgba(48, 53, 56, 1), 690px 490px 0 0 rgba(48, 53, 56, 1),
  700px 490px 0 0 rgba(48, 53, 56, 1), 710px 490px 0 0 rgba(48, 53, 56, 1),
  720px 490px 0 0 rgba(48, 53, 56, 1), 730px 490px 0 0 rgba(48, 53, 56, 1),
  740px 490px 0 0 rgba(48, 53, 56, 1), 750px 490px 0 0 rgba(48, 53, 56, 1),
  760px 490px 0 0 rgba(48, 53, 56, 1), 770px 490px 0 0 rgba(48, 53, 56, 1),
  780px 490px 0 0 rgba(48, 53, 56, 1), 790px 490px 0 0 rgba(48, 53, 56, 1),
  800px 490px 0 0 rgba(48, 53, 56, 1), 810px 490px 0 0 rgba(48, 53, 56, 1),
  820px 490px 0 0 rgba(48, 53, 56, 1), 830px 490px 0 0 rgba(48, 53, 56, 1),
  840px 490px 0 0 rgba(48, 53, 56, 1), 850px 490px 0 0 rgba(48, 53, 56, 1),
  860px 490px 0 0 rgba(48, 53, 56, 1), 870px 490px 0 0 rgba(48, 53, 56, 1),
  880px 490px 0 0 rgba(48, 53, 56, 1), 890px 490px 0 0 rgba(48, 53, 56, 1),
  900px 490px 0 0 rgba(48, 53, 56, 1), 910px 490px 0 0 rgba(48, 53, 56, 1),
  920px 490px 0 0 rgba(48, 53, 56, 1), 930px 490px 0 0 rgba(48, 53, 56, 1),
  940px 490px 0 0 rgba(48, 53, 56, 1), 950px 490px 0 0 rgba(48, 53, 56, 1),
  960px 490px 0 0 rgba(48, 53, 56, 1), 970px 490px 0 0 rgba(48, 53, 56, 1),
  980px 490px 0 0 rgba(48, 53, 56, 1), 990px 490px 0 0 rgba(48, 53, 56, 1),
  1000px 490px 0 0 rgba(48, 53, 56, 1), 10px 500px 0 0 rgba(28, 32, 34, 1),
  20px 500px 0 0 rgba(219, 222, 232, 1), 30px 500px 0 0 rgba(111, 114, 121, 1),
  40px 500px 0 0 rgba(28, 32, 34, 1), 50px 500px 0 0 rgba(48, 53, 56, 1),
  60px 500px 0 0 rgba(48, 53, 56, 1), 70px 500px 0 0 rgba(48, 53, 56, 1),
  80px 500px 0 0 rgba(48, 53, 56, 1), 90px 500px 0 0 rgba(48, 53, 56, 1),
  100px 500px 0 0 rgba(48, 53, 56, 1), 110px 500px 0 0 rgba(48, 53, 56, 1),
  120px 500px 0 0 rgba(48, 53, 56, 1), 130px 500px 0 0 rgba(48, 53, 56, 1),
  140px 500px 0 0 rgba(48, 53, 56, 1), 150px 500px 0 0 rgba(48, 53, 56, 1),
  160px 500px 0 0 rgba(48, 53, 56, 1), 170px 500px 0 0 rgba(48, 53, 56, 1),
  180px 500px 0 0 rgba(48, 53, 56, 1), 190px 500px 0 0 rgba(48, 53, 56, 1),
  200px 500px 0 0 rgba(48, 53, 56, 1), 210px 500px 0 0 rgba(48, 53, 56, 1),
  220px 500px 0 0 rgba(48, 53, 56, 1), 230px 500px 0 0 rgba(48, 53, 56, 1),
  240px 500px 0 0 rgba(48, 53, 56, 1), 250px 500px 0 0 rgba(48, 53, 56, 1),
  260px 500px 0 0 rgba(48, 53, 56, 1), 270px 500px 0 0 rgba(48, 53, 56, 1),
  280px 500px 0 0 rgba(48, 53, 56, 1), 290px 500px 0 0 rgba(48, 53, 56, 1),
  300px 500px 0 0 rgba(48, 53, 56, 1), 310px 500px 0 0 rgba(48, 53, 56, 1),
  320px 500px 0 0 rgba(48, 53, 56, 1), 330px 500px 0 0 rgba(48, 53, 56, 1),
  340px 500px 0 0 rgba(48, 53, 56, 1), 350px 500px 0 0 rgba(48, 53, 56, 1),
  360px 500px 0 0 rgba(48, 53, 56, 1), 370px 500px 0 0 rgba(48, 53, 56, 1),
  380px 500px 0 0 rgba(48, 53, 56, 1), 390px 500px 0 0 rgba(48, 53, 56, 1),
  400px 500px 0 0 rgba(48, 53, 56, 1), 410px 500px 0 0 rgba(48, 53, 56, 1),
  420px 500px 0 0 rgba(48, 53, 56, 1), 430px 500px 0 0 rgba(48, 53, 56, 1),
  440px 500px 0 0 rgba(48, 53, 56, 1), 450px 500px 0 0 rgba(48, 53, 56, 1),
  460px 500px 0 0 rgba(48, 53, 56, 1), 470px 500px 0 0 rgba(48, 53, 56, 1),
  480px 500px 0 0 rgba(48, 53, 56, 1), 490px 500px 0 0 rgba(48, 53, 56, 1),
  500px 500px 0 0 rgba(48, 53, 56, 1), 510px 500px 0 0 rgba(48, 53, 56, 1),
  520px 500px 0 0 rgba(48, 53, 56, 1), 530px 500px 0 0 rgba(48, 53, 56, 1),
  540px 500px 0 0 rgba(48, 53, 56, 1), 550px 500px 0 0 rgba(48, 53, 56, 1),
  560px 500px 0 0 rgba(48, 53, 56, 1), 570px 500px 0 0 rgba(48, 53, 56, 1),
  580px 500px 0 0 rgba(48, 53, 56, 1), 590px 500px 0 0 rgba(48, 53, 56, 1),
  600px 500px 0 0 rgba(48, 53, 56, 1), 610px 500px 0 0 rgba(48, 53, 56, 1),
  620px 500px 0 0 rgba(48, 53, 56, 1), 630px 500px 0 0 rgba(48, 53, 56, 1),
  640px 500px 0 0 rgba(48, 53, 56, 1), 650px 500px 0 0 rgba(48, 53, 56, 1),
  660px 500px 0 0 rgba(48, 53, 56, 1), 670px 500px 0 0 rgba(48, 53, 56, 1),
  680px 500px 0 0 rgba(48, 53, 56, 1), 690px 500px 0 0 rgba(48, 53, 56, 1),
  700px 500px 0 0 rgba(48, 53, 56, 1), 710px 500px 0 0 rgba(48, 53, 56, 1),
  720px 500px 0 0 rgba(48, 53, 56, 1), 730px 500px 0 0 rgba(48, 53, 56, 1),
  740px 500px 0 0 rgba(48, 53, 56, 1), 750px 500px 0 0 rgba(48, 53, 56, 1),
  760px 500px 0 0 rgba(48, 53, 56, 1), 770px 500px 0 0 rgba(48, 53, 56, 1),
  780px 500px 0 0 rgba(48, 53, 56, 1), 790px 500px 0 0 rgba(48, 53, 56, 1),
  800px 500px 0 0 rgba(48, 53, 56, 1), 810px 500px 0 0 rgba(48, 53, 56, 1),
  820px 500px 0 0 rgba(48, 53, 56, 1), 830px 500px 0 0 rgba(48, 53, 56, 1),
  840px 500px 0 0 rgba(48, 53, 56, 1), 850px 500px 0 0 rgba(48, 53, 56, 1),
  860px 500px 0 0 rgba(48, 53, 56, 1), 870px 500px 0 0 rgba(48, 53, 56, 1),
  880px 500px 0 0 rgba(48, 53, 56, 1), 890px 500px 0 0 rgba(48, 53, 56, 1),
  900px 500px 0 0 rgba(48, 53, 56, 1), 910px 500px 0 0 rgba(48, 53, 56, 1),
  920px 500px 0 0 rgba(48, 53, 56, 1), 930px 500px 0 0 rgba(48, 53, 56, 1),
  940px 500px 0 0 rgba(48, 53, 56, 1), 950px 500px 0 0 rgba(48, 53, 56, 1),
  960px 500px 0 0 rgba(48, 53, 56, 1), 970px 500px 0 0 rgba(48, 53, 56, 1),
  980px 500px 0 0 rgba(48, 53, 56, 1), 990px 500px 0 0 rgba(48, 53, 56, 1),
  1000px 500px 0 0 rgba(48, 53, 56, 1), 10px 510px 0 0 rgba(28, 32, 34, 1),
  20px 510px 0 0 rgba(219, 222, 232, 1), 30px 510px 0 0 rgba(111, 114, 121, 1),
  40px 510px 0 0 rgba(28, 32, 34, 1), 50px 510px 0 0 rgba(48, 53, 56, 1),
  60px 510px 0 0 rgba(48, 53, 56, 1), 70px 510px 0 0 rgba(48, 53, 56, 1),
  80px 510px 0 0 rgba(48, 53, 56, 1), 90px 510px 0 0 rgba(48, 53, 56, 1),
  100px 510px 0 0 rgba(48, 53, 56, 1), 110px 510px 0 0 rgba(48, 53, 56, 1),
  120px 510px 0 0 rgba(48, 53, 56, 1), 130px 510px 0 0 rgba(48, 53, 56, 1),
  140px 510px 0 0 rgba(48, 53, 56, 1), 150px 510px 0 0 rgba(48, 53, 56, 1),
  160px 510px 0 0 rgba(48, 53, 56, 1), 170px 510px 0 0 rgba(48, 53, 56, 1),
  180px 510px 0 0 rgba(48, 53, 56, 1), 190px 510px 0 0 rgba(48, 53, 56, 1),
  200px 510px 0 0 rgba(48, 53, 56, 1), 210px 510px 0 0 rgba(48, 53, 56, 1),
  220px 510px 0 0 rgba(48, 53, 56, 1), 230px 510px 0 0 rgba(48, 53, 56, 1),
  240px 510px 0 0 rgba(48, 53, 56, 1), 250px 510px 0 0 rgba(48, 53, 56, 1),
  260px 510px 0 0 rgba(48, 53, 56, 1), 270px 510px 0 0 rgba(48, 53, 56, 1),
  280px 510px 0 0 rgba(48, 53, 56, 1), 290px 510px 0 0 rgba(48, 53, 56, 1),
  300px 510px 0 0 rgba(48, 53, 56, 1), 310px 510px 0 0 rgba(48, 53, 56, 1),
  320px 510px 0 0 rgba(48, 53, 56, 1), 330px 510px 0 0 rgba(48, 53, 56, 1),
  340px 510px 0 0 rgba(48, 53, 56, 1), 350px 510px 0 0 rgba(48, 53, 56, 1),
  360px 510px 0 0 rgba(48, 53, 56, 1), 370px 510px 0 0 rgba(48, 53, 56, 1),
  380px 510px 0 0 rgba(48, 53, 56, 1), 390px 510px 0 0 rgba(48, 53, 56, 1),
  400px 510px 0 0 rgba(48, 53, 56, 1), 410px 510px 0 0 rgba(48, 53, 56, 1),
  420px 510px 0 0 rgba(48, 53, 56, 1), 430px 510px 0 0 rgba(48, 53, 56, 1),
  440px 510px 0 0 rgba(48, 53, 56, 1), 450px 510px 0 0 rgba(48, 53, 56, 1),
  460px 510px 0 0 rgba(48, 53, 56, 1), 470px 510px 0 0 rgba(48, 53, 56, 1),
  480px 510px 0 0 rgba(48, 53, 56, 1), 490px 510px 0 0 rgba(48, 53, 56, 1),
  500px 510px 0 0 rgba(48, 53, 56, 1), 510px 510px 0 0 rgba(48, 53, 56, 1),
  520px 510px 0 0 rgba(48, 53, 56, 1), 530px 510px 0 0 rgba(48, 53, 56, 1),
  540px 510px 0 0 rgba(48, 53, 56, 1), 550px 510px 0 0 rgba(48, 53, 56, 1),
  560px 510px 0 0 rgba(48, 53, 56, 1), 570px 510px 0 0 rgba(48, 53, 56, 1),
  580px 510px 0 0 rgba(48, 53, 56, 1), 590px 510px 0 0 rgba(48, 53, 56, 1),
  600px 510px 0 0 rgba(48, 53, 56, 1), 610px 510px 0 0 rgba(48, 53, 56, 1),
  620px 510px 0 0 rgba(48, 53, 56, 1), 630px 510px 0 0 rgba(48, 53, 56, 1),
  640px 510px 0 0 rgba(48, 53, 56, 1), 650px 510px 0 0 rgba(48, 53, 56, 1),
  660px 510px 0 0 rgba(48, 53, 56, 1), 670px 510px 0 0 rgba(48, 53, 56, 1),
  680px 510px 0 0 rgba(48, 53, 56, 1), 690px 510px 0 0 rgba(48, 53, 56, 1),
  700px 510px 0 0 rgba(48, 53, 56, 1), 710px 510px 0 0 rgba(48, 53, 56, 1),
  720px 510px 0 0 rgba(48, 53, 56, 1), 730px 510px 0 0 rgba(48, 53, 56, 1),
  740px 510px 0 0 rgba(48, 53, 56, 1), 750px 510px 0 0 rgba(48, 53, 56, 1),
  760px 510px 0 0 rgba(48, 53, 56, 1), 770px 510px 0 0 rgba(48, 53, 56, 1),
  780px 510px 0 0 rgba(48, 53, 56, 1), 790px 510px 0 0 rgba(48, 53, 56, 1),
  800px 510px 0 0 rgba(48, 53, 56, 1), 810px 510px 0 0 rgba(48, 53, 56, 1),
  820px 510px 0 0 rgba(48, 53, 56, 1), 830px 510px 0 0 rgba(48, 53, 56, 1),
  840px 510px 0 0 rgba(48, 53, 56, 1), 850px 510px 0 0 rgba(48, 53, 56, 1),
  860px 510px 0 0 rgba(48, 53, 56, 1), 870px 510px 0 0 rgba(48, 53, 56, 1),
  880px 510px 0 0 rgba(48, 53, 56, 1), 890px 510px 0 0 rgba(48, 53, 56, 1),
  900px 510px 0 0 rgba(48, 53, 56, 1), 910px 510px 0 0 rgba(48, 53, 56, 1),
  920px 510px 0 0 rgba(48, 53, 56, 1), 930px 510px 0 0 rgba(48, 53, 56, 1),
  940px 510px 0 0 rgba(48, 53, 56, 1), 950px 510px 0 0 rgba(48, 53, 56, 1),
  960px 510px 0 0 rgba(48, 53, 56, 1), 970px 510px 0 0 rgba(48, 53, 56, 1),
  980px 510px 0 0 rgba(48, 53, 56, 1), 990px 510px 0 0 rgba(48, 53, 56, 1),
  1000px 510px 0 0 rgba(48, 53, 56, 1), 10px 520px 0 0 rgba(28, 32, 34, 1),
  20px 520px 0 0 rgba(219, 222, 232, 1), 30px 520px 0 0 rgba(111, 114, 121, 1),
  40px 520px 0 0 rgba(28, 32, 34, 1), 50px 520px 0 0 rgba(48, 53, 56, 1),
  60px 520px 0 0 rgba(48, 53, 56, 1), 70px 520px 0 0 rgba(48, 53, 56, 1),
  80px 520px 0 0 rgba(48, 53, 56, 1), 90px 520px 0 0 rgba(48, 53, 56, 1),
  100px 520px 0 0 rgba(48, 53, 56, 1), 110px 520px 0 0 rgba(48, 53, 56, 1),
  120px 520px 0 0 rgba(48, 53, 56, 1), 130px 520px 0 0 rgba(48, 53, 56, 1),
  140px 520px 0 0 rgba(48, 53, 56, 1), 150px 520px 0 0 rgba(48, 53, 56, 1),
  160px 520px 0 0 rgba(48, 53, 56, 1), 170px 520px 0 0 rgba(48, 53, 56, 1),
  180px 520px 0 0 rgba(48, 53, 56, 1), 190px 520px 0 0 rgba(48, 53, 56, 1),
  200px 520px 0 0 rgba(48, 53, 56, 1), 210px 520px 0 0 rgba(48, 53, 56, 1),
  220px 520px 0 0 rgba(48, 53, 56, 1), 230px 520px 0 0 rgba(48, 53, 56, 1),
  240px 520px 0 0 rgba(48, 53, 56, 1), 250px 520px 0 0 rgba(48, 53, 56, 1),
  260px 520px 0 0 rgba(48, 53, 56, 1), 270px 520px 0 0 rgba(48, 53, 56, 1),
  280px 520px 0 0 rgba(48, 53, 56, 1), 290px 520px 0 0 rgba(48, 53, 56, 1),
  300px 520px 0 0 rgba(48, 53, 56, 1), 310px 520px 0 0 rgba(48, 53, 56, 1),
  320px 520px 0 0 rgba(48, 53, 56, 1), 330px 520px 0 0 rgba(48, 53, 56, 1),
  340px 520px 0 0 rgba(48, 53, 56, 1), 350px 520px 0 0 rgba(48, 53, 56, 1),
  360px 520px 0 0 rgba(48, 53, 56, 1), 370px 520px 0 0 rgba(48, 53, 56, 1),
  380px 520px 0 0 rgba(48, 53, 56, 1), 390px 520px 0 0 rgba(48, 53, 56, 1),
  400px 520px 0 0 rgba(48, 53, 56, 1), 410px 520px 0 0 rgba(48, 53, 56, 1),
  420px 520px 0 0 rgba(48, 53, 56, 1), 430px 520px 0 0 rgba(48, 53, 56, 1),
  440px 520px 0 0 rgba(48, 53, 56, 1), 450px 520px 0 0 rgba(48, 53, 56, 1),
  460px 520px 0 0 rgba(48, 53, 56, 1), 470px 520px 0 0 rgba(48, 53, 56, 1),
  480px 520px 0 0 rgba(48, 53, 56, 1), 490px 520px 0 0 rgba(48, 53, 56, 1),
  500px 520px 0 0 rgba(48, 53, 56, 1), 510px 520px 0 0 rgba(48, 53, 56, 1),
  520px 520px 0 0 rgba(48, 53, 56, 1), 530px 520px 0 0 rgba(48, 53, 56, 1),
  540px 520px 0 0 rgba(48, 53, 56, 1), 550px 520px 0 0 rgba(48, 53, 56, 1),
  560px 520px 0 0 rgba(48, 53, 56, 1), 570px 520px 0 0 rgba(48, 53, 56, 1),
  580px 520px 0 0 rgba(48, 53, 56, 1), 590px 520px 0 0 rgba(48, 53, 56, 1),
  600px 520px 0 0 rgba(48, 53, 56, 1), 610px 520px 0 0 rgba(48, 53, 56, 1),
  620px 520px 0 0 rgba(48, 53, 56, 1), 630px 520px 0 0 rgba(48, 53, 56, 1),
  640px 520px 0 0 rgba(48, 53, 56, 1), 650px 520px 0 0 rgba(48, 53, 56, 1),
  660px 520px 0 0 rgba(48, 53, 56, 1), 670px 520px 0 0 rgba(48, 53, 56, 1),
  680px 520px 0 0 rgba(48, 53, 56, 1), 690px 520px 0 0 rgba(48, 53, 56, 1),
  700px 520px 0 0 rgba(48, 53, 56, 1), 710px 520px 0 0 rgba(48, 53, 56, 1),
  720px 520px 0 0 rgba(48, 53, 56, 1), 730px 520px 0 0 rgba(48, 53, 56, 1),
  740px 520px 0 0 rgba(48, 53, 56, 1), 750px 520px 0 0 rgba(48, 53, 56, 1),
  760px 520px 0 0 rgba(48, 53, 56, 1), 770px 520px 0 0 rgba(48, 53, 56, 1),
  780px 520px 0 0 rgba(48, 53, 56, 1), 790px 520px 0 0 rgba(48, 53, 56, 1),
  800px 520px 0 0 rgba(48, 53, 56, 1), 810px 520px 0 0 rgba(48, 53, 56, 1),
  820px 520px 0 0 rgba(48, 53, 56, 1), 830px 520px 0 0 rgba(48, 53, 56, 1),
  840px 520px 0 0 rgba(48, 53, 56, 1), 850px 520px 0 0 rgba(48, 53, 56, 1),
  860px 520px 0 0 rgba(48, 53, 56, 1), 870px 520px 0 0 rgba(48, 53, 56, 1),
  880px 520px 0 0 rgba(48, 53, 56, 1), 890px 520px 0 0 rgba(48, 53, 56, 1),
  900px 520px 0 0 rgba(48, 53, 56, 1), 910px 520px 0 0 rgba(48, 53, 56, 1),
  920px 520px 0 0 rgba(48, 53, 56, 1), 930px 520px 0 0 rgba(48, 53, 56, 1),
  940px 520px 0 0 rgba(48, 53, 56, 1), 950px 520px 0 0 rgba(48, 53, 56, 1),
  960px 520px 0 0 rgba(48, 53, 56, 1), 970px 520px 0 0 rgba(48, 53, 56, 1),
  980px 520px 0 0 rgba(48, 53, 56, 1), 990px 520px 0 0 rgba(48, 53, 56, 1),
  1000px 520px 0 0 rgba(48, 53, 56, 1), 10px 530px 0 0 rgba(28, 32, 34, 1),
  20px 530px 0 0 rgba(219, 222, 232, 1), 30px 530px 0 0 rgba(111, 114, 121, 1),
  40px 530px 0 0 rgba(28, 32, 34, 1), 50px 530px 0 0 rgba(48, 53, 56, 1),
  60px 530px 0 0 rgba(48, 53, 56, 1), 70px 530px 0 0 rgba(48, 53, 56, 1),
  80px 530px 0 0 rgba(48, 53, 56, 1), 90px 530px 0 0 rgba(48, 53, 56, 1),
  100px 530px 0 0 rgba(48, 53, 56, 1), 110px 530px 0 0 rgba(48, 53, 56, 1),
  120px 530px 0 0 rgba(48, 53, 56, 1), 130px 530px 0 0 rgba(48, 53, 56, 1),
  140px 530px 0 0 rgba(48, 53, 56, 1), 150px 530px 0 0 rgba(48, 53, 56, 1),
  160px 530px 0 0 rgba(48, 53, 56, 1), 170px 530px 0 0 rgba(48, 53, 56, 1),
  180px 530px 0 0 rgba(48, 53, 56, 1), 190px 530px 0 0 rgba(48, 53, 56, 1),
  200px 530px 0 0 rgba(48, 53, 56, 1), 210px 530px 0 0 rgba(48, 53, 56, 1),
  220px 530px 0 0 rgba(48, 53, 56, 1), 230px 530px 0 0 rgba(48, 53, 56, 1),
  240px 530px 0 0 rgba(48, 53, 56, 1), 250px 530px 0 0 rgba(48, 53, 56, 1),
  260px 530px 0 0 rgba(48, 53, 56, 1), 270px 530px 0 0 rgba(48, 53, 56, 1),
  280px 530px 0 0 rgba(48, 53, 56, 1), 290px 530px 0 0 rgba(48, 53, 56, 1),
  300px 530px 0 0 rgba(48, 53, 56, 1), 310px 530px 0 0 rgba(48, 53, 56, 1),
  320px 530px 0 0 rgba(48, 53, 56, 1), 330px 530px 0 0 rgba(48, 53, 56, 1),
  340px 530px 0 0 rgba(48, 53, 56, 1), 350px 530px 0 0 rgba(48, 53, 56, 1),
  360px 530px 0 0 rgba(48, 53, 56, 1), 370px 530px 0 0 rgba(48, 53, 56, 1),
  380px 530px 0 0 rgba(48, 53, 56, 1), 390px 530px 0 0 rgba(48, 53, 56, 1),
  400px 530px 0 0 rgba(48, 53, 56, 1), 410px 530px 0 0 rgba(48, 53, 56, 1),
  420px 530px 0 0 rgba(48, 53, 56, 1), 430px 530px 0 0 rgba(48, 53, 56, 1),
  440px 530px 0 0 rgba(48, 53, 56, 1), 450px 530px 0 0 rgba(48, 53, 56, 1),
  460px 530px 0 0 rgba(48, 53, 56, 1), 470px 530px 0 0 rgba(48, 53, 56, 1),
  480px 530px 0 0 rgba(48, 53, 56, 1), 490px 530px 0 0 rgba(48, 53, 56, 1),
  500px 530px 0 0 rgba(48, 53, 56, 1), 510px 530px 0 0 rgba(48, 53, 56, 1),
  520px 530px 0 0 rgba(48, 53, 56, 1), 530px 530px 0 0 rgba(48, 53, 56, 1),
  540px 530px 0 0 rgba(48, 53, 56, 1), 550px 530px 0 0 rgba(48, 53, 56, 1),
  560px 530px 0 0 rgba(48, 53, 56, 1), 570px 530px 0 0 rgba(48, 53, 56, 1),
  580px 530px 0 0 rgba(48, 53, 56, 1), 590px 530px 0 0 rgba(48, 53, 56, 1),
  600px 530px 0 0 rgba(48, 53, 56, 1), 610px 530px 0 0 rgba(48, 53, 56, 1),
  620px 530px 0 0 rgba(48, 53, 56, 1), 630px 530px 0 0 rgba(48, 53, 56, 1),
  640px 530px 0 0 rgba(48, 53, 56, 1), 650px 530px 0 0 rgba(48, 53, 56, 1),
  660px 530px 0 0 rgba(48, 53, 56, 1), 670px 530px 0 0 rgba(48, 53, 56, 1),
  680px 530px 0 0 rgba(48, 53, 56, 1), 690px 530px 0 0 rgba(48, 53, 56, 1),
  700px 530px 0 0 rgba(48, 53, 56, 1), 710px 530px 0 0 rgba(48, 53, 56, 1),
  720px 530px 0 0 rgba(48, 53, 56, 1), 730px 530px 0 0 rgba(48, 53, 56, 1),
  740px 530px 0 0 rgba(48, 53, 56, 1), 750px 530px 0 0 rgba(48, 53, 56, 1),
  760px 530px 0 0 rgba(48, 53, 56, 1), 770px 530px 0 0 rgba(48, 53, 56, 1),
  780px 530px 0 0 rgba(48, 53, 56, 1), 790px 530px 0 0 rgba(48, 53, 56, 1),
  800px 530px 0 0 rgba(48, 53, 56, 1), 810px 530px 0 0 rgba(48, 53, 56, 1),
  820px 530px 0 0 rgba(48, 53, 56, 1), 830px 530px 0 0 rgba(48, 53, 56, 1),
  840px 530px 0 0 rgba(48, 53, 56, 1), 850px 530px 0 0 rgba(48, 53, 56, 1),
  860px 530px 0 0 rgba(48, 53, 56, 1), 870px 530px 0 0 rgba(48, 53, 56, 1),
  880px 530px 0 0 rgba(48, 53, 56, 1), 890px 530px 0 0 rgba(48, 53, 56, 1),
  900px 530px 0 0 rgba(48, 53, 56, 1), 910px 530px 0 0 rgba(48, 53, 56, 1),
  920px 530px 0 0 rgba(48, 53, 56, 1), 930px 530px 0 0 rgba(48, 53, 56, 1),
  940px 530px 0 0 rgba(48, 53, 56, 1), 950px 530px 0 0 rgba(48, 53, 56, 1),
  960px 530px 0 0 rgba(48, 53, 56, 1), 970px 530px 0 0 rgba(48, 53, 56, 1),
  980px 530px 0 0 rgba(48, 53, 56, 1), 990px 530px 0 0 rgba(48, 53, 56, 1),
  1000px 530px 0 0 rgba(48, 53, 56, 1), 10px 540px 0 0 rgba(28, 32, 34, 1),
  20px 540px 0 0 rgba(219, 222, 232, 1), 30px 540px 0 0 rgba(111, 114, 121, 1),
  40px 540px 0 0 rgba(28, 32, 34, 1), 50px 540px 0 0 rgba(48, 53, 56, 1),
  60px 540px 0 0 rgba(48, 53, 56, 1), 70px 540px 0 0 rgba(48, 53, 56, 1),
  80px 540px 0 0 rgba(48, 53, 56, 1), 90px 540px 0 0 rgba(48, 53, 56, 1),
  100px 540px 0 0 rgba(48, 53, 56, 1), 110px 540px 0 0 rgba(48, 53, 56, 1),
  120px 540px 0 0 rgba(48, 53, 56, 1), 130px 540px 0 0 rgba(48, 53, 56, 1),
  140px 540px 0 0 rgba(48, 53, 56, 1), 150px 540px 0 0 rgba(48, 53, 56, 1),
  160px 540px 0 0 rgba(48, 53, 56, 1), 170px 540px 0 0 rgba(48, 53, 56, 1),
  180px 540px 0 0 rgba(48, 53, 56, 1), 190px 540px 0 0 rgba(48, 53, 56, 1),
  200px 540px 0 0 rgba(48, 53, 56, 1), 210px 540px 0 0 rgba(48, 53, 56, 1),
  220px 540px 0 0 rgba(48, 53, 56, 1), 230px 540px 0 0 rgba(48, 53, 56, 1),
  240px 540px 0 0 rgba(48, 53, 56, 1), 250px 540px 0 0 rgba(48, 53, 56, 1),
  260px 540px 0 0 rgba(48, 53, 56, 1), 270px 540px 0 0 rgba(48, 53, 56, 1),
  280px 540px 0 0 rgba(48, 53, 56, 1), 290px 540px 0 0 rgba(48, 53, 56, 1),
  300px 540px 0 0 rgba(48, 53, 56, 1), 310px 540px 0 0 rgba(48, 53, 56, 1),
  320px 540px 0 0 rgba(48, 53, 56, 1), 330px 540px 0 0 rgba(48, 53, 56, 1),
  340px 540px 0 0 rgba(48, 53, 56, 1), 350px 540px 0 0 rgba(48, 53, 56, 1),
  360px 540px 0 0 rgba(48, 53, 56, 1), 370px 540px 0 0 rgba(48, 53, 56, 1),
  380px 540px 0 0 rgba(48, 53, 56, 1), 390px 540px 0 0 rgba(48, 53, 56, 1),
  400px 540px 0 0 rgba(48, 53, 56, 1), 410px 540px 0 0 rgba(48, 53, 56, 1),
  420px 540px 0 0 rgba(48, 53, 56, 1), 430px 540px 0 0 rgba(48, 53, 56, 1),
  440px 540px 0 0 rgba(48, 53, 56, 1), 450px 540px 0 0 rgba(48, 53, 56, 1),
  460px 540px 0 0 rgba(48, 53, 56, 1), 470px 540px 0 0 rgba(48, 53, 56, 1),
  480px 540px 0 0 rgba(48, 53, 56, 1), 490px 540px 0 0 rgba(48, 53, 56, 1),
  500px 540px 0 0 rgba(48, 53, 56, 1), 510px 540px 0 0 rgba(48, 53, 56, 1),
  520px 540px 0 0 rgba(48, 53, 56, 1), 530px 540px 0 0 rgba(48, 53, 56, 1),
  540px 540px 0 0 rgba(48, 53, 56, 1), 550px 540px 0 0 rgba(48, 53, 56, 1),
  560px 540px 0 0 rgba(48, 53, 56, 1), 570px 540px 0 0 rgba(48, 53, 56, 1),
  580px 540px 0 0 rgba(48, 53, 56, 1), 590px 540px 0 0 rgba(48, 53, 56, 1),
  600px 540px 0 0 rgba(48, 53, 56, 1), 610px 540px 0 0 rgba(48, 53, 56, 1),
  620px 540px 0 0 rgba(48, 53, 56, 1), 630px 540px 0 0 rgba(48, 53, 56, 1),
  640px 540px 0 0 rgba(48, 53, 56, 1), 650px 540px 0 0 rgba(48, 53, 56, 1),
  660px 540px 0 0 rgba(48, 53, 56, 1), 670px 540px 0 0 rgba(48, 53, 56, 1),
  680px 540px 0 0 rgba(48, 53, 56, 1), 690px 540px 0 0 rgba(48, 53, 56, 1),
  700px 540px 0 0 rgba(48, 53, 56, 1), 710px 540px 0 0 rgba(48, 53, 56, 1),
  720px 540px 0 0 rgba(48, 53, 56, 1), 730px 540px 0 0 rgba(48, 53, 56, 1),
  740px 540px 0 0 rgba(48, 53, 56, 1), 750px 540px 0 0 rgba(48, 53, 56, 1),
  760px 540px 0 0 rgba(48, 53, 56, 1), 770px 540px 0 0 rgba(48, 53, 56, 1),
  780px 540px 0 0 rgba(48, 53, 56, 1), 790px 540px 0 0 rgba(48, 53, 56, 1),
  800px 540px 0 0 rgba(48, 53, 56, 1), 810px 540px 0 0 rgba(48, 53, 56, 1),
  820px 540px 0 0 rgba(48, 53, 56, 1), 830px 540px 0 0 rgba(48, 53, 56, 1),
  840px 540px 0 0 rgba(48, 53, 56, 1), 850px 540px 0 0 rgba(48, 53, 56, 1),
  860px 540px 0 0 rgba(48, 53, 56, 1), 870px 540px 0 0 rgba(48, 53, 56, 1),
  880px 540px 0 0 rgba(48, 53, 56, 1), 890px 540px 0 0 rgba(48, 53, 56, 1),
  900px 540px 0 0 rgba(48, 53, 56, 1), 910px 540px 0 0 rgba(48, 53, 56, 1),
  920px 540px 0 0 rgba(48, 53, 56, 1), 930px 540px 0 0 rgba(48, 53, 56, 1),
  940px 540px 0 0 rgba(48, 53, 56, 1), 950px 540px 0 0 rgba(48, 53, 56, 1),
  960px 540px 0 0 rgba(48, 53, 56, 1), 970px 540px 0 0 rgba(48, 53, 56, 1),
  980px 540px 0 0 rgba(48, 53, 56, 1), 990px 540px 0 0 rgba(48, 53, 56, 1),
  1000px 540px 0 0 rgba(48, 53, 56, 1), 10px 550px 0 0 rgba(28, 32, 34, 1),
  20px 550px 0 0 rgba(219, 222, 232, 1), 30px 550px 0 0 rgba(111, 114, 121, 1),
  40px 550px 0 0 rgba(28, 32, 34, 1), 50px 550px 0 0 rgba(48, 53, 56, 1),
  60px 550px 0 0 rgba(48, 53, 56, 1), 70px 550px 0 0 rgba(48, 53, 56, 1),
  80px 550px 0 0 rgba(48, 53, 56, 1), 90px 550px 0 0 rgba(48, 53, 56, 1),
  100px 550px 0 0 rgba(48, 53, 56, 1), 110px 550px 0 0 rgba(48, 53, 56, 1),
  120px 550px 0 0 rgba(48, 53, 56, 1), 130px 550px 0 0 rgba(48, 53, 56, 1),
  140px 550px 0 0 rgba(48, 53, 56, 1), 150px 550px 0 0 rgba(48, 53, 56, 1),
  160px 550px 0 0 rgba(48, 53, 56, 1), 170px 550px 0 0 rgba(48, 53, 56, 1),
  180px 550px 0 0 rgba(48, 53, 56, 1), 190px 550px 0 0 rgba(48, 53, 56, 1),
  200px 550px 0 0 rgba(48, 53, 56, 1), 210px 550px 0 0 rgba(48, 53, 56, 1),
  220px 550px 0 0 rgba(48, 53, 56, 1), 230px 550px 0 0 rgba(48, 53, 56, 1),
  240px 550px 0 0 rgba(48, 53, 56, 1), 250px 550px 0 0 rgba(48, 53, 56, 1),
  260px 550px 0 0 rgba(48, 53, 56, 1), 270px 550px 0 0 rgba(48, 53, 56, 1),
  280px 550px 0 0 rgba(48, 53, 56, 1), 290px 550px 0 0 rgba(48, 53, 56, 1),
  300px 550px 0 0 rgba(48, 53, 56, 1), 310px 550px 0 0 rgba(48, 53, 56, 1),
  320px 550px 0 0 rgba(48, 53, 56, 1), 330px 550px 0 0 rgba(48, 53, 56, 1),
  340px 550px 0 0 rgba(48, 53, 56, 1), 350px 550px 0 0 rgba(48, 53, 56, 1),
  360px 550px 0 0 rgba(48, 53, 56, 1), 370px 550px 0 0 rgba(48, 53, 56, 1),
  380px 550px 0 0 rgba(48, 53, 56, 1), 390px 550px 0 0 rgba(48, 53, 56, 1),
  400px 550px 0 0 rgba(48, 53, 56, 1), 410px 550px 0 0 rgba(48, 53, 56, 1),
  420px 550px 0 0 rgba(48, 53, 56, 1), 430px 550px 0 0 rgba(48, 53, 56, 1),
  440px 550px 0 0 rgba(48, 53, 56, 1), 450px 550px 0 0 rgba(48, 53, 56, 1),
  460px 550px 0 0 rgba(48, 53, 56, 1), 470px 550px 0 0 rgba(48, 53, 56, 1),
  480px 550px 0 0 rgba(48, 53, 56, 1), 490px 550px 0 0 rgba(48, 53, 56, 1),
  500px 550px 0 0 rgba(48, 53, 56, 1), 510px 550px 0 0 rgba(48, 53, 56, 1),
  520px 550px 0 0 rgba(48, 53, 56, 1), 530px 550px 0 0 rgba(48, 53, 56, 1),
  540px 550px 0 0 rgba(48, 53, 56, 1), 550px 550px 0 0 rgba(48, 53, 56, 1),
  560px 550px 0 0 rgba(48, 53, 56, 1), 570px 550px 0 0 rgba(48, 53, 56, 1),
  580px 550px 0 0 rgba(48, 53, 56, 1), 590px 550px 0 0 rgba(48, 53, 56, 1),
  600px 550px 0 0 rgba(48, 53, 56, 1), 610px 550px 0 0 rgba(48, 53, 56, 1),
  620px 550px 0 0 rgba(48, 53, 56, 1), 630px 550px 0 0 rgba(48, 53, 56, 1),
  640px 550px 0 0 rgba(48, 53, 56, 1), 650px 550px 0 0 rgba(48, 53, 56, 1),
  660px 550px 0 0 rgba(48, 53, 56, 1), 670px 550px 0 0 rgba(48, 53, 56, 1),
  680px 550px 0 0 rgba(48, 53, 56, 1), 690px 550px 0 0 rgba(48, 53, 56, 1),
  700px 550px 0 0 rgba(48, 53, 56, 1), 710px 550px 0 0 rgba(48, 53, 56, 1),
  720px 550px 0 0 rgba(48, 53, 56, 1), 730px 550px 0 0 rgba(48, 53, 56, 1),
  740px 550px 0 0 rgba(48, 53, 56, 1), 750px 550px 0 0 rgba(48, 53, 56, 1),
  760px 550px 0 0 rgba(48, 53, 56, 1), 770px 550px 0 0 rgba(48, 53, 56, 1),
  780px 550px 0 0 rgba(48, 53, 56, 1), 790px 550px 0 0 rgba(48, 53, 56, 1),
  800px 550px 0 0 rgba(48, 53, 56, 1), 810px 550px 0 0 rgba(48, 53, 56, 1),
  820px 550px 0 0 rgba(48, 53, 56, 1), 830px 550px 0 0 rgba(48, 53, 56, 1),
  840px 550px 0 0 rgba(48, 53, 56, 1), 850px 550px 0 0 rgba(48, 53, 56, 1),
  860px 550px 0 0 rgba(48, 53, 56, 1), 870px 550px 0 0 rgba(48, 53, 56, 1),
  880px 550px 0 0 rgba(48, 53, 56, 1), 890px 550px 0 0 rgba(48, 53, 56, 1),
  900px 550px 0 0 rgba(48, 53, 56, 1), 910px 550px 0 0 rgba(48, 53, 56, 1),
  920px 550px 0 0 rgba(48, 53, 56, 1), 930px 550px 0 0 rgba(48, 53, 56, 1),
  940px 550px 0 0 rgba(48, 53, 56, 1), 950px 550px 0 0 rgba(48, 53, 56, 1),
  960px 550px 0 0 rgba(48, 53, 56, 1), 970px 550px 0 0 rgba(48, 53, 56, 1),
  980px 550px 0 0 rgba(48, 53, 56, 1), 990px 550px 0 0 rgba(48, 53, 56, 1),
  1000px 550px 0 0 rgba(48, 53, 56, 1), 10px 560px 0 0 rgba(28, 32, 34, 1),
  20px 560px 0 0 rgba(219, 222, 232, 1), 30px 560px 0 0 rgba(111, 114, 121, 1),
  40px 560px 0 0 rgba(28, 32, 34, 1), 50px 560px 0 0 rgba(48, 53, 56, 1),
  60px 560px 0 0 rgba(48, 53, 56, 1), 70px 560px 0 0 rgba(48, 53, 56, 1),
  80px 560px 0 0 rgba(48, 53, 56, 1), 90px 560px 0 0 rgba(48, 53, 56, 1),
  100px 560px 0 0 rgba(48, 53, 56, 1), 110px 560px 0 0 rgba(48, 53, 56, 1),
  120px 560px 0 0 rgba(48, 53, 56, 1), 130px 560px 0 0 rgba(48, 53, 56, 1),
  140px 560px 0 0 rgba(48, 53, 56, 1), 150px 560px 0 0 rgba(48, 53, 56, 1),
  160px 560px 0 0 rgba(48, 53, 56, 1), 170px 560px 0 0 rgba(48, 53, 56, 1),
  180px 560px 0 0 rgba(48, 53, 56, 1), 190px 560px 0 0 rgba(48, 53, 56, 1),
  200px 560px 0 0 rgba(48, 53, 56, 1), 210px 560px 0 0 rgba(48, 53, 56, 1),
  220px 560px 0 0 rgba(48, 53, 56, 1), 230px 560px 0 0 rgba(48, 53, 56, 1),
  240px 560px 0 0 rgba(48, 53, 56, 1), 250px 560px 0 0 rgba(48, 53, 56, 1),
  260px 560px 0 0 rgba(48, 53, 56, 1), 270px 560px 0 0 rgba(48, 53, 56, 1),
  280px 560px 0 0 rgba(48, 53, 56, 1), 290px 560px 0 0 rgba(48, 53, 56, 1),
  300px 560px 0 0 rgba(48, 53, 56, 1), 310px 560px 0 0 rgba(48, 53, 56, 1),
  320px 560px 0 0 rgba(48, 53, 56, 1), 330px 560px 0 0 rgba(48, 53, 56, 1),
  340px 560px 0 0 rgba(48, 53, 56, 1), 350px 560px 0 0 rgba(48, 53, 56, 1),
  360px 560px 0 0 rgba(48, 53, 56, 1), 370px 560px 0 0 rgba(48, 53, 56, 1),
  380px 560px 0 0 rgba(48, 53, 56, 1), 390px 560px 0 0 rgba(48, 53, 56, 1),
  400px 560px 0 0 rgba(48, 53, 56, 1), 410px 560px 0 0 rgba(48, 53, 56, 1),
  420px 560px 0 0 rgba(48, 53, 56, 1), 430px 560px 0 0 rgba(48, 53, 56, 1),
  440px 560px 0 0 rgba(48, 53, 56, 1), 450px 560px 0 0 rgba(48, 53, 56, 1),
  460px 560px 0 0 rgba(48, 53, 56, 1), 470px 560px 0 0 rgba(48, 53, 56, 1),
  480px 560px 0 0 rgba(48, 53, 56, 1), 490px 560px 0 0 rgba(48, 53, 56, 1),
  500px 560px 0 0 rgba(48, 53, 56, 1), 510px 560px 0 0 rgba(48, 53, 56, 1),
  520px 560px 0 0 rgba(48, 53, 56, 1), 530px 560px 0 0 rgba(48, 53, 56, 1),
  540px 560px 0 0 rgba(48, 53, 56, 1), 550px 560px 0 0 rgba(48, 53, 56, 1),
  560px 560px 0 0 rgba(48, 53, 56, 1), 570px 560px 0 0 rgba(48, 53, 56, 1),
  580px 560px 0 0 rgba(48, 53, 56, 1), 590px 560px 0 0 rgba(48, 53, 56, 1),
  600px 560px 0 0 rgba(48, 53, 56, 1), 610px 560px 0 0 rgba(48, 53, 56, 1),
  620px 560px 0 0 rgba(48, 53, 56, 1), 630px 560px 0 0 rgba(48, 53, 56, 1),
  640px 560px 0 0 rgba(48, 53, 56, 1), 650px 560px 0 0 rgba(48, 53, 56, 1),
  660px 560px 0 0 rgba(48, 53, 56, 1), 670px 560px 0 0 rgba(48, 53, 56, 1),
  680px 560px 0 0 rgba(48, 53, 56, 1), 690px 560px 0 0 rgba(48, 53, 56, 1),
  700px 560px 0 0 rgba(48, 53, 56, 1), 710px 560px 0 0 rgba(48, 53, 56, 1),
  720px 560px 0 0 rgba(48, 53, 56, 1), 730px 560px 0 0 rgba(48, 53, 56, 1),
  740px 560px 0 0 rgba(48, 53, 56, 1), 750px 560px 0 0 rgba(48, 53, 56, 1),
  760px 560px 0 0 rgba(48, 53, 56, 1), 770px 560px 0 0 rgba(48, 53, 56, 1),
  780px 560px 0 0 rgba(48, 53, 56, 1), 790px 560px 0 0 rgba(48, 53, 56, 1),
  800px 560px 0 0 rgba(48, 53, 56, 1), 810px 560px 0 0 rgba(48, 53, 56, 1),
  820px 560px 0 0 rgba(48, 53, 56, 1), 830px 560px 0 0 rgba(48, 53, 56, 1),
  840px 560px 0 0 rgba(48, 53, 56, 1), 850px 560px 0 0 rgba(48, 53, 56, 1),
  860px 560px 0 0 rgba(48, 53, 56, 1), 870px 560px 0 0 rgba(48, 53, 56, 1),
  880px 560px 0 0 rgba(48, 53, 56, 1), 890px 560px 0 0 rgba(48, 53, 56, 1),
  900px 560px 0 0 rgba(48, 53, 56, 1), 910px 560px 0 0 rgba(48, 53, 56, 1),
  920px 560px 0 0 rgba(48, 53, 56, 1), 930px 560px 0 0 rgba(48, 53, 56, 1),
  940px 560px 0 0 rgba(48, 53, 56, 1), 950px 560px 0 0 rgba(48, 53, 56, 1),
  960px 560px 0 0 rgba(48, 53, 56, 1), 970px 560px 0 0 rgba(48, 53, 56, 1),
  980px 560px 0 0 rgba(48, 53, 56, 1), 990px 560px 0 0 rgba(48, 53, 56, 1),
  1000px 560px 0 0 rgba(48, 53, 56, 1), 10px 570px 0 0 rgba(28, 32, 34, 1),
  20px 570px 0 0 rgba(219, 222, 232, 1), 30px 570px 0 0 rgba(111, 114, 121, 1),
  40px 570px 0 0 rgba(28, 32, 34, 1), 50px 570px 0 0 rgba(48, 53, 56, 1),
  60px 570px 0 0 rgba(48, 53, 56, 1), 70px 570px 0 0 rgba(48, 53, 56, 1),
  80px 570px 0 0 rgba(48, 53, 56, 1), 90px 570px 0 0 rgba(48, 53, 56, 1),
  100px 570px 0 0 rgba(48, 53, 56, 1), 110px 570px 0 0 rgba(48, 53, 56, 1),
  120px 570px 0 0 rgba(48, 53, 56, 1), 130px 570px 0 0 rgba(48, 53, 56, 1),
  140px 570px 0 0 rgba(48, 53, 56, 1), 150px 570px 0 0 rgba(48, 53, 56, 1),
  160px 570px 0 0 rgba(48, 53, 56, 1), 170px 570px 0 0 rgba(48, 53, 56, 1),
  180px 570px 0 0 rgba(48, 53, 56, 1), 190px 570px 0 0 rgba(48, 53, 56, 1),
  200px 570px 0 0 rgba(48, 53, 56, 1), 210px 570px 0 0 rgba(48, 53, 56, 1),
  220px 570px 0 0 rgba(48, 53, 56, 1), 230px 570px 0 0 rgba(48, 53, 56, 1),
  240px 570px 0 0 rgba(48, 53, 56, 1), 250px 570px 0 0 rgba(48, 53, 56, 1),
  260px 570px 0 0 rgba(48, 53, 56, 1), 270px 570px 0 0 rgba(48, 53, 56, 1),
  280px 570px 0 0 rgba(48, 53, 56, 1), 290px 570px 0 0 rgba(48, 53, 56, 1),
  300px 570px 0 0 rgba(48, 53, 56, 1), 310px 570px 0 0 rgba(48, 53, 56, 1),
  320px 570px 0 0 rgba(48, 53, 56, 1), 330px 570px 0 0 rgba(48, 53, 56, 1),
  340px 570px 0 0 rgba(48, 53, 56, 1), 350px 570px 0 0 rgba(48, 53, 56, 1),
  360px 570px 0 0 rgba(48, 53, 56, 1), 370px 570px 0 0 rgba(48, 53, 56, 1),
  380px 570px 0 0 rgba(48, 53, 56, 1), 390px 570px 0 0 rgba(48, 53, 56, 1),
  400px 570px 0 0 rgba(48, 53, 56, 1), 410px 570px 0 0 rgba(48, 53, 56, 1),
  420px 570px 0 0 rgba(48, 53, 56, 1), 430px 570px 0 0 rgba(48, 53, 56, 1),
  440px 570px 0 0 rgba(48, 53, 56, 1), 450px 570px 0 0 rgba(48, 53, 56, 1),
  460px 570px 0 0 rgba(48, 53, 56, 1), 470px 570px 0 0 rgba(48, 53, 56, 1),
  480px 570px 0 0 rgba(48, 53, 56, 1), 490px 570px 0 0 rgba(48, 53, 56, 1),
  500px 570px 0 0 rgba(48, 53, 56, 1), 510px 570px 0 0 rgba(48, 53, 56, 1),
  520px 570px 0 0 rgba(48, 53, 56, 1), 530px 570px 0 0 rgba(48, 53, 56, 1),
  540px 570px 0 0 rgba(48, 53, 56, 1), 550px 570px 0 0 rgba(48, 53, 56, 1),
  560px 570px 0 0 rgba(48, 53, 56, 1), 570px 570px 0 0 rgba(48, 53, 56, 1),
  580px 570px 0 0 rgba(48, 53, 56, 1), 590px 570px 0 0 rgba(48, 53, 56, 1),
  600px 570px 0 0 rgba(48, 53, 56, 1), 610px 570px 0 0 rgba(48, 53, 56, 1),
  620px 570px 0 0 rgba(48, 53, 56, 1), 630px 570px 0 0 rgba(48, 53, 56, 1),
  640px 570px 0 0 rgba(48, 53, 56, 1), 650px 570px 0 0 rgba(48, 53, 56, 1),
  660px 570px 0 0 rgba(48, 53, 56, 1), 670px 570px 0 0 rgba(48, 53, 56, 1),
  680px 570px 0 0 rgba(48, 53, 56, 1), 690px 570px 0 0 rgba(48, 53, 56, 1),
  700px 570px 0 0 rgba(48, 53, 56, 1), 710px 570px 0 0 rgba(48, 53, 56, 1),
  720px 570px 0 0 rgba(48, 53, 56, 1), 730px 570px 0 0 rgba(48, 53, 56, 1),
  740px 570px 0 0 rgba(48, 53, 56, 1), 750px 570px 0 0 rgba(48, 53, 56, 1),
  760px 570px 0 0 rgba(48, 53, 56, 1), 770px 570px 0 0 rgba(48, 53, 56, 1),
  780px 570px 0 0 rgba(48, 53, 56, 1), 790px 570px 0 0 rgba(48, 53, 56, 1),
  800px 570px 0 0 rgba(48, 53, 56, 1), 810px 570px 0 0 rgba(48, 53, 56, 1),
  820px 570px 0 0 rgba(48, 53, 56, 1), 830px 570px 0 0 rgba(48, 53, 56, 1),
  840px 570px 0 0 rgba(48, 53, 56, 1), 850px 570px 0 0 rgba(48, 53, 56, 1),
  860px 570px 0 0 rgba(48, 53, 56, 1), 870px 570px 0 0 rgba(48, 53, 56, 1),
  880px 570px 0 0 rgba(48, 53, 56, 1), 890px 570px 0 0 rgba(48, 53, 56, 1),
  900px 570px 0 0 rgba(48, 53, 56, 1), 910px 570px 0 0 rgba(48, 53, 56, 1),
  920px 570px 0 0 rgba(48, 53, 56, 1), 930px 570px 0 0 rgba(48, 53, 56, 1),
  940px 570px 0 0 rgba(48, 53, 56, 1), 950px 570px 0 0 rgba(48, 53, 56, 1),
  960px 570px 0 0 rgba(48, 53, 56, 1), 970px 570px 0 0 rgba(48, 53, 56, 1),
  980px 570px 0 0 rgba(48, 53, 56, 1), 990px 570px 0 0 rgba(48, 53, 56, 1),
  1000px 570px 0 0 rgba(48, 53, 56, 1), 10px 580px 0 0 rgba(28, 32, 34, 1),
  20px 580px 0 0 rgba(219, 222, 232, 1), 30px 580px 0 0 rgba(111, 114, 121, 1),
  40px 580px 0 0 rgba(28, 32, 34, 1), 50px 580px 0 0 rgba(48, 53, 56, 1),
  60px 580px 0 0 rgba(48, 53, 56, 1), 70px 580px 0 0 rgba(48, 53, 56, 1),
  80px 580px 0 0 rgba(48, 53, 56, 1), 90px 580px 0 0 rgba(48, 53, 56, 1),
  100px 580px 0 0 rgba(48, 53, 56, 1), 110px 580px 0 0 rgba(48, 53, 56, 1),
  120px 580px 0 0 rgba(48, 53, 56, 1), 130px 580px 0 0 rgba(48, 53, 56, 1),
  140px 580px 0 0 rgba(48, 53, 56, 1), 150px 580px 0 0 rgba(48, 53, 56, 1),
  160px 580px 0 0 rgba(48, 53, 56, 1), 170px 580px 0 0 rgba(48, 53, 56, 1),
  180px 580px 0 0 rgba(48, 53, 56, 1), 190px 580px 0 0 rgba(48, 53, 56, 1),
  200px 580px 0 0 rgba(48, 53, 56, 1), 210px 580px 0 0 rgba(48, 53, 56, 1),
  220px 580px 0 0 rgba(48, 53, 56, 1), 230px 580px 0 0 rgba(48, 53, 56, 1),
  240px 580px 0 0 rgba(48, 53, 56, 1), 250px 580px 0 0 rgba(48, 53, 56, 1),
  260px 580px 0 0 rgba(48, 53, 56, 1), 270px 580px 0 0 rgba(48, 53, 56, 1),
  280px 580px 0 0 rgba(48, 53, 56, 1), 290px 580px 0 0 rgba(48, 53, 56, 1),
  300px 580px 0 0 rgba(48, 53, 56, 1), 310px 580px 0 0 rgba(48, 53, 56, 1),
  320px 580px 0 0 rgba(48, 53, 56, 1), 330px 580px 0 0 rgba(48, 53, 56, 1),
  340px 580px 0 0 rgba(48, 53, 56, 1), 350px 580px 0 0 rgba(48, 53, 56, 1),
  360px 580px 0 0 rgba(48, 53, 56, 1), 370px 580px 0 0 rgba(48, 53, 56, 1),
  380px 580px 0 0 rgba(48, 53, 56, 1), 390px 580px 0 0 rgba(48, 53, 56, 1),
  400px 580px 0 0 rgba(48, 53, 56, 1), 410px 580px 0 0 rgba(48, 53, 56, 1),
  420px 580px 0 0 rgba(48, 53, 56, 1), 430px 580px 0 0 rgba(48, 53, 56, 1),
  440px 580px 0 0 rgba(48, 53, 56, 1), 450px 580px 0 0 rgba(48, 53, 56, 1),
  460px 580px 0 0 rgba(48, 53, 56, 1), 470px 580px 0 0 rgba(48, 53, 56, 1),
  480px 580px 0 0 rgba(48, 53, 56, 1), 490px 580px 0 0 rgba(48, 53, 56, 1),
  500px 580px 0 0 rgba(48, 53, 56, 1), 510px 580px 0 0 rgba(48, 53, 56, 1),
  520px 580px 0 0 rgba(48, 53, 56, 1), 530px 580px 0 0 rgba(48, 53, 56, 1),
  540px 580px 0 0 rgba(48, 53, 56, 1), 550px 580px 0 0 rgba(48, 53, 56, 1),
  560px 580px 0 0 rgba(48, 53, 56, 1), 570px 580px 0 0 rgba(48, 53, 56, 1),
  580px 580px 0 0 rgba(48, 53, 56, 1), 590px 580px 0 0 rgba(48, 53, 56, 1),
  600px 580px 0 0 rgba(48, 53, 56, 1), 610px 580px 0 0 rgba(48, 53, 56, 1),
  620px 580px 0 0 rgba(48, 53, 56, 1), 630px 580px 0 0 rgba(48, 53, 56, 1),
  640px 580px 0 0 rgba(48, 53, 56, 1), 650px 580px 0 0 rgba(48, 53, 56, 1),
  660px 580px 0 0 rgba(48, 53, 56, 1), 670px 580px 0 0 rgba(48, 53, 56, 1),
  680px 580px 0 0 rgba(48, 53, 56, 1), 690px 580px 0 0 rgba(48, 53, 56, 1),
  700px 580px 0 0 rgba(48, 53, 56, 1), 710px 580px 0 0 rgba(48, 53, 56, 1),
  720px 580px 0 0 rgba(48, 53, 56, 1), 730px 580px 0 0 rgba(48, 53, 56, 1),
  740px 580px 0 0 rgba(48, 53, 56, 1), 750px 580px 0 0 rgba(48, 53, 56, 1),
  760px 580px 0 0 rgba(48, 53, 56, 1), 770px 580px 0 0 rgba(48, 53, 56, 1),
  780px 580px 0 0 rgba(48, 53, 56, 1), 790px 580px 0 0 rgba(48, 53, 56, 1),
  800px 580px 0 0 rgba(48, 53, 56, 1), 810px 580px 0 0 rgba(48, 53, 56, 1),
  820px 580px 0 0 rgba(48, 53, 56, 1), 830px 580px 0 0 rgba(48, 53, 56, 1),
  840px 580px 0 0 rgba(48, 53, 56, 1), 850px 580px 0 0 rgba(48, 53, 56, 1),
  860px 580px 0 0 rgba(48, 53, 56, 1), 870px 580px 0 0 rgba(48, 53, 56, 1),
  880px 580px 0 0 rgba(48, 53, 56, 1), 890px 580px 0 0 rgba(48, 53, 56, 1),
  900px 580px 0 0 rgba(48, 53, 56, 1), 910px 580px 0 0 rgba(48, 53, 56, 1),
  920px 580px 0 0 rgba(48, 53, 56, 1), 930px 580px 0 0 rgba(48, 53, 56, 1),
  940px 580px 0 0 rgba(48, 53, 56, 1), 950px 580px 0 0 rgba(48, 53, 56, 1),
  960px 580px 0 0 rgba(48, 53, 56, 1), 970px 580px 0 0 rgba(48, 53, 56, 1),
  980px 580px 0 0 rgba(48, 53, 56, 1), 990px 580px 0 0 rgba(48, 53, 56, 1),
  1000px 580px 0 0 rgba(48, 53, 56, 1), 10px 590px 0 0 rgba(28, 32, 34, 1),
  20px 590px 0 0 rgba(219, 222, 232, 1), 30px 590px 0 0 rgba(111, 114, 121, 1),
  40px 590px 0 0 rgba(28, 32, 34, 1), 50px 590px 0 0 rgba(48, 53, 56, 1),
  60px 590px 0 0 rgba(48, 53, 56, 1), 70px 590px 0 0 rgba(48, 53, 56, 1),
  80px 590px 0 0 rgba(48, 53, 56, 1), 90px 590px 0 0 rgba(48, 53, 56, 1),
  100px 590px 0 0 rgba(48, 53, 56, 1), 110px 590px 0 0 rgba(48, 53, 56, 1),
  120px 590px 0 0 rgba(48, 53, 56, 1), 130px 590px 0 0 rgba(48, 53, 56, 1),
  140px 590px 0 0 rgba(48, 53, 56, 1), 150px 590px 0 0 rgba(48, 53, 56, 1),
  160px 590px 0 0 rgba(48, 53, 56, 1), 170px 590px 0 0 rgba(48, 53, 56, 1),
  180px 590px 0 0 rgba(48, 53, 56, 1), 190px 590px 0 0 rgba(48, 53, 56, 1),
  200px 590px 0 0 rgba(48, 53, 56, 1), 210px 590px 0 0 rgba(48, 53, 56, 1),
  220px 590px 0 0 rgba(48, 53, 56, 1), 230px 590px 0 0 rgba(48, 53, 56, 1),
  240px 590px 0 0 rgba(48, 53, 56, 1), 250px 590px 0 0 rgba(48, 53, 56, 1),
  260px 590px 0 0 rgba(48, 53, 56, 1), 270px 590px 0 0 rgba(48, 53, 56, 1),
  280px 590px 0 0 rgba(48, 53, 56, 1), 290px 590px 0 0 rgba(48, 53, 56, 1),
  300px 590px 0 0 rgba(48, 53, 56, 1), 310px 590px 0 0 rgba(48, 53, 56, 1),
  320px 590px 0 0 rgba(48, 53, 56, 1), 330px 590px 0 0 rgba(48, 53, 56, 1),
  340px 590px 0 0 rgba(48, 53, 56, 1), 350px 590px 0 0 rgba(48, 53, 56, 1),
  360px 590px 0 0 rgba(48, 53, 56, 1), 370px 590px 0 0 rgba(48, 53, 56, 1),
  380px 590px 0 0 rgba(48, 53, 56, 1), 390px 590px 0 0 rgba(48, 53, 56, 1),
  400px 590px 0 0 rgba(48, 53, 56, 1), 410px 590px 0 0 rgba(48, 53, 56, 1),
  420px 590px 0 0 rgba(48, 53, 56, 1), 430px 590px 0 0 rgba(48, 53, 56, 1),
  440px 590px 0 0 rgba(48, 53, 56, 1), 450px 590px 0 0 rgba(48, 53, 56, 1),
  460px 590px 0 0 rgba(48, 53, 56, 1), 470px 590px 0 0 rgba(48, 53, 56, 1),
  480px 590px 0 0 rgba(48, 53, 56, 1), 490px 590px 0 0 rgba(48, 53, 56, 1),
  500px 590px 0 0 rgba(48, 53, 56, 1), 510px 590px 0 0 rgba(48, 53, 56, 1),
  520px 590px 0 0 rgba(48, 53, 56, 1), 530px 590px 0 0 rgba(48, 53, 56, 1),
  540px 590px 0 0 rgba(48, 53, 56, 1), 550px 590px 0 0 rgba(48, 53, 56, 1),
  560px 590px 0 0 rgba(48, 53, 56, 1), 570px 590px 0 0 rgba(48, 53, 56, 1),
  580px 590px 0 0 rgba(48, 53, 56, 1), 590px 590px 0 0 rgba(48, 53, 56, 1),
  600px 590px 0 0 rgba(48, 53, 56, 1), 610px 590px 0 0 rgba(48, 53, 56, 1),
  620px 590px 0 0 rgba(48, 53, 56, 1), 630px 590px 0 0 rgba(48, 53, 56, 1),
  640px 590px 0 0 rgba(48, 53, 56, 1), 650px 590px 0 0 rgba(48, 53, 56, 1),
  660px 590px 0 0 rgba(48, 53, 56, 1), 670px 590px 0 0 rgba(48, 53, 56, 1),
  680px 590px 0 0 rgba(48, 53, 56, 1), 690px 590px 0 0 rgba(48, 53, 56, 1),
  700px 590px 0 0 rgba(48, 53, 56, 1), 710px 590px 0 0 rgba(48, 53, 56, 1),
  720px 590px 0 0 rgba(48, 53, 56, 1), 730px 590px 0 0 rgba(48, 53, 56, 1),
  740px 590px 0 0 rgba(48, 53, 56, 1), 750px 590px 0 0 rgba(48, 53, 56, 1),
  760px 590px 0 0 rgba(48, 53, 56, 1), 770px 590px 0 0 rgba(48, 53, 56, 1),
  780px 590px 0 0 rgba(48, 53, 56, 1), 790px 590px 0 0 rgba(48, 53, 56, 1),
  800px 590px 0 0 rgba(48, 53, 56, 1), 810px 590px 0 0 rgba(48, 53, 56, 1),
  820px 590px 0 0 rgba(48, 53, 56, 1), 830px 590px 0 0 rgba(48, 53, 56, 1),
  840px 590px 0 0 rgba(48, 53, 56, 1), 850px 590px 0 0 rgba(48, 53, 56, 1),
  860px 590px 0 0 rgba(48, 53, 56, 1), 870px 590px 0 0 rgba(48, 53, 56, 1),
  880px 590px 0 0 rgba(48, 53, 56, 1), 890px 590px 0 0 rgba(48, 53, 56, 1),
  900px 590px 0 0 rgba(48, 53, 56, 1), 910px 590px 0 0 rgba(48, 53, 56, 1),
  920px 590px 0 0 rgba(48, 53, 56, 1), 930px 590px 0 0 rgba(48, 53, 56, 1),
  940px 590px 0 0 rgba(48, 53, 56, 1), 950px 590px 0 0 rgba(48, 53, 56, 1),
  960px 590px 0 0 rgba(48, 53, 56, 1), 970px 590px 0 0 rgba(48, 53, 56, 1),
  980px 590px 0 0 rgba(48, 53, 56, 1), 990px 590px 0 0 rgba(48, 53, 56, 1),
  1000px 590px 0 0 rgba(48, 53, 56, 1), 10px 600px 0 0 rgba(28, 32, 34, 1),
  20px 600px 0 0 rgba(219, 222, 232, 1), 30px 600px 0 0 rgba(111, 114, 121, 1),
  40px 600px 0 0 rgba(28, 32, 34, 1), 50px 600px 0 0 rgba(48, 53, 56, 1),
  60px 600px 0 0 rgba(48, 53, 56, 1), 70px 600px 0 0 rgba(48, 53, 56, 1),
  80px 600px 0 0 rgba(48, 53, 56, 1), 90px 600px 0 0 rgba(48, 53, 56, 1),
  100px 600px 0 0 rgba(48, 53, 56, 1), 110px 600px 0 0 rgba(48, 53, 56, 1),
  120px 600px 0 0 rgba(48, 53, 56, 1), 130px 600px 0 0 rgba(48, 53, 56, 1),
  140px 600px 0 0 rgba(48, 53, 56, 1), 150px 600px 0 0 rgba(48, 53, 56, 1),
  160px 600px 0 0 rgba(48, 53, 56, 1), 170px 600px 0 0 rgba(48, 53, 56, 1),
  180px 600px 0 0 rgba(48, 53, 56, 1), 190px 600px 0 0 rgba(48, 53, 56, 1),
  200px 600px 0 0 rgba(48, 53, 56, 1), 210px 600px 0 0 rgba(48, 53, 56, 1),
  220px 600px 0 0 rgba(48, 53, 56, 1), 230px 600px 0 0 rgba(48, 53, 56, 1),
  240px 600px 0 0 rgba(48, 53, 56, 1), 250px 600px 0 0 rgba(48, 53, 56, 1),
  260px 600px 0 0 rgba(48, 53, 56, 1), 270px 600px 0 0 rgba(48, 53, 56, 1),
  280px 600px 0 0 rgba(48, 53, 56, 1), 290px 600px 0 0 rgba(48, 53, 56, 1),
  300px 600px 0 0 rgba(48, 53, 56, 1), 310px 600px 0 0 rgba(48, 53, 56, 1),
  320px 600px 0 0 rgba(48, 53, 56, 1), 330px 600px 0 0 rgba(48, 53, 56, 1),
  340px 600px 0 0 rgba(48, 53, 56, 1), 350px 600px 0 0 rgba(48, 53, 56, 1),
  360px 600px 0 0 rgba(48, 53, 56, 1), 370px 600px 0 0 rgba(48, 53, 56, 1),
  380px 600px 0 0 rgba(48, 53, 56, 1), 390px 600px 0 0 rgba(48, 53, 56, 1),
  400px 600px 0 0 rgba(48, 53, 56, 1), 410px 600px 0 0 rgba(48, 53, 56, 1),
  420px 600px 0 0 rgba(48, 53, 56, 1), 430px 600px 0 0 rgba(48, 53, 56, 1),
  440px 600px 0 0 rgba(48, 53, 56, 1), 450px 600px 0 0 rgba(48, 53, 56, 1),
  460px 600px 0 0 rgba(48, 53, 56, 1), 470px 600px 0 0 rgba(48, 53, 56, 1),
  480px 600px 0 0 rgba(48, 53, 56, 1), 490px 600px 0 0 rgba(48, 53, 56, 1),
  500px 600px 0 0 rgba(48, 53, 56, 1), 510px 600px 0 0 rgba(48, 53, 56, 1),
  520px 600px 0 0 rgba(48, 53, 56, 1), 530px 600px 0 0 rgba(48, 53, 56, 1),
  540px 600px 0 0 rgba(48, 53, 56, 1), 550px 600px 0 0 rgba(48, 53, 56, 1),
  560px 600px 0 0 rgba(48, 53, 56, 1), 570px 600px 0 0 rgba(48, 53, 56, 1),
  580px 600px 0 0 rgba(48, 53, 56, 1), 590px 600px 0 0 rgba(48, 53, 56, 1),
  600px 600px 0 0 rgba(48, 53, 56, 1), 610px 600px 0 0 rgba(48, 53, 56, 1),
  620px 600px 0 0 rgba(48, 53, 56, 1), 630px 600px 0 0 rgba(48, 53, 56, 1),
  640px 600px 0 0 rgba(48, 53, 56, 1), 650px 600px 0 0 rgba(48, 53, 56, 1),
  660px 600px 0 0 rgba(48, 53, 56, 1), 670px 600px 0 0 rgba(48, 53, 56, 1),
  680px 600px 0 0 rgba(48, 53, 56, 1), 690px 600px 0 0 rgba(48, 53, 56, 1),
  700px 600px 0 0 rgba(48, 53, 56, 1), 710px 600px 0 0 rgba(48, 53, 56, 1),
  720px 600px 0 0 rgba(48, 53, 56, 1), 730px 600px 0 0 rgba(48, 53, 56, 1),
  740px 600px 0 0 rgba(48, 53, 56, 1), 750px 600px 0 0 rgba(48, 53, 56, 1),
  760px 600px 0 0 rgba(48, 53, 56, 1), 770px 600px 0 0 rgba(48, 53, 56, 1),
  780px 600px 0 0 rgba(48, 53, 56, 1), 790px 600px 0 0 rgba(48, 53, 56, 1),
  800px 600px 0 0 rgba(48, 53, 56, 1), 810px 600px 0 0 rgba(48, 53, 56, 1),
  820px 600px 0 0 rgba(48, 53, 56, 1), 830px 600px 0 0 rgba(48, 53, 56, 1),
  840px 600px 0 0 rgba(48, 53, 56, 1), 850px 600px 0 0 rgba(48, 53, 56, 1),
  860px 600px 0 0 rgba(48, 53, 56, 1), 870px 600px 0 0 rgba(48, 53, 56, 1),
  880px 600px 0 0 rgba(48, 53, 56, 1), 890px 600px 0 0 rgba(48, 53, 56, 1),
  900px 600px 0 0 rgba(48, 53, 56, 1), 910px 600px 0 0 rgba(48, 53, 56, 1),
  920px 600px 0 0 rgba(48, 53, 56, 1), 930px 600px 0 0 rgba(48, 53, 56, 1),
  940px 600px 0 0 rgba(48, 53, 56, 1), 950px 600px 0 0 rgba(48, 53, 56, 1),
  960px 600px 0 0 rgba(48, 53, 56, 1), 970px 600px 0 0 rgba(48, 53, 56, 1),
  980px 600px 0 0 rgba(48, 53, 56, 1), 990px 600px 0 0 rgba(48, 53, 56, 1),
  1000px 600px 0 0 rgba(48, 53, 56, 1), 10px 610px 0 0 rgba(28, 32, 34, 1),
  20px 610px 0 0 rgba(219, 222, 232, 1), 30px 610px 0 0 rgba(111, 114, 121, 1),
  40px 610px 0 0 rgba(28, 32, 34, 1), 50px 610px 0 0 rgba(28, 32, 34, 1),
  60px 610px 0 0 rgba(28, 32, 34, 1), 70px 610px 0 0 rgba(28, 32, 34, 1),
  80px 610px 0 0 rgba(28, 32, 34, 1), 90px 610px 0 0 rgba(28, 32, 34, 1),
  100px 610px 0 0 rgba(28, 32, 34, 1), 110px 610px 0 0 rgba(28, 32, 34, 1),
  120px 610px 0 0 rgba(28, 32, 34, 1), 130px 610px 0 0 rgba(28, 32, 34, 1),
  140px 610px 0 0 rgba(28, 32, 34, 1), 150px 610px 0 0 rgba(28, 32, 34, 1),
  160px 610px 0 0 rgba(28, 32, 34, 1), 170px 610px 0 0 rgba(28, 32, 34, 1),
  180px 610px 0 0 rgba(28, 32, 34, 1), 190px 610px 0 0 rgba(28, 32, 34, 1),
  200px 610px 0 0 rgba(28, 32, 34, 1), 210px 610px 0 0 rgba(28, 32, 34, 1),
  220px 610px 0 0 rgba(28, 32, 34, 1), 230px 610px 0 0 rgba(28, 32, 34, 1),
  240px 610px 0 0 rgba(28, 32, 34, 1), 250px 610px 0 0 rgba(28, 32, 34, 1),
  260px 610px 0 0 rgba(28, 32, 34, 1), 270px 610px 0 0 rgba(28, 32, 34, 1),
  280px 610px 0 0 rgba(28, 32, 34, 1), 290px 610px 0 0 rgba(28, 32, 34, 1),
  300px 610px 0 0 rgba(28, 32, 34, 1), 310px 610px 0 0 rgba(28, 32, 34, 1),
  320px 610px 0 0 rgba(28, 32, 34, 1), 330px 610px 0 0 rgba(28, 32, 34, 1),
  340px 610px 0 0 rgba(28, 32, 34, 1), 350px 610px 0 0 rgba(28, 32, 34, 1),
  360px 610px 0 0 rgba(28, 32, 34, 1), 370px 610px 0 0 rgba(28, 32, 34, 1),
  380px 610px 0 0 rgba(28, 32, 34, 1), 390px 610px 0 0 rgba(28, 32, 34, 1),
  400px 610px 0 0 rgba(28, 32, 34, 1), 410px 610px 0 0 rgba(28, 32, 34, 1),
  420px 610px 0 0 rgba(28, 32, 34, 1), 430px 610px 0 0 rgba(28, 32, 34, 1),
  440px 610px 0 0 rgba(28, 32, 34, 1), 450px 610px 0 0 rgba(28, 32, 34, 1),
  460px 610px 0 0 rgba(28, 32, 34, 1), 470px 610px 0 0 rgba(28, 32, 34, 1),
  480px 610px 0 0 rgba(28, 32, 34, 1), 490px 610px 0 0 rgba(28, 32, 34, 1),
  500px 610px 0 0 rgba(28, 32, 34, 1), 510px 610px 0 0 rgba(28, 32, 34, 1),
  520px 610px 0 0 rgba(28, 32, 34, 1), 530px 610px 0 0 rgba(28, 32, 34, 1),
  540px 610px 0 0 rgba(28, 32, 34, 1), 550px 610px 0 0 rgba(28, 32, 34, 1),
  560px 610px 0 0 rgba(28, 32, 34, 1), 570px 610px 0 0 rgba(28, 32, 34, 1),
  580px 610px 0 0 rgba(28, 32, 34, 1), 590px 610px 0 0 rgba(28, 32, 34, 1),
  600px 610px 0 0 rgba(28, 32, 34, 1), 610px 610px 0 0 rgba(28, 32, 34, 1),
  620px 610px 0 0 rgba(28, 32, 34, 1), 630px 610px 0 0 rgba(28, 32, 34, 1),
  640px 610px 0 0 rgba(28, 32, 34, 1), 650px 610px 0 0 rgba(28, 32, 34, 1),
  660px 610px 0 0 rgba(28, 32, 34, 1), 670px 610px 0 0 rgba(28, 32, 34, 1),
  680px 610px 0 0 rgba(28, 32, 34, 1), 690px 610px 0 0 rgba(28, 32, 34, 1),
  700px 610px 0 0 rgba(28, 32, 34, 1), 710px 610px 0 0 rgba(28, 32, 34, 1),
  720px 610px 0 0 rgba(28, 32, 34, 1), 730px 610px 0 0 rgba(28, 32, 34, 1),
  740px 610px 0 0 rgba(28, 32, 34, 1), 750px 610px 0 0 rgba(28, 32, 34, 1),
  760px 610px 0 0 rgba(28, 32, 34, 1), 770px 610px 0 0 rgba(28, 32, 34, 1),
  780px 610px 0 0 rgba(28, 32, 34, 1), 790px 610px 0 0 rgba(28, 32, 34, 1),
  800px 610px 0 0 rgba(28, 32, 34, 1), 810px 610px 0 0 rgba(28, 32, 34, 1),
  820px 610px 0 0 rgba(28, 32, 34, 1), 830px 610px 0 0 rgba(28, 32, 34, 1),
  840px 610px 0 0 rgba(28, 32, 34, 1), 850px 610px 0 0 rgba(28, 32, 34, 1),
  860px 610px 0 0 rgba(28, 32, 34, 1), 870px 610px 0 0 rgba(28, 32, 34, 1),
  880px 610px 0 0 rgba(28, 32, 34, 1), 890px 610px 0 0 rgba(28, 32, 34, 1),
  900px 610px 0 0 rgba(28, 32, 34, 1), 910px 610px 0 0 rgba(28, 32, 34, 1),
  920px 610px 0 0 rgba(28, 32, 34, 1), 930px 610px 0 0 rgba(28, 32, 34, 1),
  940px 610px 0 0 rgba(28, 32, 34, 1), 950px 610px 0 0 rgba(28, 32, 34, 1),
  960px 610px 0 0 rgba(28, 32, 34, 1), 970px 610px 0 0 rgba(28, 32, 34, 1),
  980px 610px 0 0 rgba(28, 32, 34, 1), 990px 610px 0 0 rgba(28, 32, 34, 1),
  1000px 610px 0 0 rgba(28, 32, 34, 1), 10px 620px 0 0 rgba(28, 32, 34, 1),
  20px 620px 0 0 rgba(219, 222, 232, 1), 30px 620px 0 0 rgba(111, 114, 121, 1),
  40px 620px 0 0 rgba(89, 92, 100, 1), 50px 620px 0 0 rgba(89, 92, 100, 1),
  60px 620px 0 0 rgba(89, 92, 100, 1), 70px 620px 0 0 rgba(89, 92, 100, 1),
  80px 620px 0 0 rgba(89, 92, 100, 1), 90px 620px 0 0 rgba(89, 92, 100, 1),
  100px 620px 0 0 rgba(89, 92, 100, 1), 110px 620px 0 0 rgba(89, 92, 100, 1),
  120px 620px 0 0 rgba(89, 92, 100, 1), 130px 620px 0 0 rgba(89, 92, 100, 1),
  140px 620px 0 0 rgba(89, 92, 100, 1), 150px 620px 0 0 rgba(89, 92, 100, 1),
  160px 620px 0 0 rgba(89, 92, 100, 1), 170px 620px 0 0 rgba(89, 92, 100, 1),
  180px 620px 0 0 rgba(89, 92, 100, 1), 190px 620px 0 0 rgba(89, 92, 100, 1),
  200px 620px 0 0 rgba(89, 92, 100, 1), 210px 620px 0 0 rgba(89, 92, 100, 1),
  220px 620px 0 0 rgba(89, 92, 100, 1), 230px 620px 0 0 rgba(89, 92, 100, 1),
  240px 620px 0 0 rgba(89, 92, 100, 1), 250px 620px 0 0 rgba(89, 92, 100, 1),
  260px 620px 0 0 rgba(89, 92, 100, 1), 270px 620px 0 0 rgba(89, 92, 100, 1),
  280px 620px 0 0 rgba(89, 92, 100, 1), 290px 620px 0 0 rgba(89, 92, 100, 1),
  300px 620px 0 0 rgba(89, 92, 100, 1), 310px 620px 0 0 rgba(89, 92, 100, 1),
  320px 620px 0 0 rgba(89, 92, 100, 1), 330px 620px 0 0 rgba(89, 92, 100, 1),
  340px 620px 0 0 rgba(89, 92, 100, 1), 350px 620px 0 0 rgba(89, 92, 100, 1),
  360px 620px 0 0 rgba(89, 92, 100, 1), 370px 620px 0 0 rgba(89, 92, 100, 1),
  380px 620px 0 0 rgba(89, 92, 100, 1), 390px 620px 0 0 rgba(89, 92, 100, 1),
  400px 620px 0 0 rgba(89, 92, 100, 1), 410px 620px 0 0 rgba(89, 92, 100, 1),
  420px 620px 0 0 rgba(89, 92, 100, 1), 430px 620px 0 0 rgba(89, 92, 100, 1),
  440px 620px 0 0 rgba(89, 92, 100, 1), 450px 620px 0 0 rgba(89, 92, 100, 1),
  460px 620px 0 0 rgba(89, 92, 100, 1), 470px 620px 0 0 rgba(89, 92, 100, 1),
  480px 620px 0 0 rgba(89, 92, 100, 1), 490px 620px 0 0 rgba(89, 92, 100, 1),
  500px 620px 0 0 rgba(89, 92, 100, 1), 510px 620px 0 0 rgba(89, 92, 100, 1),
  520px 620px 0 0 rgba(89, 92, 100, 1), 530px 620px 0 0 rgba(89, 92, 100, 1),
  540px 620px 0 0 rgba(89, 92, 100, 1), 550px 620px 0 0 rgba(89, 92, 100, 1),
  560px 620px 0 0 rgba(89, 92, 100, 1), 570px 620px 0 0 rgba(89, 92, 100, 1),
  580px 620px 0 0 rgba(89, 92, 100, 1), 590px 620px 0 0 rgba(89, 92, 100, 1),
  600px 620px 0 0 rgba(89, 92, 100, 1), 610px 620px 0 0 rgba(89, 92, 100, 1),
  620px 620px 0 0 rgba(89, 92, 100, 1), 630px 620px 0 0 rgba(89, 92, 100, 1),
  640px 620px 0 0 rgba(89, 92, 100, 1), 650px 620px 0 0 rgba(89, 92, 100, 1),
  660px 620px 0 0 rgba(89, 92, 100, 1), 670px 620px 0 0 rgba(89, 92, 100, 1),
  680px 620px 0 0 rgba(89, 92, 100, 1), 690px 620px 0 0 rgba(89, 92, 100, 1),
  700px 620px 0 0 rgba(89, 92, 100, 1), 710px 620px 0 0 rgba(89, 92, 100, 1),
  720px 620px 0 0 rgba(89, 92, 100, 1), 730px 620px 0 0 rgba(89, 92, 100, 1),
  740px 620px 0 0 rgba(89, 92, 100, 1), 750px 620px 0 0 rgba(89, 92, 100, 1),
  760px 620px 0 0 rgba(89, 92, 100, 1), 770px 620px 0 0 rgba(89, 92, 100, 1),
  780px 620px 0 0 rgba(89, 92, 100, 1), 790px 620px 0 0 rgba(89, 92, 100, 1),
  800px 620px 0 0 rgba(89, 92, 100, 1), 810px 620px 0 0 rgba(89, 92, 100, 1),
  820px 620px 0 0 rgba(89, 92, 100, 1), 830px 620px 0 0 rgba(89, 92, 100, 1),
  840px 620px 0 0 rgba(89, 92, 100, 1), 850px 620px 0 0 rgba(89, 92, 100, 1),
  860px 620px 0 0 rgba(89, 92, 100, 1), 870px 620px 0 0 rgba(89, 92, 100, 1),
  880px 620px 0 0 rgba(89, 92, 100, 1), 890px 620px 0 0 rgba(89, 92, 100, 1),
  900px 620px 0 0 rgba(89, 92, 100, 1), 910px 620px 0 0 rgba(89, 92, 100, 1),
  920px 620px 0 0 rgba(89, 92, 100, 1), 930px 620px 0 0 rgba(89, 92, 100, 1),
  940px 620px 0 0 rgba(89, 92, 100, 1), 950px 620px 0 0 rgba(89, 92, 100, 1),
  960px 620px 0 0 rgba(89, 92, 100, 1), 970px 620px 0 0 rgba(89, 92, 100, 1),
  980px 620px 0 0 rgba(89, 92, 100, 1), 990px 620px 0 0 rgba(89, 92, 100, 1),
  1000px 620px 0 0 rgba(89, 92, 100, 1), 10px 630px 0 0 rgba(28, 32, 34, 1),
  20px 630px 0 0 rgba(219, 222, 232, 1), 30px 630px 0 0 rgba(111, 114, 121, 1),
  40px 630px 0 0 rgba(111, 114, 121, 1), 50px 630px 0 0 rgba(111, 114, 121, 1),
  60px 630px 0 0 rgba(111, 114, 121, 1), 70px 630px 0 0 rgba(111, 114, 121, 1),
  80px 630px 0 0 rgba(111, 114, 121, 1), 90px 630px 0 0 rgba(111, 114, 121, 1),
  100px 630px 0 0 rgba(111, 114, 121, 1), 110px 630px 0 0 rgba(111, 114, 121, 1),
  120px 630px 0 0 rgba(111, 114, 121, 1), 130px 630px 0 0 rgba(111, 114, 121, 1),
  140px 630px 0 0 rgba(111, 114, 121, 1), 150px 630px 0 0 rgba(111, 114, 121, 1),
  160px 630px 0 0 rgba(111, 114, 121, 1), 170px 630px 0 0 rgba(111, 114, 121, 1),
  180px 630px 0 0 rgba(111, 114, 121, 1), 190px 630px 0 0 rgba(111, 114, 121, 1),
  200px 630px 0 0 rgba(111, 114, 121, 1), 210px 630px 0 0 rgba(111, 114, 121, 1),
  220px 630px 0 0 rgba(111, 114, 121, 1), 230px 630px 0 0 rgba(111, 114, 121, 1),
  240px 630px 0 0 rgba(111, 114, 121, 1), 250px 630px 0 0 rgba(111, 114, 121, 1),
  260px 630px 0 0 rgba(111, 114, 121, 1), 270px 630px 0 0 rgba(111, 114, 121, 1),
  280px 630px 0 0 rgba(111, 114, 121, 1), 290px 630px 0 0 rgba(111, 114, 121, 1),
  300px 630px 0 0 rgba(111, 114, 121, 1), 310px 630px 0 0 rgba(111, 114, 121, 1),
  320px 630px 0 0 rgba(111, 114, 121, 1), 330px 630px 0 0 rgba(111, 114, 121, 1),
  340px 630px 0 0 rgba(111, 114, 121, 1), 350px 630px 0 0 rgba(111, 114, 121, 1),
  360px 630px 0 0 rgba(111, 114, 121, 1), 370px 630px 0 0 rgba(111, 114, 121, 1),
  380px 630px 0 0 rgba(111, 114, 121, 1), 390px 630px 0 0 rgba(111, 114, 121, 1),
  400px 630px 0 0 rgba(111, 114, 121, 1), 410px 630px 0 0 rgba(111, 114, 121, 1),
  420px 630px 0 0 rgba(111, 114, 121, 1), 430px 630px 0 0 rgba(111, 114, 121, 1),
  440px 630px 0 0 rgba(111, 114, 121, 1), 450px 630px 0 0 rgba(111, 114, 121, 1),
  460px 630px 0 0 rgba(111, 114, 121, 1), 470px 630px 0 0 rgba(111, 114, 121, 1),
  480px 630px 0 0 rgba(111, 114, 121, 1), 490px 630px 0 0 rgba(111, 114, 121, 1),
  500px 630px 0 0 rgba(111, 114, 121, 1), 510px 630px 0 0 rgba(111, 114, 121, 1),
  520px 630px 0 0 rgba(111, 114, 121, 1), 530px 630px 0 0 rgba(111, 114, 121, 1),
  540px 630px 0 0 rgba(111, 114, 121, 1), 550px 630px 0 0 rgba(111, 114, 121, 1),
  560px 630px 0 0 rgba(111, 114, 121, 1), 570px 630px 0 0 rgba(111, 114, 121, 1),
  580px 630px 0 0 rgba(111, 114, 121, 1), 590px 630px 0 0 rgba(111, 114, 121, 1),
  600px 630px 0 0 rgba(111, 114, 121, 1), 610px 630px 0 0 rgba(111, 114, 121, 1),
  620px 630px 0 0 rgba(111, 114, 121, 1), 630px 630px 0 0 rgba(111, 114, 121, 1),
  640px 630px 0 0 rgba(111, 114, 121, 1), 650px 630px 0 0 rgba(111, 114, 121, 1),
  660px 630px 0 0 rgba(111, 114, 121, 1), 670px 630px 0 0 rgba(111, 114, 121, 1),
  680px 630px 0 0 rgba(111, 114, 121, 1), 690px 630px 0 0 rgba(111, 114, 121, 1),
  700px 630px 0 0 rgba(111, 114, 121, 1), 710px 630px 0 0 rgba(111, 114, 121, 1),
  720px 630px 0 0 rgba(111, 114, 121, 1), 730px 630px 0 0 rgba(111, 114, 121, 1),
  740px 630px 0 0 rgba(111, 114, 121, 1), 750px 630px 0 0 rgba(111, 114, 121, 1),
  760px 630px 0 0 rgba(111, 114, 121, 1), 770px 630px 0 0 rgba(111, 114, 121, 1),
  780px 630px 0 0 rgba(111, 114, 121, 1), 790px 630px 0 0 rgba(111, 114, 121, 1),
  800px 630px 0 0 rgba(111, 114, 121, 1), 810px 630px 0 0 rgba(111, 114, 121, 1),
  820px 630px 0 0 rgba(111, 114, 121, 1), 830px 630px 0 0 rgba(111, 114, 121, 1),
  840px 630px 0 0 rgba(111, 114, 121, 1), 850px 630px 0 0 rgba(111, 114, 121, 1),
  860px 630px 0 0 rgba(111, 114, 121, 1), 870px 630px 0 0 rgba(111, 114, 121, 1),
  880px 630px 0 0 rgba(111, 114, 121, 1), 890px 630px 0 0 rgba(111, 114, 121, 1),
  900px 630px 0 0 rgba(111, 114, 121, 1), 910px 630px 0 0 rgba(111, 114, 121, 1),
  920px 630px 0 0 rgba(111, 114, 121, 1), 930px 630px 0 0 rgba(111, 114, 121, 1),
  940px 630px 0 0 rgba(111, 114, 121, 1), 950px 630px 0 0 rgba(111, 114, 121, 1),
  960px 630px 0 0 rgba(111, 114, 121, 1), 970px 630px 0 0 rgba(111, 114, 121, 1),
  980px 630px 0 0 rgba(111, 114, 121, 1), 990px 630px 0 0 rgba(111, 114, 121, 1),
  1000px 630px 0 0 rgba(111, 114, 121, 1), 10px 640px 0 0 rgba(28, 32, 34, 1),
  20px 640px 0 0 rgba(28, 32, 34, 1), 30px 640px 0 0 rgba(28, 32, 34, 1),
  40px 640px 0 0 rgba(28, 32, 34, 1), 50px 640px 0 0 rgba(28, 32, 34, 1),
  60px 640px 0 0 rgba(28, 32, 34, 1), 70px 640px 0 0 rgba(28, 32, 34, 1),
  80px 640px 0 0 rgba(28, 32, 34, 1), 90px 640px 0 0 rgba(28, 32, 34, 1),
  100px 640px 0 0 rgba(28, 32, 34, 1), 110px 640px 0 0 rgba(28, 32, 34, 1),
  120px 640px 0 0 rgba(28, 32, 34, 1), 130px 640px 0 0 rgba(28, 32, 34, 1),
  140px 640px 0 0 rgba(28, 32, 34, 1), 150px 640px 0 0 rgba(28, 32, 34, 1),
  160px 640px 0 0 rgba(28, 32, 34, 1), 170px 640px 0 0 rgba(28, 32, 34, 1),
  180px 640px 0 0 rgba(28, 32, 34, 1), 190px 640px 0 0 rgba(28, 32, 34, 1),
  200px 640px 0 0 rgba(28, 32, 34, 1), 210px 640px 0 0 rgba(28, 32, 34, 1),
  220px 640px 0 0 rgba(28, 32, 34, 1), 230px 640px 0 0 rgba(28, 32, 34, 1),
  240px 640px 0 0 rgba(28, 32, 34, 1), 250px 640px 0 0 rgba(28, 32, 34, 1),
  260px 640px 0 0 rgba(28, 32, 34, 1), 270px 640px 0 0 rgba(28, 32, 34, 1),
  280px 640px 0 0 rgba(28, 32, 34, 1), 290px 640px 0 0 rgba(28, 32, 34, 1),
  300px 640px 0 0 rgba(28, 32, 34, 1), 310px 640px 0 0 rgba(28, 32, 34, 1),
  320px 640px 0 0 rgba(28, 32, 34, 1), 330px 640px 0 0 rgba(28, 32, 34, 1),
  340px 640px 0 0 rgba(28, 32, 34, 1), 350px 640px 0 0 rgba(28, 32, 34, 1),
  360px 640px 0 0 rgba(28, 32, 34, 1), 370px 640px 0 0 rgba(28, 32, 34, 1),
  380px 640px 0 0 rgba(28, 32, 34, 1), 390px 640px 0 0 rgba(28, 32, 34, 1),
  400px 640px 0 0 rgba(28, 32, 34, 1), 410px 640px 0 0 rgba(28, 32, 34, 1),
  420px 640px 0 0 rgba(28, 32, 34, 1), 430px 640px 0 0 rgba(28, 32, 34, 1),
  440px 640px 0 0 rgba(28, 32, 34, 1), 450px 640px 0 0 rgba(28, 32, 34, 1),
  460px 640px 0 0 rgba(28, 32, 34, 1), 470px 640px 0 0 rgba(28, 32, 34, 1),
  480px 640px 0 0 rgba(28, 32, 34, 1), 490px 640px 0 0 rgba(28, 32, 34, 1),
  500px 640px 0 0 rgba(28, 32, 34, 1), 510px 640px 0 0 rgba(28, 32, 34, 1),
  520px 640px 0 0 rgba(28, 32, 34, 1), 530px 640px 0 0 rgba(28, 32, 34, 1),
  540px 640px 0 0 rgba(28, 32, 34, 1), 550px 640px 0 0 rgba(28, 32, 34, 1),
  560px 640px 0 0 rgba(28, 32, 34, 1), 570px 640px 0 0 rgba(28, 32, 34, 1),
  580px 640px 0 0 rgba(28, 32, 34, 1), 590px 640px 0 0 rgba(28, 32, 34, 1),
  600px 640px 0 0 rgba(28, 32, 34, 1), 610px 640px 0 0 rgba(28, 32, 34, 1),
  620px 640px 0 0 rgba(28, 32, 34, 1), 630px 640px 0 0 rgba(28, 32, 34, 1),
  640px 640px 0 0 rgba(28, 32, 34, 1), 650px 640px 0 0 rgba(28, 32, 34, 1),
  660px 640px 0 0 rgba(28, 32, 34, 1), 670px 640px 0 0 rgba(28, 32, 34, 1),
  680px 640px 0 0 rgba(28, 32, 34, 1), 690px 640px 0 0 rgba(28, 32, 34, 1),
  700px 640px 0 0 rgba(28, 32, 34, 1), 710px 640px 0 0 rgba(28, 32, 34, 1),
  720px 640px 0 0 rgba(28, 32, 34, 1), 730px 640px 0 0 rgba(28, 32, 34, 1),
  740px 640px 0 0 rgba(28, 32, 34, 1), 750px 640px 0 0 rgba(28, 32, 34, 1),
  760px 640px 0 0 rgba(28, 32, 34, 1), 770px 640px 0 0 rgba(28, 32, 34, 1),
  780px 640px 0 0 rgba(28, 32, 34, 1), 790px 640px 0 0 rgba(28, 32, 34, 1),
  800px 640px 0 0 rgba(28, 32, 34, 1), 810px 640px 0 0 rgba(28, 32, 34, 1),
  820px 640px 0 0 rgba(28, 32, 34, 1), 830px 640px 0 0 rgba(28, 32, 34, 1),
  840px 640px 0 0 rgba(28, 32, 34, 1), 850px 640px 0 0 rgba(28, 32, 34, 1),
  860px 640px 0 0 rgba(28, 32, 34, 1), 870px 640px 0 0 rgba(28, 32, 34, 1),
  880px 640px 0 0 rgba(28, 32, 34, 1), 890px 640px 0 0 rgba(28, 32, 34, 1),
  900px 640px 0 0 rgba(28, 32, 34, 1), 910px 640px 0 0 rgba(28, 32, 34, 1),
  920px 640px 0 0 rgba(28, 32, 34, 1), 930px 640px 0 0 rgba(28, 32, 34, 1),
  940px 640px 0 0 rgba(28, 32, 34, 1), 950px 640px 0 0 rgba(28, 32, 34, 1),
  960px 640px 0 0 rgba(28, 32, 34, 1), 970px 640px 0 0 rgba(28, 32, 34, 1),
  980px 640px 0 0 rgba(28, 32, 34, 1), 990px 640px 0 0 rgba(28, 32, 34, 1),
  1000px 640px 0 0 rgba(28, 32, 34, 1);
 height: 10px;
 width: 10px;
}
.pixelart-to-css-text {
 box-shadow: 20px 5px 0 0 rgba(255, 255, 255, 1),
  25px 5px 0 0 rgba(255, 255, 255, 1), 30px 5px 0 0 rgba(255, 255, 255, 1),
  35px 5px 0 0 rgba(255, 255, 255, 1), 40px 5px 0 0 rgba(255, 255, 255, 1),
  45px 5px 0 0 rgba(255, 255, 255, 1), 50px 5px 0 0 rgba(255, 255, 255, 1),
  55px 5px 0 0 rgba(255, 255, 255, 1), 60px 5px 0 0 rgba(255, 255, 255, 1),
  65px 5px 0 0 rgba(255, 255, 255, 1), 70px 5px 0 0 rgba(255, 255, 255, 1),
  75px 5px 0 0 rgba(255, 255, 255, 1), 80px 5px 0 0 rgba(255, 255, 255, 1),
  85px 5px 0 0 rgba(255, 255, 255, 1), 90px 5px 0 0 rgba(255, 255, 255, 1),
  95px 5px 0 0 rgba(255, 255, 255, 1), 100px 5px 0 0 rgba(255, 255, 255, 1),
  105px 5px 0 0 rgba(255, 255, 255, 1), 110px 5px 0 0 rgba(255, 255, 255, 1),
  115px 5px 0 0 rgba(255, 255, 255, 1), 120px 5px 0 0 rgba(255, 255, 255, 1),
  125px 5px 0 0 rgba(255, 255, 255, 1), 130px 5px 0 0 rgba(255, 255, 255, 1),
  135px 5px 0 0 rgba(255, 255, 255, 1), 140px 5px 0 0 rgba(255, 255, 255, 1),
  15px 10px 0 0 rgba(255, 255, 255, 1), 20px 10px 0 0 rgba(48, 53, 57, 1),
  25px 10px 0 0 rgba(48, 53, 57, 1), 30px 10px 0 0 rgba(48, 53, 57, 1),
  35px 10px 0 0 rgba(48, 53, 57, 1), 40px 10px 0 0 rgba(48, 53, 57, 1),
  45px 10px 0 0 rgba(48, 53, 57, 1), 50px 10px 0 0 rgba(48, 53, 57, 1),
  55px 10px 0 0 rgba(48, 53, 57, 1), 60px 10px 0 0 rgba(48, 53, 57, 1),
  65px 10px 0 0 rgba(48, 53, 57, 1), 70px 10px 0 0 rgba(48, 53, 57, 1),
  75px 10px 0 0 rgba(48, 53, 57, 1), 80px 10px 0 0 rgba(48, 53, 57, 1),
  85px 10px 0 0 rgba(48, 53, 57, 1), 90px 10px 0 0 rgba(48, 53, 57, 1),
  95px 10px 0 0 rgba(48, 53, 57, 1), 100px 10px 0 0 rgba(48, 53, 57, 1),
  105px 10px 0 0 rgba(48, 53, 57, 1), 110px 10px 0 0 rgba(48, 53, 57, 1),
  115px 10px 0 0 rgba(48, 53, 57, 1), 120px 10px 0 0 rgba(48, 53, 57, 1),
  125px 10px 0 0 rgba(48, 53, 57, 1), 130px 10px 0 0 rgba(48, 53, 57, 1),
  135px 10px 0 0 rgba(48, 53, 57, 1), 140px 10px 0 0 rgba(48, 53, 57, 1),
  145px 10px 0 0 rgba(255, 255, 255, 1), 10px 15px 0 0 rgba(255, 255, 255, 1),
  15px 15px 0 0 rgba(48, 53, 57, 1), 20px 15px 0 0 rgba(255, 255, 255, 1),
  25px 15px 0 0 rgba(255, 255, 255, 1), 30px 15px 0 0 rgba(255, 255, 255, 1),
  35px 15px 0 0 rgba(255, 255, 255, 1), 40px 15px 0 0 rgba(255, 255, 255, 1),
  45px 15px 0 0 rgba(255, 255, 255, 1), 50px 15px 0 0 rgba(255, 255, 255, 1),
  55px 15px 0 0 rgba(255, 255, 255, 1), 60px 15px 0 0 rgba(255, 255, 255, 1),
  65px 15px 0 0 rgba(255, 255, 255, 1), 70px 15px 0 0 rgba(255, 255, 255, 1),
  75px 15px 0 0 rgba(255, 255, 255, 1), 80px 15px 0 0 rgba(255, 255, 255, 1),
  85px 15px 0 0 rgba(255, 255, 255, 1), 90px 15px 0 0 rgba(255, 255, 255, 1),
  95px 15px 0 0 rgba(255, 255, 255, 1), 100px 15px 0 0 rgba(255, 255, 255, 1),
  105px 15px 0 0 rgba(255, 255, 255, 1), 110px 15px 0 0 rgba(255, 255, 255, 1),
  115px 15px 0 0 rgba(255, 255, 255, 1), 120px 15px 0 0 rgba(255, 255, 255, 1),
  125px 15px 0 0 rgba(255, 255, 255, 1), 130px 15px 0 0 rgba(255, 255, 255, 1),
  135px 15px 0 0 rgba(255, 255, 255, 1), 140px 15px 0 0 rgba(255, 255, 255, 1),
  145px 15px 0 0 rgba(48, 53, 57, 1), 150px 15px 0 0 rgba(255, 255, 255, 1),
  5px 20px 0 0 rgba(255, 255, 255, 1), 10px 20px 0 0 rgba(48, 53, 57, 1),
  15px 20px 0 0 rgba(255, 255, 255, 1), 20px 20px 0 0 rgba(255, 255, 255, 1),
  25px 20px 0 0 rgba(255, 255, 255, 1), 30px 20px 0 0 rgba(255, 255, 255, 1),
  35px 20px 0 0 rgba(255, 255, 255, 1), 40px 20px 0 0 rgba(48, 53, 57, 1),
  45px 20px 0 0 rgba(48, 53, 57, 1), 50px 20px 0 0 rgba(48, 53, 57, 1),
  55px 20px 0 0 rgba(255, 255, 255, 1), 60px 20px 0 0 rgba(48, 53, 57, 1),
  65px 20px 0 0 rgba(48, 53, 57, 1), 70px 20px 0 0 rgba(48, 53, 57, 1),
  75px 20px 0 0 rgba(255, 255, 255, 1), 80px 20px 0 0 rgba(48, 53, 57, 1),
  85px 20px 0 0 rgba(255, 255, 255, 1), 90px 20px 0 0 rgba(255, 255, 255, 1),
  95px 20px 0 0 rgba(255, 255, 255, 1), 100px 20px 0 0 rgba(48, 53, 57, 1),
  105px 20px 0 0 rgba(255, 255, 255, 1), 110px 20px 0 0 rgba(48, 53, 57, 1),
  115px 20px 0 0 rgba(48, 53, 57, 1), 120px 20px 0 0 rgba(48, 53, 57, 1),
  125px 20px 0 0 rgba(255, 255, 255, 1), 130px 20px 0 0 rgba(255, 255, 255, 1),
  135px 20px 0 0 rgba(255, 255, 255, 1), 140px 20px 0 0 rgba(255, 255, 255, 1),
  145px 20px 0 0 rgba(255, 255, 255, 1), 150px 20px 0 0 rgba(48, 53, 57, 1),
  155px 20px 0 0 rgba(255, 255, 255, 1), 5px 25px 0 0 rgba(255, 255, 255, 1),
  10px 25px 0 0 rgba(48, 53, 57, 1), 15px 25px 0 0 rgba(255, 255, 255, 1),
  20px 25px 0 0 rgba(255, 255, 255, 1), 25px 25px 0 0 rgba(255, 255, 255, 1),
  30px 25px 0 0 rgba(255, 255, 255, 1), 35px 25px 0 0 rgba(255, 255, 255, 1),
  40px 25px 0 0 rgba(255, 255, 255, 1), 45px 25px 0 0 rgba(48, 53, 57, 1),
  50px 25px 0 0 rgba(255, 255, 255, 1), 55px 25px 0 0 rgba(255, 255, 255, 1),
  60px 25px 0 0 rgba(48, 53, 57, 1), 65px 25px 0 0 rgba(255, 255, 255, 1),
  70px 25px 0 0 rgba(255, 255, 255, 1), 75px 25px 0 0 rgba(255, 255, 255, 1),
  80px 25px 0 0 rgba(255, 255, 255, 1), 85px 25px 0 0 rgba(48, 53, 57, 1),
  90px 25px 0 0 rgba(255, 255, 255, 1), 95px 25px 0 0 rgba(48, 53, 57, 1),
  100px 25px 0 0 rgba(255, 255, 255, 1), 105px 25px 0 0 rgba(255, 255, 255, 1),
  110px 25px 0 0 rgba(255, 255, 255, 1), 115px 25px 0 0 rgba(48, 53, 57, 1),
  120px 25px 0 0 rgba(255, 255, 255, 1), 125px 25px 0 0 rgba(255, 255, 255, 1),
  130px 25px 0 0 rgba(255, 255, 255, 1), 135px 25px 0 0 rgba(255, 255, 255, 1),
  140px 25px 0 0 rgba(255, 255, 255, 1), 145px 25px 0 0 rgba(255, 255, 255, 1),
  150px 25px 0 0 rgba(48, 53, 57, 1), 155px 25px 0 0 rgba(255, 255, 255, 1),
  5px 30px 0 0 rgba(255, 255, 255, 1), 10px 30px 0 0 rgba(48, 53, 57, 1),
  15px 30px 0 0 rgba(255, 255, 255, 1), 20px 30px 0 0 rgba(255, 255, 255, 1),
  25px 30px 0 0 rgba(255, 255, 255, 1), 30px 30px 0 0 rgba(255, 255, 255, 1),
  35px 30px 0 0 rgba(255, 255, 255, 1), 40px 30px 0 0 rgba(255, 255, 255, 1),
  45px 30px 0 0 rgba(48, 53, 57, 1), 50px 30px 0 0 rgba(255, 255, 255, 1),
  55px 30px 0 0 rgba(255, 255, 255, 1), 60px 30px 0 0 rgba(48, 53, 57, 1),
  65px 30px 0 0 rgba(48, 53, 57, 1), 70px 30px 0 0 rgba(255, 255, 255, 1),
  75px 30px 0 0 rgba(255, 255, 255, 1), 80px 30px 0 0 rgba(255, 255, 255, 1),
  85px 30px 0 0 rgba(255, 255, 255, 1), 90px 30px 0 0 rgba(48, 53, 57, 1),
  95px 30px 0 0 rgba(255, 255, 255, 1), 100px 30px 0 0 rgba(255, 255, 255, 1),
  105px 30px 0 0 rgba(255, 255, 255, 1), 110px 30px 0 0 rgba(255, 255, 255, 1),
  115px 30px 0 0 rgba(48, 53, 57, 1), 120px 30px 0 0 rgba(255, 255, 255, 1),
  125px 30px 0 0 rgba(255, 255, 255, 1), 130px 30px 0 0 rgba(255, 255, 255, 1),
  135px 30px 0 0 rgba(255, 255, 255, 1), 140px 30px 0 0 rgba(255, 255, 255, 1),
  145px 30px 0 0 rgba(255, 255, 255, 1), 150px 30px 0 0 rgba(48, 53, 57, 1),
  155px 30px 0 0 rgba(255, 255, 255, 1), 5px 35px 0 0 rgba(255, 255, 255, 1),
  10px 35px 0 0 rgba(48, 53, 57, 1), 15px 35px 0 0 rgba(255, 255, 255, 1),
  20px 35px 0 0 rgba(255, 255, 255, 1), 25px 35px 0 0 rgba(255, 255, 255, 1),
  30px 35px 0 0 rgba(255, 255, 255, 1), 35px 35px 0 0 rgba(255, 255, 255, 1),
  40px 35px 0 0 rgba(255, 255, 255, 1), 45px 35px 0 0 rgba(48, 53, 57, 1),
  50px 35px 0 0 rgba(255, 255, 255, 1), 55px 35px 0 0 rgba(255, 255, 255, 1),
  60px 35px 0 0 rgba(48, 53, 57, 1), 65px 35px 0 0 rgba(255, 255, 255, 1),
  70px 35px 0 0 rgba(255, 255, 255, 1), 75px 35px 0 0 rgba(255, 255, 255, 1),
  80px 35px 0 0 rgba(255, 255, 255, 1), 85px 35px 0 0 rgba(48, 53, 57, 1),
  90px 35px 0 0 rgba(255, 255, 255, 1), 95px 35px 0 0 rgba(48, 53, 57, 1),
  100px 35px 0 0 rgba(255, 255, 255, 1), 105px 35px 0 0 rgba(255, 255, 255, 1),
  110px 35px 0 0 rgba(255, 255, 255, 1), 115px 35px 0 0 rgba(48, 53, 57, 1),
  120px 35px 0 0 rgba(255, 255, 255, 1), 125px 35px 0 0 rgba(255, 255, 255, 1),
  130px 35px 0 0 rgba(255, 255, 255, 1), 135px 35px 0 0 rgba(255, 255, 255, 1),
  140px 35px 0 0 rgba(255, 255, 255, 1), 145px 35px 0 0 rgba(255, 255, 255, 1),
  150px 35px 0 0 rgba(48, 53, 57, 1), 155px 35px 0 0 rgba(255, 255, 255, 1),
  5px 40px 0 0 rgba(255, 255, 255, 1), 10px 40px 0 0 rgba(48, 53, 57, 1),
  15px 40px 0 0 rgba(255, 255, 255, 1), 20px 40px 0 0 rgba(255, 255, 255, 1),
  25px 40px 0 0 rgba(255, 255, 255, 1), 30px 40px 0 0 rgba(255, 255, 255, 1),
  35px 40px 0 0 rgba(255, 255, 255, 1), 40px 40px 0 0 rgba(255, 255, 255, 1),
  45px 40px 0 0 rgba(48, 53, 57, 1), 50px 40px 0 0 rgba(255, 255, 255, 1),
  55px 40px 0 0 rgba(255, 255, 255, 1), 60px 40px 0 0 rgba(48, 53, 57, 1),
  65px 40px 0 0 rgba(48, 53, 57, 1), 70px 40px 0 0 rgba(48, 53, 57, 1),
  75px 40px 0 0 rgba(255, 255, 255, 1), 80px 40px 0 0 rgba(48, 53, 57, 1),
  85px 40px 0 0 rgba(255, 255, 255, 1), 90px 40px 0 0 rgba(255, 255, 255, 1),
  95px 40px 0 0 rgba(255, 255, 255, 1), 100px 40px 0 0 rgba(48, 53, 57, 1),
  105px 40px 0 0 rgba(255, 255, 255, 1), 110px 40px 0 0 rgba(255, 255, 255, 1),
  115px 40px 0 0 rgba(48, 53, 57, 1), 120px 40px 0 0 rgba(255, 255, 255, 1),
  125px 40px 0 0 rgba(255, 255, 255, 1), 130px 40px 0 0 rgba(255, 255, 255, 1),
  135px 40px 0 0 rgba(255, 255, 255, 1), 140px 40px 0 0 rgba(255, 255, 255, 1),
  145px 40px 0 0 rgba(255, 255, 255, 1), 150px 40px 0 0 rgba(48, 53, 57, 1),
  155px 40px 0 0 rgba(255, 255, 255, 1), 10px 45px 0 0 rgba(255, 255, 255, 1),
  15px 45px 0 0 rgba(48, 53, 57, 1), 20px 45px 0 0 rgba(255, 255, 255, 1),
  25px 45px 0 0 rgba(255, 255, 255, 1), 30px 45px 0 0 rgba(255, 255, 255, 1),
  35px 45px 0 0 rgba(255, 255, 255, 1), 40px 45px 0 0 rgba(255, 255, 255, 1),
  45px 45px 0 0 rgba(255, 255, 255, 1), 50px 45px 0 0 rgba(255, 255, 255, 1),
  55px 45px 0 0 rgba(255, 255, 255, 1), 60px 45px 0 0 rgba(255, 255, 255, 1),
  65px 45px 0 0 rgba(255, 255, 255, 1), 70px 45px 0 0 rgba(255, 255, 255, 1),
  75px 45px 0 0 rgba(255, 255, 255, 1), 80px 45px 0 0 rgba(255, 255, 255, 1),
  85px 45px 0 0 rgba(255, 255, 255, 1), 90px 45px 0 0 rgba(255, 255, 255, 1),
  95px 45px 0 0 rgba(255, 255, 255, 1), 100px 45px 0 0 rgba(255, 255, 255, 1),
  105px 45px 0 0 rgba(255, 255, 255, 1), 110px 45px 0 0 rgba(255, 255, 255, 1),
  115px 45px 0 0 rgba(255, 255, 255, 1), 120px 45px 0 0 rgba(255, 255, 255, 1),
  125px 45px 0 0 rgba(255, 255, 255, 1), 130px 45px 0 0 rgba(255, 255, 255, 1),
  135px 45px 0 0 rgba(255, 255, 255, 1), 140px 45px 0 0 rgba(255, 255, 255, 1),
  145px 45px 0 0 rgba(48, 53, 57, 1), 150px 45px 0 0 rgba(255, 255, 255, 1),
  15px 50px 0 0 rgba(255, 255, 255, 1), 20px 50px 0 0 rgba(48, 53, 57, 1),
  25px 50px 0 0 rgba(48, 53, 57, 1), 30px 50px 0 0 rgba(48, 53, 57, 1),
  35px 50px 0 0 rgba(48, 53, 57, 1), 40px 50px 0 0 rgba(48, 53, 57, 1),
  45px 50px 0 0 rgba(48, 53, 57, 1), 50px 50px 0 0 rgba(48, 53, 57, 1),
  55px 50px 0 0 rgba(48, 53, 57, 1), 60px 50px 0 0 rgba(48, 53, 57, 1),
  65px 50px 0 0 rgba(48, 53, 57, 1), 70px 50px 0 0 rgba(48, 53, 57, 1),
  75px 50px 0 0 rgba(48, 53, 57, 1), 80px 50px 0 0 rgba(48, 53, 57, 1),
  85px 50px 0 0 rgba(48, 53, 57, 1), 90px 50px 0 0 rgba(48, 53, 57, 1),
  95px 50px 0 0 rgba(48, 53, 57, 1), 100px 50px 0 0 rgba(48, 53, 57, 1),
  105px 50px 0 0 rgba(48, 53, 57, 1), 110px 50px 0 0 rgba(48, 53, 57, 1),
  115px 50px 0 0 rgba(48, 53, 57, 1), 120px 50px 0 0 rgba(48, 53, 57, 1),
  125px 50px 0 0 rgba(48, 53, 57, 1), 130px 50px 0 0 rgba(48, 53, 57, 1),
  135px 50px 0 0 rgba(48, 53, 57, 1), 140px 50px 0 0 rgba(48, 53, 57, 1),
  145px 50px 0 0 rgba(255, 255, 255, 1), 20px 55px 0 0 rgba(255, 255, 255, 1),
  25px 55px 0 0 rgba(255, 255, 255, 1), 30px 55px 0 0 rgba(255, 255, 255, 1),
  35px 55px 0 0 rgba(255, 255, 255, 1), 40px 55px 0 0 rgba(255, 255, 255, 1),
  45px 55px 0 0 rgba(255, 255, 255, 1), 50px 55px 0 0 rgba(255, 255, 255, 1),
  55px 55px 0 0 rgba(255, 255, 255, 1), 60px 55px 0 0 rgba(255, 255, 255, 1),
  65px 55px 0 0 rgba(255, 255, 255, 1), 70px 55px 0 0 rgba(255, 255, 255, 1),
  75px 55px 0 0 rgba(255, 255, 255, 1), 80px 55px 0 0 rgba(255, 255, 255, 1),
  85px 55px 0 0 rgba(255, 255, 255, 1), 90px 55px 0 0 rgba(255, 255, 255, 1),
  95px 55px 0 0 rgba(255, 255, 255, 1), 100px 55px 0 0 rgba(255, 255, 255, 1),
  105px 55px 0 0 rgba(255, 255, 255, 1), 110px 55px 0 0 rgba(255, 255, 255, 1),
  115px 55px 0 0 rgba(255, 255, 255, 1), 120px 55px 0 0 rgba(255, 255, 255, 1),
  125px 55px 0 0 rgba(255, 255, 255, 1), 130px 55px 0 0 rgba(255, 255, 255, 1),
  135px 55px 0 0 rgba(255, 255, 255, 1), 140px 55px 0 0 rgba(255, 255, 255, 1);
 height: 5px;
 width: 5px;
}
.pixelart-to-css-log {
 box-shadow: 20px 5px 0 0 rgba(255, 255, 255, 1),
  25px 5px 0 0 rgba(255, 255, 255, 1), 30px 5px 0 0 rgba(255, 255, 255, 1),
  35px 5px 0 0 rgba(255, 255, 255, 1), 40px 5px 0 0 rgba(255, 255, 255, 1),
  45px 5px 0 0 rgba(255, 255, 255, 1), 50px 5px 0 0 rgba(255, 255, 255, 1),
  55px 5px 0 0 rgba(255, 255, 255, 1), 60px 5px 0 0 rgba(255, 255, 255, 1),
  65px 5px 0 0 rgba(255, 255, 255, 1), 70px 5px 0 0 rgba(255, 255, 255, 1),
  75px 5px 0 0 rgba(255, 255, 255, 1), 80px 5px 0 0 rgba(255, 255, 255, 1),
  85px 5px 0 0 rgba(255, 255, 255, 1), 90px 5px 0 0 rgba(255, 255, 255, 1),
  95px 5px 0 0 rgba(255, 255, 255, 1), 100px 5px 0 0 rgba(255, 255, 255, 1),
  105px 5px 0 0 rgba(255, 255, 255, 1), 110px 5px 0 0 rgba(255, 255, 255, 1),
  115px 5px 0 0 rgba(255, 255, 255, 1), 120px 5px 0 0 rgba(255, 255, 255, 1),
  125px 5px 0 0 rgba(255, 255, 255, 1), 130px 5px 0 0 rgba(255, 255, 255, 1),
  135px 5px 0 0 rgba(255, 255, 255, 1), 140px 5px 0 0 rgba(255, 255, 255, 1),
  15px 10px 0 0 rgba(255, 255, 255, 1), 20px 10px 0 0 rgba(48, 53, 57, 1),
  25px 10px 0 0 rgba(48, 53, 57, 1), 30px 10px 0 0 rgba(48, 53, 57, 1),
  35px 10px 0 0 rgba(48, 53, 57, 1), 40px 10px 0 0 rgba(48, 53, 57, 1),
  45px 10px 0 0 rgba(48, 53, 57, 1), 50px 10px 0 0 rgba(48, 53, 57, 1),
  55px 10px 0 0 rgba(48, 53, 57, 1), 60px 10px 0 0 rgba(48, 53, 57, 1),
  65px 10px 0 0 rgba(48, 53, 57, 1), 70px 10px 0 0 rgba(48, 53, 57, 1),
  75px 10px 0 0 rgba(48, 53, 57, 1), 80px 10px 0 0 rgba(48, 53, 57, 1),
  85px 10px 0 0 rgba(48, 53, 57, 1), 90px 10px 0 0 rgba(48, 53, 57, 1),
  95px 10px 0 0 rgba(48, 53, 57, 1), 100px 10px 0 0 rgba(48, 53, 57, 1),
  105px 10px 0 0 rgba(48, 53, 57, 1), 110px 10px 0 0 rgba(48, 53, 57, 1),
  115px 10px 0 0 rgba(48, 53, 57, 1), 120px 10px 0 0 rgba(48, 53, 57, 1),
  125px 10px 0 0 rgba(48, 53, 57, 1), 130px 10px 0 0 rgba(48, 53, 57, 1),
  135px 10px 0 0 rgba(48, 53, 57, 1), 140px 10px 0 0 rgba(48, 53, 57, 1),
  145px 10px 0 0 rgba(255, 255, 255, 1), 10px 15px 0 0 rgba(255, 255, 255, 1),
  15px 15px 0 0 rgba(48, 53, 57, 1), 20px 15px 0 0 rgba(255, 255, 255, 1),
  25px 15px 0 0 rgba(255, 255, 255, 1), 30px 15px 0 0 rgba(255, 255, 255, 1),
  35px 15px 0 0 rgba(255, 255, 255, 1), 40px 15px 0 0 rgba(255, 255, 255, 1),
  45px 15px 0 0 rgba(255, 255, 255, 1), 50px 15px 0 0 rgba(255, 255, 255, 1),
  55px 15px 0 0 rgba(255, 255, 255, 1), 60px 15px 0 0 rgba(255, 255, 255, 1),
  65px 15px 0 0 rgba(255, 255, 255, 1), 70px 15px 0 0 rgba(255, 255, 255, 1),
  75px 15px 0 0 rgba(255, 255, 255, 1), 80px 15px 0 0 rgba(255, 255, 255, 1),
  85px 15px 0 0 rgba(255, 255, 255, 1), 90px 15px 0 0 rgba(255, 255, 255, 1),
  95px 15px 0 0 rgba(255, 255, 255, 1), 100px 15px 0 0 rgba(255, 255, 255, 1),
  105px 15px 0 0 rgba(255, 255, 255, 1), 110px 15px 0 0 rgba(255, 255, 255, 1),
  115px 15px 0 0 rgba(255, 255, 255, 1), 120px 15px 0 0 rgba(255, 255, 255, 1),
  125px 15px 0 0 rgba(255, 255, 255, 1), 130px 15px 0 0 rgba(255, 255, 255, 1),
  135px 15px 0 0 rgba(255, 255, 255, 1), 140px 15px 0 0 rgba(255, 255, 255, 1),
  145px 15px 0 0 rgba(48, 53, 57, 1), 150px 15px 0 0 rgba(255, 255, 255, 1),
  5px 20px 0 0 rgba(255, 255, 255, 1), 10px 20px 0 0 rgba(48, 53, 57, 1),
  15px 20px 0 0 rgba(255, 255, 255, 1), 20px 20px 0 0 rgba(255, 255, 255, 1),
  25px 20px 0 0 rgba(255, 255, 255, 1), 30px 20px 0 0 rgba(255, 255, 255, 1),
  35px 20px 0 0 rgba(255, 255, 255, 1), 40px 20px 0 0 rgba(255, 255, 255, 1),
  45px 20px 0 0 rgba(255, 255, 255, 1), 50px 20px 0 0 rgba(48, 53, 57, 1),
  55px 20px 0 0 rgba(255, 255, 255, 1), 60px 20px 0 0 rgba(255, 255, 255, 1),
  65px 20px 0 0 rgba(255, 255, 255, 1), 70px 20px 0 0 rgba(255, 255, 255, 1),
  75px 20px 0 0 rgba(48, 53, 57, 1), 80px 20px 0 0 rgba(48, 53, 57, 1),
  85px 20px 0 0 rgba(255, 255, 255, 1), 90px 20px 0 0 rgba(255, 255, 255, 1),
  95px 20px 0 0 rgba(255, 255, 255, 1), 100px 20px 0 0 rgba(48, 53, 57, 1),
  105px 20px 0 0 rgba(48, 53, 57, 1), 110px 20px 0 0 rgba(48, 53, 57, 1),
  115px 20px 0 0 rgba(255, 255, 255, 1), 120px 20px 0 0 rgba(255, 255, 255, 1),
  125px 20px 0 0 rgba(255, 255, 255, 1), 130px 20px 0 0 rgba(255, 255, 255, 1),
  135px 20px 0 0 rgba(255, 255, 255, 1), 140px 20px 0 0 rgba(255, 255, 255, 1),
  145px 20px 0 0 rgba(255, 255, 255, 1), 150px 20px 0 0 rgba(48, 53, 57, 1),
  155px 20px 0 0 rgba(255, 255, 255, 1), 5px 25px 0 0 rgba(255, 255, 255, 1),
  10px 25px 0 0 rgba(48, 53, 57, 1), 15px 25px 0 0 rgba(255, 255, 255, 1),
  20px 25px 0 0 rgba(255, 255, 255, 1), 25px 25px 0 0 rgba(255, 255, 255, 1),
  30px 25px 0 0 rgba(255, 255, 255, 1), 35px 25px 0 0 rgba(255, 255, 255, 1),
  40px 25px 0 0 rgba(255, 255, 255, 1), 45px 25px 0 0 rgba(255, 255, 255, 1),
  50px 25px 0 0 rgba(48, 53, 57, 1), 55px 25px 0 0 rgba(255, 255, 255, 1),
  60px 25px 0 0 rgba(255, 255, 255, 1), 65px 25px 0 0 rgba(255, 255, 255, 1),
  70px 25px 0 0 rgba(48, 53, 57, 1), 75px 25px 0 0 rgba(255, 255, 255, 1),
  80px 25px 0 0 rgba(255, 255, 255, 1), 85px 25px 0 0 rgba(48, 53, 57, 1),
  90px 25px 0 0 rgba(255, 255, 255, 1), 95px 25px 0 0 rgba(48, 53, 57, 1),
  100px 25px 0 0 rgba(255, 255, 255, 1), 105px 25px 0 0 rgba(255, 255, 255, 1),
  110px 25px 0 0 rgba(255, 255, 255, 1), 115px 25px 0 0 rgba(255, 255, 255, 1),
  120px 25px 0 0 rgba(255, 255, 255, 1), 125px 25px 0 0 rgba(255, 255, 255, 1),
  130px 25px 0 0 rgba(255, 255, 255, 1), 135px 25px 0 0 rgba(255, 255, 255, 1),
  140px 25px 0 0 rgba(255, 255, 255, 1), 145px 25px 0 0 rgba(255, 255, 255, 1),
  150px 25px 0 0 rgba(48, 53, 57, 1), 155px 25px 0 0 rgba(255, 255, 255, 1),
  5px 30px 0 0 rgba(255, 255, 255, 1), 10px 30px 0 0 rgba(48, 53, 57, 1),
  15px 30px 0 0 rgba(255, 255, 255, 1), 20px 30px 0 0 rgba(255, 255, 255, 1),
  25px 30px 0 0 rgba(255, 255, 255, 1), 30px 30px 0 0 rgba(255, 255, 255, 1),
  35px 30px 0 0 rgba(255, 255, 255, 1), 40px 30px 0 0 rgba(255, 255, 255, 1),
  45px 30px 0 0 rgba(255, 255, 255, 1), 50px 30px 0 0 rgba(48, 53, 57, 1),
  55px 30px 0 0 rgba(255, 255, 255, 1), 60px 30px 0 0 rgba(255, 255, 255, 1),
  65px 30px 0 0 rgba(255, 255, 255, 1), 70px 30px 0 0 rgba(48, 53, 57, 1),
  75px 30px 0 0 rgba(255, 255, 255, 1), 80px 30px 0 0 rgba(255, 255, 255, 1),
  85px 30px 0 0 rgba(48, 53, 57, 1), 90px 30px 0 0 rgba(255, 255, 255, 1),
  95px 30px 0 0 rgba(48, 53, 57, 1), 100px 30px 0 0 rgba(255, 255, 255, 1),
  105px 30px 0 0 rgba(48, 53, 57, 1), 110px 30px 0 0 rgba(48, 53, 57, 1),
  115px 30px 0 0 rgba(255, 255, 255, 1), 120px 30px 0 0 rgba(255, 255, 255, 1),
  125px 30px 0 0 rgba(255, 255, 255, 1), 130px 30px 0 0 rgba(255, 255, 255, 1),
  135px 30px 0 0 rgba(255, 255, 255, 1), 140px 30px 0 0 rgba(255, 255, 255, 1),
  145px 30px 0 0 rgba(255, 255, 255, 1), 150px 30px 0 0 rgba(48, 53, 57, 1),
  155px 30px 0 0 rgba(255, 255, 255, 1), 5px 35px 0 0 rgba(255, 255, 255, 1),
  10px 35px 0 0 rgba(48, 53, 57, 1), 15px 35px 0 0 rgba(255, 255, 255, 1),
  20px 35px 0 0 rgba(255, 255, 255, 1), 25px 35px 0 0 rgba(255, 255, 255, 1),
  30px 35px 0 0 rgba(255, 255, 255, 1), 35px 35px 0 0 rgba(255, 255, 255, 1),
  40px 35px 0 0 rgba(255, 255, 255, 1), 45px 35px 0 0 rgba(255, 255, 255, 1),
  50px 35px 0 0 rgba(48, 53, 57, 1), 55px 35px 0 0 rgba(255, 255, 255, 1),
  60px 35px 0 0 rgba(255, 255, 255, 1), 65px 35px 0 0 rgba(255, 255, 255, 1),
  70px 35px 0 0 rgba(48, 53, 57, 1), 75px 35px 0 0 rgba(255, 255, 255, 1),
  80px 35px 0 0 rgba(255, 255, 255, 1), 85px 35px 0 0 rgba(48, 53, 57, 1),
  90px 35px 0 0 rgba(255, 255, 255, 1), 95px 35px 0 0 rgba(48, 53, 57, 1),
  100px 35px 0 0 rgba(255, 255, 255, 1), 105px 35px 0 0 rgba(255, 255, 255, 1),
  110px 35px 0 0 rgba(48, 53, 57, 1), 115px 35px 0 0 rgba(255, 255, 255, 1),
  120px 35px 0 0 rgba(255, 255, 255, 1), 125px 35px 0 0 rgba(255, 255, 255, 1),
  130px 35px 0 0 rgba(255, 255, 255, 1), 135px 35px 0 0 rgba(255, 255, 255, 1),
  140px 35px 0 0 rgba(255, 255, 255, 1), 145px 35px 0 0 rgba(255, 255, 255, 1),
  150px 35px 0 0 rgba(48, 53, 57, 1), 155px 35px 0 0 rgba(255, 255, 255, 1),
  5px 40px 0 0 rgba(255, 255, 255, 1), 10px 40px 0 0 rgba(48, 53, 57, 1),
  15px 40px 0 0 rgba(255, 255, 255, 1), 20px 40px 0 0 rgba(255, 255, 255, 1),
  25px 40px 0 0 rgba(255, 255, 255, 1), 30px 40px 0 0 rgba(255, 255, 255, 1),
  35px 40px 0 0 rgba(255, 255, 255, 1), 40px 40px 0 0 rgba(255, 255, 255, 1),
  45px 40px 0 0 rgba(255, 255, 255, 1), 50px 40px 0 0 rgba(48, 53, 57, 1),
  55px 40px 0 0 rgba(48, 53, 57, 1), 60px 40px 0 0 rgba(48, 53, 57, 1),
  65px 40px 0 0 rgba(255, 255, 255, 1), 70px 40px 0 0 rgba(255, 255, 255, 1),
  75px 40px 0 0 rgba(48, 53, 57, 1), 80px 40px 0 0 rgba(48, 53, 57, 1),
  85px 40px 0 0 rgba(255, 255, 255, 1), 90px 40px 0 0 rgba(255, 255, 255, 1),
  95px 40px 0 0 rgba(255, 255, 255, 1), 100px 40px 0 0 rgba(48, 53, 57, 1),
  105px 40px 0 0 rgba(48, 53, 57, 1), 110px 40px 0 0 rgba(48, 53, 57, 1),
  115px 40px 0 0 rgba(255, 255, 255, 1), 120px 40px 0 0 rgba(255, 255, 255, 1),
  125px 40px 0 0 rgba(255, 255, 255, 1), 130px 40px 0 0 rgba(255, 255, 255, 1),
  135px 40px 0 0 rgba(255, 255, 255, 1), 140px 40px 0 0 rgba(255, 255, 255, 1),
  145px 40px 0 0 rgba(255, 255, 255, 1), 150px 40px 0 0 rgba(48, 53, 57, 1),
  155px 40px 0 0 rgba(255, 255, 255, 1), 10px 45px 0 0 rgba(255, 255, 255, 1),
  15px 45px 0 0 rgba(48, 53, 57, 1), 20px 45px 0 0 rgba(255, 255, 255, 1),
  25px 45px 0 0 rgba(255, 255, 255, 1), 30px 45px 0 0 rgba(255, 255, 255, 1),
  35px 45px 0 0 rgba(255, 255, 255, 1), 40px 45px 0 0 rgba(255, 255, 255, 1),
  45px 45px 0 0 rgba(255, 255, 255, 1), 50px 45px 0 0 rgba(255, 255, 255, 1),
  55px 45px 0 0 rgba(255, 255, 255, 1), 60px 45px 0 0 rgba(255, 255, 255, 1),
  65px 45px 0 0 rgba(255, 255, 255, 1), 70px 45px 0 0 rgba(255, 255, 255, 1),
  75px 45px 0 0 rgba(255, 255, 255, 1), 80px 45px 0 0 rgba(255, 255, 255, 1),
  85px 45px 0 0 rgba(255, 255, 255, 1), 90px 45px 0 0 rgba(255, 255, 255, 1),
  95px 45px 0 0 rgba(255, 255, 255, 1), 100px 45px 0 0 rgba(255, 255, 255, 1),
  105px 45px 0 0 rgba(255, 255, 255, 1), 110px 45px 0 0 rgba(255, 255, 255, 1),
  115px 45px 0 0 rgba(255, 255, 255, 1), 120px 45px 0 0 rgba(255, 255, 255, 1),
  125px 45px 0 0 rgba(255, 255, 255, 1), 130px 45px 0 0 rgba(255, 255, 255, 1),
  135px 45px 0 0 rgba(255, 255, 255, 1), 140px 45px 0 0 rgba(255, 255, 255, 1),
  145px 45px 0 0 rgba(48, 53, 57, 1), 150px 45px 0 0 rgba(255, 255, 255, 1),
  15px 50px 0 0 rgba(255, 255, 255, 1), 20px 50px 0 0 rgba(48, 53, 57, 1),
  25px 50px 0 0 rgba(48, 53, 57, 1), 30px 50px 0 0 rgba(48, 53, 57, 1),
  35px 50px 0 0 rgba(48, 53, 57, 1), 40px 50px 0 0 rgba(48, 53, 57, 1),
  45px 50px 0 0 rgba(48, 53, 57, 1), 50px 50px 0 0 rgba(48, 53, 57, 1),
  55px 50px 0 0 rgba(48, 53, 57, 1), 60px 50px 0 0 rgba(48, 53, 57, 1),
  65px 50px 0 0 rgba(48, 53, 57, 1), 70px 50px 0 0 rgba(48, 53, 57, 1),
  75px 50px 0 0 rgba(48, 53, 57, 1), 80px 50px 0 0 rgba(48, 53, 57, 1),
  85px 50px 0 0 rgba(48, 53, 57, 1), 90px 50px 0 0 rgba(48, 53, 57, 1),
  95px 50px 0 0 rgba(48, 53, 57, 1), 100px 50px 0 0 rgba(48, 53, 57, 1),
  105px 50px 0 0 rgba(48, 53, 57, 1), 110px 50px 0 0 rgba(48, 53, 57, 1),
  115px 50px 0 0 rgba(48, 53, 57, 1), 120px 50px 0 0 rgba(48, 53, 57, 1),
  125px 50px 0 0 rgba(48, 53, 57, 1), 130px 50px 0 0 rgba(48, 53, 57, 1),
  135px 50px 0 0 rgba(48, 53, 57, 1), 140px 50px 0 0 rgba(48, 53, 57, 1),
  145px 50px 0 0 rgba(255, 255, 255, 1), 20px 55px 0 0 rgba(255, 255, 255, 1),
  25px 55px 0 0 rgba(255, 255, 255, 1), 30px 55px 0 0 rgba(255, 255, 255, 1),
  35px 55px 0 0 rgba(255, 255, 255, 1), 40px 55px 0 0 rgba(255, 255, 255, 1),
  45px 55px 0 0 rgba(255, 255, 255, 1), 50px 55px 0 0 rgba(255, 255, 255, 1),
  55px 55px 0 0 rgba(255, 255, 255, 1), 60px 55px 0 0 rgba(255, 255, 255, 1),
  65px 55px 0 0 rgba(255, 255, 255, 1), 70px 55px 0 0 rgba(255, 255, 255, 1),
  75px 55px 0 0 rgba(255, 255, 255, 1), 80px 55px 0 0 rgba(255, 255, 255, 1),
  85px 55px 0 0 rgba(255, 255, 255, 1), 90px 55px 0 0 rgba(255, 255, 255, 1),
  95px 55px 0 0 rgba(255, 255, 255, 1), 100px 55px 0 0 rgba(255, 255, 255, 1),
  105px 55px 0 0 rgba(255, 255, 255, 1), 110px 55px 0 0 rgba(255, 255, 255, 1),
  115px 55px 0 0 rgba(255, 255, 255, 1), 120px 55px 0 0 rgba(255, 255, 255, 1),
  125px 55px 0 0 rgba(255, 255, 255, 1), 130px 55px 0 0 rgba(255, 255, 255, 1),
  135px 55px 0 0 rgba(255, 255, 255, 1), 140px 55px 0 0 rgba(255, 255, 255, 1);
 height: 5px;
 width: 5px;
}
.pixelart-to-css-folder {
 box-shadow: 25px 15px 0 0 rgba(255, 255, 255, 1),
  30px 15px 0 0 rgba(255, 255, 255, 1), 35px 15px 0 0 rgba(255, 255, 255, 1),
  40px 15px 0 0 rgba(255, 255, 255, 1), 45px 15px 0 0 rgba(255, 255, 255, 1),
  20px 20px 0 0 rgba(255, 255, 255, 1), 25px 20px 0 0 rgba(48, 53, 56, 1),
  30px 20px 0 0 rgba(48, 53, 56, 1), 35px 20px 0 0 rgba(48, 53, 56, 1),
  40px 20px 0 0 rgba(48, 53, 56, 1), 45px 20px 0 0 rgba(48, 53, 56, 1),
  50px 20px 0 0 rgba(255, 255, 255, 1), 15px 25px 0 0 rgba(255, 255, 255, 1),
  20px 25px 0 0 rgba(48, 53, 56, 1), 25px 25px 0 0 rgba(183, 96, 154, 1),
  30px 25px 0 0 rgba(183, 96, 154, 1), 35px 25px 0 0 rgba(183, 96, 154, 1),
  40px 25px 0 0 rgba(183, 96, 154, 1), 45px 25px 0 0 rgba(183, 96, 154, 1),
  50px 25px 0 0 rgba(48, 53, 56, 1), 55px 25px 0 0 rgba(255, 255, 255, 1),
  60px 25px 0 0 rgba(255, 255, 255, 1), 65px 25px 0 0 rgba(255, 255, 255, 1),
  70px 25px 0 0 rgba(255, 255, 255, 1), 75px 25px 0 0 rgba(255, 255, 255, 1),
  80px 25px 0 0 rgba(255, 255, 255, 1), 15px 30px 0 0 rgba(255, 255, 255, 1),
  20px 30px 0 0 rgba(48, 53, 56, 1), 25px 30px 0 0 rgba(183, 96, 154, 1),
  30px 30px 0 0 rgba(183, 96, 154, 1), 35px 30px 0 0 rgba(183, 96, 154, 1),
  40px 30px 0 0 rgba(183, 96, 154, 1), 45px 30px 0 0 rgba(183, 96, 154, 1),
  50px 30px 0 0 rgba(183, 96, 154, 1), 55px 30px 0 0 rgba(48, 53, 56, 1),
  60px 30px 0 0 rgba(48, 53, 56, 1), 65px 30px 0 0 rgba(48, 53, 56, 1),
  70px 30px 0 0 rgba(48, 53, 56, 1), 75px 30px 0 0 rgba(48, 53, 56, 1),
  80px 30px 0 0 rgba(48, 53, 56, 1), 85px 30px 0 0 rgba(255, 255, 255, 1),
  15px 35px 0 0 rgba(255, 255, 255, 1), 20px 35px 0 0 rgba(48, 53, 56, 1),
  25px 35px 0 0 rgba(183, 96, 154, 1), 30px 35px 0 0 rgba(183, 96, 154, 1),
  35px 35px 0 0 rgba(183, 96, 154, 1), 40px 35px 0 0 rgba(183, 96, 154, 1),
  45px 35px 0 0 rgba(183, 96, 154, 1), 50px 35px 0 0 rgba(183, 96, 154, 1),
  55px 35px 0 0 rgba(183, 96, 154, 1), 60px 35px 0 0 rgba(183, 96, 154, 1),
  65px 35px 0 0 rgba(183, 96, 154, 1), 70px 35px 0 0 rgba(183, 96, 154, 1),
  75px 35px 0 0 rgba(183, 96, 154, 1), 80px 35px 0 0 rgba(183, 96, 154, 1),
  85px 35px 0 0 rgba(48, 53, 56, 1), 90px 35px 0 0 rgba(255, 255, 255, 1),
  95px 35px 0 0 rgba(255, 255, 255, 1), 15px 40px 0 0 rgba(255, 255, 255, 1),
  20px 40px 0 0 rgba(48, 53, 56, 1), 25px 40px 0 0 rgba(183, 96, 154, 1),
  30px 40px 0 0 rgba(183, 96, 154, 1), 35px 40px 0 0 rgba(183, 96, 154, 1),
  40px 40px 0 0 rgba(183, 96, 154, 1), 45px 40px 0 0 rgba(48, 53, 56, 1),
  50px 40px 0 0 rgba(48, 53, 56, 1), 55px 40px 0 0 rgba(48, 53, 56, 1),
  60px 40px 0 0 rgba(48, 53, 56, 1), 65px 40px 0 0 rgba(48, 53, 56, 1),
  70px 40px 0 0 rgba(48, 53, 56, 1), 75px 40px 0 0 rgba(48, 53, 56, 1),
  80px 40px 0 0 rgba(48, 53, 56, 1), 85px 40px 0 0 rgba(48, 53, 56, 1),
  90px 40px 0 0 rgba(48, 53, 56, 1), 95px 40px 0 0 rgba(48, 53, 56, 1),
  100px 40px 0 0 rgba(255, 255, 255, 1), 15px 45px 0 0 rgba(255, 255, 255, 1),
  20px 45px 0 0 rgba(48, 53, 56, 1), 25px 45px 0 0 rgba(183, 96, 154, 1),
  30px 45px 0 0 rgba(183, 96, 154, 1), 35px 45px 0 0 rgba(183, 96, 154, 1),
  40px 45px 0 0 rgba(48, 53, 56, 1), 45px 45px 0 0 rgba(252, 200, 117, 1),
  50px 45px 0 0 rgba(252, 200, 117, 1), 55px 45px 0 0 rgba(252, 200, 117, 1),
  60px 45px 0 0 rgba(252, 200, 117, 1), 65px 45px 0 0 rgba(252, 200, 117, 1),
  70px 45px 0 0 rgba(252, 200, 117, 1), 75px 45px 0 0 rgba(252, 200, 117, 1),
  80px 45px 0 0 rgba(252, 200, 117, 1), 85px 45px 0 0 rgba(252, 200, 117, 1),
  90px 45px 0 0 rgba(252, 200, 117, 1), 95px 45px 0 0 rgba(48, 53, 56, 1),
  100px 45px 0 0 rgba(255, 255, 255, 1), 15px 50px 0 0 rgba(255, 255, 255, 1),
  20px 50px 0 0 rgba(48, 53, 56, 1), 25px 50px 0 0 rgba(183, 96, 154, 1),
  30px 50px 0 0 rgba(183, 96, 154, 1), 35px 50px 0 0 rgba(183, 96, 154, 1),
  40px 50px 0 0 rgba(48, 53, 56, 1), 45px 50px 0 0 rgba(252, 200, 117, 1),
  50px 50px 0 0 rgba(252, 200, 117, 1), 55px 50px 0 0 rgba(252, 200, 117, 1),
  60px 50px 0 0 rgba(252, 200, 117, 1), 65px 50px 0 0 rgba(252, 200, 117, 1),
  70px 50px 0 0 rgba(252, 200, 117, 1), 75px 50px 0 0 rgba(252, 200, 117, 1),
  80px 50px 0 0 rgba(252, 200, 117, 1), 85px 50px 0 0 rgba(252, 200, 117, 1),
  90px 50px 0 0 rgba(48, 53, 56, 1), 95px 50px 0 0 rgba(255, 255, 255, 1),
  15px 55px 0 0 rgba(255, 255, 255, 1), 20px 55px 0 0 rgba(48, 53, 56, 1),
  25px 55px 0 0 rgba(183, 96, 154, 1), 30px 55px 0 0 rgba(183, 96, 154, 1),
  35px 55px 0 0 rgba(48, 53, 56, 1), 40px 55px 0 0 rgba(252, 200, 117, 1),
  45px 55px 0 0 rgba(252, 200, 117, 1), 50px 55px 0 0 rgba(252, 200, 117, 1),
  55px 55px 0 0 rgba(252, 200, 117, 1), 60px 55px 0 0 rgba(252, 200, 117, 1),
  65px 55px 0 0 rgba(252, 200, 117, 1), 70px 55px 0 0 rgba(252, 200, 117, 1),
  75px 55px 0 0 rgba(252, 200, 117, 1), 80px 55px 0 0 rgba(252, 200, 117, 1),
  85px 55px 0 0 rgba(252, 200, 117, 1), 90px 55px 0 0 rgba(48, 53, 56, 1),
  95px 55px 0 0 rgba(255, 255, 255, 1), 15px 60px 0 0 rgba(255, 255, 255, 1),
  20px 60px 0 0 rgba(48, 53, 56, 1), 25px 60px 0 0 rgba(183, 96, 154, 1),
  30px 60px 0 0 rgba(183, 96, 154, 1), 35px 60px 0 0 rgba(48, 53, 56, 1),
  40px 60px 0 0 rgba(252, 200, 117, 1), 45px 60px 0 0 rgba(252, 200, 117, 1),
  50px 60px 0 0 rgba(252, 200, 117, 1), 55px 60px 0 0 rgba(252, 200, 117, 1),
  60px 60px 0 0 rgba(252, 200, 117, 1), 65px 60px 0 0 rgba(252, 200, 117, 1),
  70px 60px 0 0 rgba(252, 200, 117, 1), 75px 60px 0 0 rgba(252, 200, 117, 1),
  80px 60px 0 0 rgba(252, 200, 117, 1), 85px 60px 0 0 rgba(48, 53, 56, 1),
  90px 60px 0 0 rgba(255, 255, 255, 1), 15px 65px 0 0 rgba(255, 255, 255, 1),
  20px 65px 0 0 rgba(48, 53, 56, 1), 25px 65px 0 0 rgba(183, 96, 154, 1),
  30px 65px 0 0 rgba(48, 53, 56, 1), 35px 65px 0 0 rgba(252, 200, 117, 1),
  40px 65px 0 0 rgba(252, 200, 117, 1), 45px 65px 0 0 rgba(252, 200, 117, 1),
  50px 65px 0 0 rgba(252, 200, 117, 1), 55px 65px 0 0 rgba(252, 200, 117, 1),
  60px 65px 0 0 rgba(252, 200, 117, 1), 65px 65px 0 0 rgba(252, 200, 117, 1),
  70px 65px 0 0 rgba(252, 200, 117, 1), 75px 65px 0 0 rgba(252, 200, 117, 1),
  80px 65px 0 0 rgba(252, 200, 117, 1), 85px 65px 0 0 rgba(48, 53, 56, 1),
  90px 65px 0 0 rgba(255, 255, 255, 1), 15px 70px 0 0 rgba(255, 255, 255, 1),
  20px 70px 0 0 rgba(48, 53, 56, 1), 25px 70px 0 0 rgba(183, 96, 154, 1),
  30px 70px 0 0 rgba(48, 53, 56, 1), 35px 70px 0 0 rgba(252, 200, 117, 1),
  40px 70px 0 0 rgba(252, 200, 117, 1), 45px 70px 0 0 rgba(252, 200, 117, 1),
  50px 70px 0 0 rgba(252, 200, 117, 1), 55px 70px 0 0 rgba(252, 200, 117, 1),
  60px 70px 0 0 rgba(252, 200, 117, 1), 65px 70px 0 0 rgba(252, 200, 117, 1),
  70px 70px 0 0 rgba(252, 200, 117, 1), 75px 70px 0 0 rgba(252, 200, 117, 1),
  80px 70px 0 0 rgba(48, 53, 56, 1), 85px 70px 0 0 rgba(255, 255, 255, 1),
  15px 75px 0 0 rgba(255, 255, 255, 1), 20px 75px 0 0 rgba(48, 53, 56, 1),
  25px 75px 0 0 rgba(183, 96, 154, 1), 30px 75px 0 0 rgba(48, 53, 56, 1),
  35px 75px 0 0 rgba(252, 200, 117, 1), 40px 75px 0 0 rgba(252, 200, 117, 1),
  45px 75px 0 0 rgba(252, 200, 117, 1), 50px 75px 0 0 rgba(252, 200, 117, 1),
  55px 75px 0 0 rgba(252, 200, 117, 1), 60px 75px 0 0 rgba(252, 200, 117, 1),
  65px 75px 0 0 rgba(252, 200, 117, 1), 70px 75px 0 0 rgba(252, 200, 117, 1),
  75px 75px 0 0 rgba(252, 200, 117, 1), 80px 75px 0 0 rgba(48, 53, 56, 1),
  85px 75px 0 0 rgba(255, 255, 255, 1), 20px 80px 0 0 rgba(255, 255, 255, 1),
  25px 80px 0 0 rgba(48, 53, 56, 1), 30px 80px 0 0 rgba(48, 53, 56, 1),
  35px 80px 0 0 rgba(48, 53, 56, 1), 40px 80px 0 0 rgba(48, 53, 56, 1),
  45px 80px 0 0 rgba(48, 53, 56, 1), 50px 80px 0 0 rgba(48, 53, 56, 1),
  55px 80px 0 0 rgba(48, 53, 56, 1), 60px 80px 0 0 rgba(48, 53, 56, 1),
  65px 80px 0 0 rgba(48, 53, 56, 1), 70px 80px 0 0 rgba(48, 53, 56, 1),
  75px 80px 0 0 rgba(48, 53, 56, 1), 80px 80px 0 0 rgba(255, 255, 255, 1),
  25px 85px 0 0 rgba(255, 255, 255, 1), 30px 85px 0 0 rgba(255, 255, 255, 1),
  35px 85px 0 0 rgba(255, 255, 255, 1), 40px 85px 0 0 rgba(255, 255, 255, 1),
  45px 85px 0 0 rgba(255, 255, 255, 1), 50px 85px 0 0 rgba(255, 255, 255, 1),
  55px 85px 0 0 rgba(255, 255, 255, 1), 60px 85px 0 0 rgba(255, 255, 255, 1),
  65px 85px 0 0 rgba(255, 255, 255, 1), 70px 85px 0 0 rgba(255, 255, 255, 1),
  75px 85px 0 0 rgba(255, 255, 255, 1);
 height: 5px;
 width: 5px;
}
.pixelart-to-css-static2 {
 box-shadow: 50px 10px 0 0 rgba(255, 255, 255, 1),
  50px 30px 0 0 rgba(255, 255, 255, 1), 50px 50px 0 0 rgba(255, 255, 255, 1),
  50px 70px 0 0 rgba(255, 255, 255, 1), 50px 90px 0 0 rgba(255, 255, 255, 1),
  50px 110px 0 0 rgba(255, 255, 255, 1), 50px 130px 0 0 rgba(255, 255, 255, 1),
  50px 150px 0 0 rgba(255, 255, 255, 1), 50px 170px 0 0 rgba(255, 255, 255, 1),
  50px 190px 0 0 rgba(255, 255, 255, 1), 50px 210px 0 0 rgba(255, 255, 255, 1),
  50px 230px 0 0 rgba(255, 255, 255, 1);
 height: 10px;
 width: 10px;
}
.pixelart-to-css {
 box-shadow: 20px 5px 0 0 rgba(203, 109, 181, 1),
  25px 5px 0 0 rgba(203, 109, 181, 1), 30px 5px 0 0 rgba(203, 109, 181, 1),
  35px 5px 0 0 rgba(203, 109, 181, 1), 40px 5px 0 0 rgba(203, 109, 181, 1),
  45px 5px 0 0 rgba(203, 109, 181, 1), 50px 5px 0 0 rgba(203, 109, 181, 1),
  55px 5px 0 0 rgba(203, 109, 181, 1), 60px 5px 0 0 rgba(203, 109, 181, 1),
  65px 5px 0 0 rgba(203, 109, 181, 1), 70px 5px 0 0 rgba(203, 109, 181, 1),
  75px 5px 0 0 rgba(203, 109, 181, 1), 80px 5px 0 0 rgba(203, 109, 181, 1),
  85px 5px 0 0 rgba(203, 109, 181, 1), 90px 5px 0 0 rgba(203, 109, 181, 1),
  95px 5px 0 0 rgba(203, 109, 181, 1), 100px 5px 0 0 rgba(203, 109, 181, 1),
  105px 5px 0 0 rgba(203, 109, 181, 1), 110px 5px 0 0 rgba(203, 109, 181, 1),
  115px 5px 0 0 rgba(203, 109, 181, 1), 120px 5px 0 0 rgba(203, 109, 181, 1),
  125px 5px 0 0 rgba(203, 109, 181, 1), 130px 5px 0 0 rgba(203, 109, 181, 1),
  135px 5px 0 0 rgba(203, 109, 181, 1), 140px 5px 0 0 rgba(203, 109, 181, 1),
  145px 5px 0 0 rgba(203, 109, 181, 1), 150px 5px 0 0 rgba(203, 109, 181, 1),
  155px 5px 0 0 rgba(203, 109, 181, 1), 160px 5px 0 0 rgba(203, 109, 181, 1),
  165px 5px 0 0 rgba(203, 109, 181, 1), 170px 5px 0 0 rgba(203, 109, 181, 1),
  175px 5px 0 0 rgba(203, 109, 181, 1), 180px 5px 0 0 rgba(203, 109, 181, 1),
  185px 5px 0 0 rgba(203, 109, 181, 1), 190px 5px 0 0 rgba(203, 109, 181, 1),
  195px 5px 0 0 rgba(203, 109, 181, 1), 200px 5px 0 0 rgba(203, 109, 181, 1),
  205px 5px 0 0 rgba(203, 109, 181, 1), 210px 5px 0 0 rgba(203, 109, 181, 1),
  215px 5px 0 0 rgba(203, 109, 181, 1), 220px 5px 0 0 rgba(203, 109, 181, 1),
  225px 5px 0 0 rgba(203, 109, 181, 1), 230px 5px 0 0 rgba(203, 109, 181, 1),
  235px 5px 0 0 rgba(203, 109, 181, 1), 240px 5px 0 0 rgba(203, 109, 181, 1),
  245px 5px 0 0 rgba(203, 109, 181, 1), 250px 5px 0 0 rgba(203, 109, 181, 1),
  255px 5px 0 0 rgba(203, 109, 181, 1), 260px 5px 0 0 rgba(203, 109, 181, 1),
  265px 5px 0 0 rgba(203, 109, 181, 1), 270px 5px 0 0 rgba(203, 109, 181, 1),
  275px 5px 0 0 rgba(203, 109, 181, 1), 280px 5px 0 0 rgba(203, 109, 181, 1),
  285px 5px 0 0 rgba(203, 109, 181, 1), 290px 5px 0 0 rgba(203, 109, 181, 1),
  295px 5px 0 0 rgba(203, 109, 181, 1), 300px 5px 0 0 rgba(203, 109, 181, 1),
  305px 5px 0 0 rgba(203, 109, 181, 1), 310px 5px 0 0 rgba(203, 109, 181, 1),
  315px 5px 0 0 rgba(203, 109, 181, 1), 320px 5px 0 0 rgba(203, 109, 181, 1),
  325px 5px 0 0 rgba(203, 109, 181, 1), 330px 5px 0 0 rgba(203, 109, 181, 1),
  335px 5px 0 0 rgba(203, 109, 181, 1), 340px 5px 0 0 rgba(203, 109, 181, 1),
  345px 5px 0 0 rgba(203, 109, 181, 1), 350px 5px 0 0 rgba(203, 109, 181, 1),
  355px 5px 0 0 rgba(203, 109, 181, 1), 360px 5px 0 0 rgba(203, 109, 181, 1),
  365px 5px 0 0 rgba(203, 109, 181, 1), 370px 5px 0 0 rgba(203, 109, 181, 1),
  375px 5px 0 0 rgba(203, 109, 181, 1), 380px 5px 0 0 rgba(203, 109, 181, 1),
  385px 5px 0 0 rgba(203, 109, 181, 1), 390px 5px 0 0 rgba(203, 109, 181, 1),
  395px 5px 0 0 rgba(203, 109, 181, 1), 400px 5px 0 0 rgba(203, 109, 181, 1),
  405px 5px 0 0 rgba(203, 109, 181, 1), 410px 5px 0 0 rgba(203, 109, 181, 1),
  415px 5px 0 0 rgba(203, 109, 181, 1), 420px 5px 0 0 rgba(203, 109, 181, 1),
  425px 5px 0 0 rgba(203, 109, 181, 1), 430px 5px 0 0 rgba(203, 109, 181, 1),
  435px 5px 0 0 rgba(203, 109, 181, 1), 440px 5px 0 0 rgba(203, 109, 181, 1),
  445px 5px 0 0 rgba(203, 109, 181, 1), 450px 5px 0 0 rgba(203, 109, 181, 1),
  455px 5px 0 0 rgba(203, 109, 181, 1), 460px 5px 0 0 rgba(203, 109, 181, 1),
  465px 5px 0 0 rgba(203, 109, 181, 1), 470px 5px 0 0 rgba(203, 109, 181, 1),
  475px 5px 0 0 rgba(203, 109, 181, 1), 480px 5px 0 0 rgba(203, 109, 181, 1),
  485px 5px 0 0 rgba(203, 109, 181, 1), 490px 5px 0 0 rgba(203, 109, 181, 1),
  495px 5px 0 0 rgba(203, 109, 181, 1), 500px 5px 0 0 rgba(203, 109, 181, 1),
  505px 5px 0 0 rgba(203, 109, 181, 1), 510px 5px 0 0 rgba(203, 109, 181, 1),
  515px 5px 0 0 rgba(203, 109, 181, 1), 520px 5px 0 0 rgba(203, 109, 181, 1),
  525px 5px 0 0 rgba(203, 109, 181, 1), 530px 5px 0 0 rgba(203, 109, 181, 1),
  535px 5px 0 0 rgba(203, 109, 181, 1), 540px 5px 0 0 rgba(203, 109, 181, 1),
  545px 5px 0 0 rgba(203, 109, 181, 1), 550px 5px 0 0 rgba(203, 109, 181, 1),
  555px 5px 0 0 rgba(203, 109, 181, 1), 560px 5px 0 0 rgba(203, 109, 181, 1),
  565px 5px 0 0 rgba(203, 109, 181, 1), 570px 5px 0 0 rgba(203, 109, 181, 1),
  575px 5px 0 0 rgba(203, 109, 181, 1), 580px 5px 0 0 rgba(203, 109, 181, 1),
  585px 5px 0 0 rgba(203, 109, 181, 1), 590px 5px 0 0 rgba(203, 109, 181, 1),
  595px 5px 0 0 rgba(203, 109, 181, 1), 600px 5px 0 0 rgba(203, 109, 181, 1),
  605px 5px 0 0 rgba(203, 109, 181, 1), 610px 5px 0 0 rgba(203, 109, 181, 1),
  615px 5px 0 0 rgba(203, 109, 181, 1), 620px 5px 0 0 rgba(203, 109, 181, 1),
  625px 5px 0 0 rgba(203, 109, 181, 1), 630px 5px 0 0 rgba(203, 109, 181, 1),
  635px 5px 0 0 rgba(203, 109, 181, 1), 640px 5px 0 0 rgba(203, 109, 181, 1),
  645px 5px 0 0 rgba(203, 109, 181, 1), 650px 5px 0 0 rgba(203, 109, 181, 1),
  655px 5px 0 0 rgba(203, 109, 181, 1), 660px 5px 0 0 rgba(203, 109, 181, 1),
  665px 5px 0 0 rgba(203, 109, 181, 1), 670px 5px 0 0 rgba(203, 109, 181, 1),
  675px 5px 0 0 rgba(203, 109, 181, 1), 680px 5px 0 0 rgba(203, 109, 181, 1),
  685px 5px 0 0 rgba(203, 109, 181, 1), 690px 5px 0 0 rgba(203, 109, 181, 1),
  15px 10px 0 0 rgba(203, 109, 181, 1), 20px 10px 0 0 rgba(252, 231, 243, 1),
  25px 10px 0 0 rgba(252, 231, 243, 1), 30px 10px 0 0 rgba(252, 231, 243, 1),
  35px 10px 0 0 rgba(252, 231, 243, 1), 40px 10px 0 0 rgba(252, 231, 243, 1),
  45px 10px 0 0 rgba(252, 231, 243, 1), 50px 10px 0 0 rgba(252, 231, 243, 1),
  55px 10px 0 0 rgba(252, 231, 243, 1), 60px 10px 0 0 rgba(252, 231, 243, 1),
  65px 10px 0 0 rgba(252, 231, 243, 1), 70px 10px 0 0 rgba(252, 231, 243, 1),
  75px 10px 0 0 rgba(252, 231, 243, 1), 80px 10px 0 0 rgba(252, 231, 243, 1),
  85px 10px 0 0 rgba(252, 231, 243, 1), 90px 10px 0 0 rgba(252, 231, 243, 1),
  95px 10px 0 0 rgba(252, 231, 243, 1), 100px 10px 0 0 rgba(252, 231, 243, 1),
  105px 10px 0 0 rgba(252, 231, 243, 1), 110px 10px 0 0 rgba(252, 231, 243, 1),
  115px 10px 0 0 rgba(252, 231, 243, 1), 120px 10px 0 0 rgba(252, 231, 243, 1),
  125px 10px 0 0 rgba(252, 231, 243, 1), 130px 10px 0 0 rgba(252, 231, 243, 1),
  135px 10px 0 0 rgba(252, 231, 243, 1), 140px 10px 0 0 rgba(252, 231, 243, 1),
  145px 10px 0 0 rgba(252, 231, 243, 1), 150px 10px 0 0 rgba(252, 231, 243, 1),
  155px 10px 0 0 rgba(252, 231, 243, 1), 160px 10px 0 0 rgba(252, 231, 243, 1),
  165px 10px 0 0 rgba(252, 231, 243, 1), 170px 10px 0 0 rgba(252, 231, 243, 1),
  175px 10px 0 0 rgba(252, 231, 243, 1), 180px 10px 0 0 rgba(252, 231, 243, 1),
  185px 10px 0 0 rgba(252, 231, 243, 1), 190px 10px 0 0 rgba(252, 231, 243, 1),
  195px 10px 0 0 rgba(252, 231, 243, 1), 200px 10px 0 0 rgba(252, 231, 243, 1),
  205px 10px 0 0 rgba(252, 231, 243, 1), 210px 10px 0 0 rgba(252, 231, 243, 1),
  215px 10px 0 0 rgba(252, 231, 243, 1), 220px 10px 0 0 rgba(252, 231, 243, 1),
  225px 10px 0 0 rgba(252, 231, 243, 1), 230px 10px 0 0 rgba(252, 231, 243, 1),
  235px 10px 0 0 rgba(252, 231, 243, 1), 240px 10px 0 0 rgba(252, 231, 243, 1),
  245px 10px 0 0 rgba(252, 231, 243, 1), 250px 10px 0 0 rgba(252, 231, 243, 1),
  255px 10px 0 0 rgba(252, 231, 243, 1), 260px 10px 0 0 rgba(252, 231, 243, 1),
  265px 10px 0 0 rgba(252, 231, 243, 1), 270px 10px 0 0 rgba(252, 231, 243, 1),
  275px 10px 0 0 rgba(252, 231, 243, 1), 280px 10px 0 0 rgba(252, 231, 243, 1),
  285px 10px 0 0 rgba(252, 231, 243, 1), 290px 10px 0 0 rgba(252, 231, 243, 1),
  295px 10px 0 0 rgba(252, 231, 243, 1), 300px 10px 0 0 rgba(252, 231, 243, 1),
  305px 10px 0 0 rgba(252, 231, 243, 1), 310px 10px 0 0 rgba(252, 231, 243, 1),
  315px 10px 0 0 rgba(252, 231, 243, 1), 320px 10px 0 0 rgba(252, 231, 243, 1),
  325px 10px 0 0 rgba(252, 231, 243, 1), 330px 10px 0 0 rgba(252, 231, 243, 1),
  335px 10px 0 0 rgba(252, 231, 243, 1), 340px 10px 0 0 rgba(252, 231, 243, 1),
  345px 10px 0 0 rgba(252, 231, 243, 1), 350px 10px 0 0 rgba(252, 231, 243, 1),
  355px 10px 0 0 rgba(252, 231, 243, 1), 360px 10px 0 0 rgba(252, 231, 243, 1),
  365px 10px 0 0 rgba(252, 231, 243, 1), 370px 10px 0 0 rgba(252, 231, 243, 1),
  375px 10px 0 0 rgba(252, 231, 243, 1), 380px 10px 0 0 rgba(252, 231, 243, 1),
  385px 10px 0 0 rgba(252, 231, 243, 1), 390px 10px 0 0 rgba(252, 231, 243, 1),
  395px 10px 0 0 rgba(252, 231, 243, 1), 400px 10px 0 0 rgba(252, 231, 243, 1),
  405px 10px 0 0 rgba(252, 231, 243, 1), 410px 10px 0 0 rgba(252, 231, 243, 1),
  415px 10px 0 0 rgba(252, 231, 243, 1), 420px 10px 0 0 rgba(252, 231, 243, 1),
  425px 10px 0 0 rgba(252, 231, 243, 1), 430px 10px 0 0 rgba(252, 231, 243, 1),
  435px 10px 0 0 rgba(252, 231, 243, 1), 440px 10px 0 0 rgba(252, 231, 243, 1),
  445px 10px 0 0 rgba(252, 231, 243, 1), 450px 10px 0 0 rgba(252, 231, 243, 1),
  455px 10px 0 0 rgba(252, 231, 243, 1), 460px 10px 0 0 rgba(252, 231, 243, 1),
  465px 10px 0 0 rgba(252, 231, 243, 1), 470px 10px 0 0 rgba(252, 231, 243, 1),
  475px 10px 0 0 rgba(252, 231, 243, 1), 480px 10px 0 0 rgba(252, 231, 243, 1),
  485px 10px 0 0 rgba(252, 231, 243, 1), 490px 10px 0 0 rgba(252, 231, 243, 1),
  495px 10px 0 0 rgba(252, 231, 243, 1), 500px 10px 0 0 rgba(252, 231, 243, 1),
  505px 10px 0 0 rgba(252, 231, 243, 1), 510px 10px 0 0 rgba(252, 231, 243, 1),
  515px 10px 0 0 rgba(252, 231, 243, 1), 520px 10px 0 0 rgba(252, 231, 243, 1),
  525px 10px 0 0 rgba(252, 231, 243, 1), 530px 10px 0 0 rgba(252, 231, 243, 1),
  535px 10px 0 0 rgba(252, 231, 243, 1), 540px 10px 0 0 rgba(252, 231, 243, 1),
  545px 10px 0 0 rgba(252, 231, 243, 1), 550px 10px 0 0 rgba(252, 231, 243, 1),
  555px 10px 0 0 rgba(252, 231, 243, 1), 560px 10px 0 0 rgba(252, 231, 243, 1),
  565px 10px 0 0 rgba(252, 231, 243, 1), 570px 10px 0 0 rgba(252, 231, 243, 1),
  575px 10px 0 0 rgba(252, 231, 243, 1), 580px 10px 0 0 rgba(252, 231, 243, 1),
  585px 10px 0 0 rgba(252, 231, 243, 1), 590px 10px 0 0 rgba(252, 231, 243, 1),
  595px 10px 0 0 rgba(252, 231, 243, 1), 600px 10px 0 0 rgba(252, 231, 243, 1),
  605px 10px 0 0 rgba(252, 231, 243, 1), 610px 10px 0 0 rgba(252, 231, 243, 1),
  615px 10px 0 0 rgba(252, 231, 243, 1), 620px 10px 0 0 rgba(252, 231, 243, 1),
  625px 10px 0 0 rgba(252, 231, 243, 1), 630px 10px 0 0 rgba(252, 231, 243, 1),
  635px 10px 0 0 rgba(252, 231, 243, 1), 640px 10px 0 0 rgba(252, 231, 243, 1),
  645px 10px 0 0 rgba(252, 231, 243, 1), 650px 10px 0 0 rgba(252, 231, 243, 1),
  655px 10px 0 0 rgba(252, 231, 243, 1), 660px 10px 0 0 rgba(252, 231, 243, 1),
  665px 10px 0 0 rgba(252, 231, 243, 1), 670px 10px 0 0 rgba(252, 231, 243, 1),
  675px 10px 0 0 rgba(252, 231, 243, 1), 680px 10px 0 0 rgba(252, 231, 243, 1),
  685px 10px 0 0 rgba(252, 231, 243, 1), 690px 10px 0 0 rgba(252, 231, 243, 1),
  695px 10px 0 0 rgba(203, 109, 181, 1), 10px 15px 0 0 rgba(203, 109, 181, 1),
  15px 15px 0 0 rgba(252, 231, 243, 1), 20px 15px 0 0 rgba(255, 205, 234, 1),
  25px 15px 0 0 rgba(255, 205, 234, 1), 30px 15px 0 0 rgba(255, 205, 234, 1),
  35px 15px 0 0 rgba(255, 205, 234, 1), 40px 15px 0 0 rgba(255, 205, 234, 1),
  45px 15px 0 0 rgba(255, 205, 234, 1), 50px 15px 0 0 rgba(255, 205, 234, 1),
  55px 15px 0 0 rgba(255, 205, 234, 1), 60px 15px 0 0 rgba(255, 205, 234, 1),
  65px 15px 0 0 rgba(255, 205, 234, 1), 70px 15px 0 0 rgba(255, 205, 234, 1),
  75px 15px 0 0 rgba(255, 205, 234, 1), 80px 15px 0 0 rgba(255, 205, 234, 1),
  85px 15px 0 0 rgba(255, 205, 234, 1), 90px 15px 0 0 rgba(255, 205, 234, 1),
  95px 15px 0 0 rgba(255, 205, 234, 1), 100px 15px 0 0 rgba(255, 205, 234, 1),
  105px 15px 0 0 rgba(255, 205, 234, 1), 110px 15px 0 0 rgba(255, 205, 234, 1),
  115px 15px 0 0 rgba(255, 205, 234, 1), 120px 15px 0 0 rgba(255, 205, 234, 1),
  125px 15px 0 0 rgba(255, 205, 234, 1), 130px 15px 0 0 rgba(255, 205, 234, 1),
  135px 15px 0 0 rgba(255, 205, 234, 1), 140px 15px 0 0 rgba(255, 205, 234, 1),
  145px 15px 0 0 rgba(255, 205, 234, 1), 150px 15px 0 0 rgba(255, 205, 234, 1),
  155px 15px 0 0 rgba(255, 205, 234, 1), 160px 15px 0 0 rgba(255, 205, 234, 1),
  165px 15px 0 0 rgba(255, 205, 234, 1), 170px 15px 0 0 rgba(255, 205, 234, 1),
  175px 15px 0 0 rgba(255, 205, 234, 1), 180px 15px 0 0 rgba(255, 205, 234, 1),
  185px 15px 0 0 rgba(255, 205, 234, 1), 190px 15px 0 0 rgba(255, 205, 234, 1),
  195px 15px 0 0 rgba(255, 205, 234, 1), 200px 15px 0 0 rgba(255, 205, 234, 1),
  205px 15px 0 0 rgba(255, 205, 234, 1), 210px 15px 0 0 rgba(255, 205, 234, 1),
  215px 15px 0 0 rgba(255, 205, 234, 1), 220px 15px 0 0 rgba(255, 205, 234, 1),
  225px 15px 0 0 rgba(255, 205, 234, 1), 230px 15px 0 0 rgba(255, 205, 234, 1),
  235px 15px 0 0 rgba(255, 205, 234, 1), 240px 15px 0 0 rgba(255, 205, 234, 1),
  245px 15px 0 0 rgba(255, 205, 234, 1), 250px 15px 0 0 rgba(255, 205, 234, 1),
  255px 15px 0 0 rgba(255, 205, 234, 1), 260px 15px 0 0 rgba(255, 205, 234, 1),
  265px 15px 0 0 rgba(255, 205, 234, 1), 270px 15px 0 0 rgba(255, 205, 234, 1),
  275px 15px 0 0 rgba(255, 205, 234, 1), 280px 15px 0 0 rgba(255, 205, 234, 1),
  285px 15px 0 0 rgba(255, 205, 234, 1), 290px 15px 0 0 rgba(255, 205, 234, 1),
  295px 15px 0 0 rgba(255, 205, 234, 1), 300px 15px 0 0 rgba(255, 205, 234, 1),
  305px 15px 0 0 rgba(255, 205, 234, 1), 310px 15px 0 0 rgba(255, 205, 234, 1),
  315px 15px 0 0 rgba(255, 205, 234, 1), 320px 15px 0 0 rgba(255, 205, 234, 1),
  325px 15px 0 0 rgba(255, 205, 234, 1), 330px 15px 0 0 rgba(255, 205, 234, 1),
  335px 15px 0 0 rgba(255, 205, 234, 1), 340px 15px 0 0 rgba(255, 205, 234, 1),
  345px 15px 0 0 rgba(255, 205, 234, 1), 350px 15px 0 0 rgba(255, 205, 234, 1),
  355px 15px 0 0 rgba(255, 205, 234, 1), 360px 15px 0 0 rgba(255, 205, 234, 1),
  365px 15px 0 0 rgba(255, 205, 234, 1), 370px 15px 0 0 rgba(255, 205, 234, 1),
  375px 15px 0 0 rgba(255, 205, 234, 1), 380px 15px 0 0 rgba(255, 205, 234, 1),
  385px 15px 0 0 rgba(255, 205, 234, 1), 390px 15px 0 0 rgba(255, 205, 234, 1),
  395px 15px 0 0 rgba(255, 205, 234, 1), 400px 15px 0 0 rgba(255, 205, 234, 1),
  405px 15px 0 0 rgba(255, 205, 234, 1), 410px 15px 0 0 rgba(255, 205, 234, 1),
  415px 15px 0 0 rgba(255, 205, 234, 1), 420px 15px 0 0 rgba(255, 205, 234, 1),
  425px 15px 0 0 rgba(255, 205, 234, 1), 430px 15px 0 0 rgba(255, 205, 234, 1),
  435px 15px 0 0 rgba(255, 205, 234, 1), 440px 15px 0 0 rgba(255, 205, 234, 1),
  445px 15px 0 0 rgba(255, 205, 234, 1), 450px 15px 0 0 rgba(255, 205, 234, 1),
  455px 15px 0 0 rgba(255, 205, 234, 1), 460px 15px 0 0 rgba(255, 205, 234, 1),
  465px 15px 0 0 rgba(255, 205, 234, 1), 470px 15px 0 0 rgba(255, 205, 234, 1),
  475px 15px 0 0 rgba(255, 205, 234, 1), 480px 15px 0 0 rgba(255, 205, 234, 1),
  485px 15px 0 0 rgba(255, 205, 234, 1), 490px 15px 0 0 rgba(255, 205, 234, 1),
  495px 15px 0 0 rgba(255, 205, 234, 1), 500px 15px 0 0 rgba(255, 205, 234, 1),
  505px 15px 0 0 rgba(255, 205, 234, 1), 510px 15px 0 0 rgba(255, 205, 234, 1),
  515px 15px 0 0 rgba(255, 205, 234, 1), 520px 15px 0 0 rgba(255, 205, 234, 1),
  525px 15px 0 0 rgba(255, 205, 234, 1), 530px 15px 0 0 rgba(255, 205, 234, 1),
  535px 15px 0 0 rgba(255, 205, 234, 1), 540px 15px 0 0 rgba(255, 205, 234, 1),
  545px 15px 0 0 rgba(255, 205, 234, 1), 550px 15px 0 0 rgba(255, 205, 234, 1),
  555px 15px 0 0 rgba(255, 205, 234, 1), 560px 15px 0 0 rgba(255, 205, 234, 1),
  565px 15px 0 0 rgba(255, 205, 234, 1), 570px 15px 0 0 rgba(255, 205, 234, 1),
  575px 15px 0 0 rgba(255, 205, 234, 1), 580px 15px 0 0 rgba(255, 205, 234, 1),
  585px 15px 0 0 rgba(255, 205, 234, 1), 590px 15px 0 0 rgba(255, 205, 234, 1),
  595px 15px 0 0 rgba(255, 205, 234, 1), 600px 15px 0 0 rgba(255, 205, 234, 1),
  605px 15px 0 0 rgba(255, 205, 234, 1), 610px 15px 0 0 rgba(255, 205, 234, 1),
  615px 15px 0 0 rgba(255, 205, 234, 1), 620px 15px 0 0 rgba(255, 205, 234, 1),
  625px 15px 0 0 rgba(255, 205, 234, 1), 630px 15px 0 0 rgba(255, 205, 234, 1),
  635px 15px 0 0 rgba(255, 205, 234, 1), 640px 15px 0 0 rgba(255, 205, 234, 1),
  645px 15px 0 0 rgba(255, 205, 234, 1), 650px 15px 0 0 rgba(255, 205, 234, 1),
  655px 15px 0 0 rgba(255, 205, 234, 1), 660px 15px 0 0 rgba(255, 205, 234, 1),
  665px 15px 0 0 rgba(255, 205, 234, 1), 670px 15px 0 0 rgba(255, 205, 234, 1),
  675px 15px 0 0 rgba(255, 205, 234, 1), 680px 15px 0 0 rgba(255, 205, 234, 1),
  685px 15px 0 0 rgba(255, 205, 234, 1), 690px 15px 0 0 rgba(255, 205, 234, 1),
  695px 15px 0 0 rgba(168, 90, 150, 1), 700px 15px 0 0 rgba(203, 109, 181, 1),
  5px 20px 0 0 rgba(203, 109, 181, 1), 10px 20px 0 0 rgba(252, 231, 243, 1),
  15px 20px 0 0 rgba(255, 205, 234, 1), 20px 20px 0 0 rgba(255, 205, 234, 1),
  25px 20px 0 0 rgba(203, 109, 181, 1), 30px 20px 0 0 rgba(203, 109, 181, 1),
  35px 20px 0 0 rgba(203, 109, 181, 1), 40px 20px 0 0 rgba(203, 109, 181, 1),
  45px 20px 0 0 rgba(203, 109, 181, 1), 50px 20px 0 0 rgba(203, 109, 181, 1),
  55px 20px 0 0 rgba(203, 109, 181, 1), 60px 20px 0 0 rgba(203, 109, 181, 1),
  65px 20px 0 0 rgba(203, 109, 181, 1), 70px 20px 0 0 rgba(203, 109, 181, 1),
  75px 20px 0 0 rgba(203, 109, 181, 1), 80px 20px 0 0 rgba(203, 109, 181, 1),
  85px 20px 0 0 rgba(203, 109, 181, 1), 90px 20px 0 0 rgba(203, 109, 181, 1),
  95px 20px 0 0 rgba(203, 109, 181, 1), 100px 20px 0 0 rgba(203, 109, 181, 1),
  105px 20px 0 0 rgba(203, 109, 181, 1), 110px 20px 0 0 rgba(203, 109, 181, 1),
  115px 20px 0 0 rgba(203, 109, 181, 1), 120px 20px 0 0 rgba(203, 109, 181, 1),
  125px 20px 0 0 rgba(203, 109, 181, 1), 130px 20px 0 0 rgba(203, 109, 181, 1),
  135px 20px 0 0 rgba(203, 109, 181, 1), 140px 20px 0 0 rgba(203, 109, 181, 1),
  145px 20px 0 0 rgba(203, 109, 181, 1), 150px 20px 0 0 rgba(203, 109, 181, 1),
  155px 20px 0 0 rgba(203, 109, 181, 1), 160px 20px 0 0 rgba(203, 109, 181, 1),
  165px 20px 0 0 rgba(203, 109, 181, 1), 170px 20px 0 0 rgba(203, 109, 181, 1),
  175px 20px 0 0 rgba(203, 109, 181, 1), 180px 20px 0 0 rgba(203, 109, 181, 1),
  185px 20px 0 0 rgba(203, 109, 181, 1), 190px 20px 0 0 rgba(203, 109, 181, 1),
  195px 20px 0 0 rgba(203, 109, 181, 1), 200px 20px 0 0 rgba(203, 109, 181, 1),
  205px 20px 0 0 rgba(203, 109, 181, 1), 210px 20px 0 0 rgba(203, 109, 181, 1),
  215px 20px 0 0 rgba(203, 109, 181, 1), 220px 20px 0 0 rgba(203, 109, 181, 1),
  225px 20px 0 0 rgba(203, 109, 181, 1), 230px 20px 0 0 rgba(203, 109, 181, 1),
  235px 20px 0 0 rgba(203, 109, 181, 1), 240px 20px 0 0 rgba(203, 109, 181, 1),
  245px 20px 0 0 rgba(203, 109, 181, 1), 250px 20px 0 0 rgba(203, 109, 181, 1),
  255px 20px 0 0 rgba(203, 109, 181, 1), 260px 20px 0 0 rgba(203, 109, 181, 1),
  265px 20px 0 0 rgba(203, 109, 181, 1), 270px 20px 0 0 rgba(203, 109, 181, 1),
  275px 20px 0 0 rgba(203, 109, 181, 1), 280px 20px 0 0 rgba(203, 109, 181, 1),
  285px 20px 0 0 rgba(203, 109, 181, 1), 290px 20px 0 0 rgba(203, 109, 181, 1),
  295px 20px 0 0 rgba(203, 109, 181, 1), 300px 20px 0 0 rgba(203, 109, 181, 1),
  305px 20px 0 0 rgba(203, 109, 181, 1), 310px 20px 0 0 rgba(203, 109, 181, 1),
  315px 20px 0 0 rgba(203, 109, 181, 1), 320px 20px 0 0 rgba(203, 109, 181, 1),
  325px 20px 0 0 rgba(203, 109, 181, 1), 330px 20px 0 0 rgba(203, 109, 181, 1),
  335px 20px 0 0 rgba(203, 109, 181, 1), 340px 20px 0 0 rgba(203, 109, 181, 1),
  345px 20px 0 0 rgba(203, 109, 181, 1), 350px 20px 0 0 rgba(203, 109, 181, 1),
  355px 20px 0 0 rgba(203, 109, 181, 1), 360px 20px 0 0 rgba(203, 109, 181, 1),
  365px 20px 0 0 rgba(203, 109, 181, 1), 370px 20px 0 0 rgba(203, 109, 181, 1),
  375px 20px 0 0 rgba(203, 109, 181, 1), 380px 20px 0 0 rgba(203, 109, 181, 1),
  385px 20px 0 0 rgba(203, 109, 181, 1), 390px 20px 0 0 rgba(203, 109, 181, 1),
  395px 20px 0 0 rgba(203, 109, 181, 1), 400px 20px 0 0 rgba(203, 109, 181, 1),
  405px 20px 0 0 rgba(203, 109, 181, 1), 410px 20px 0 0 rgba(203, 109, 181, 1),
  415px 20px 0 0 rgba(203, 109, 181, 1), 420px 20px 0 0 rgba(203, 109, 181, 1),
  425px 20px 0 0 rgba(203, 109, 181, 1), 430px 20px 0 0 rgba(203, 109, 181, 1),
  435px 20px 0 0 rgba(203, 109, 181, 1), 440px 20px 0 0 rgba(203, 109, 181, 1),
  445px 20px 0 0 rgba(203, 109, 181, 1), 450px 20px 0 0 rgba(203, 109, 181, 1),
  455px 20px 0 0 rgba(203, 109, 181, 1), 460px 20px 0 0 rgba(203, 109, 181, 1),
  465px 20px 0 0 rgba(203, 109, 181, 1), 470px 20px 0 0 rgba(203, 109, 181, 1),
  475px 20px 0 0 rgba(203, 109, 181, 1), 480px 20px 0 0 rgba(203, 109, 181, 1),
  485px 20px 0 0 rgba(203, 109, 181, 1), 490px 20px 0 0 rgba(203, 109, 181, 1),
  495px 20px 0 0 rgba(203, 109, 181, 1), 500px 20px 0 0 rgba(203, 109, 181, 1),
  505px 20px 0 0 rgba(203, 109, 181, 1), 510px 20px 0 0 rgba(203, 109, 181, 1),
  515px 20px 0 0 rgba(203, 109, 181, 1), 520px 20px 0 0 rgba(203, 109, 181, 1),
  525px 20px 0 0 rgba(203, 109, 181, 1), 530px 20px 0 0 rgba(203, 109, 181, 1),
  535px 20px 0 0 rgba(203, 109, 181, 1), 540px 20px 0 0 rgba(203, 109, 181, 1),
  545px 20px 0 0 rgba(203, 109, 181, 1), 550px 20px 0 0 rgba(203, 109, 181, 1),
  555px 20px 0 0 rgba(203, 109, 181, 1), 560px 20px 0 0 rgba(203, 109, 181, 1),
  565px 20px 0 0 rgba(203, 109, 181, 1), 570px 20px 0 0 rgba(203, 109, 181, 1),
  575px 20px 0 0 rgba(203, 109, 181, 1), 580px 20px 0 0 rgba(203, 109, 181, 1),
  585px 20px 0 0 rgba(203, 109, 181, 1), 590px 20px 0 0 rgba(203, 109, 181, 1),
  595px 20px 0 0 rgba(203, 109, 181, 1), 600px 20px 0 0 rgba(203, 109, 181, 1),
  605px 20px 0 0 rgba(203, 109, 181, 1), 610px 20px 0 0 rgba(203, 109, 181, 1),
  615px 20px 0 0 rgba(203, 109, 181, 1), 620px 20px 0 0 rgba(203, 109, 181, 1),
  625px 20px 0 0 rgba(203, 109, 181, 1), 630px 20px 0 0 rgba(203, 109, 181, 1),
  635px 20px 0 0 rgba(203, 109, 181, 1), 640px 20px 0 0 rgba(203, 109, 181, 1),
  645px 20px 0 0 rgba(203, 109, 181, 1), 650px 20px 0 0 rgba(203, 109, 181, 1),
  655px 20px 0 0 rgba(203, 109, 181, 1), 660px 20px 0 0 rgba(203, 109, 181, 1),
  665px 20px 0 0 rgba(203, 109, 181, 1), 670px 20px 0 0 rgba(203, 109, 181, 1),
  675px 20px 0 0 rgba(203, 109, 181, 1), 680px 20px 0 0 rgba(203, 109, 181, 1),
  685px 20px 0 0 rgba(203, 109, 181, 1), 690px 20px 0 0 rgba(255, 205, 234, 1),
  695px 20px 0 0 rgba(255, 205, 234, 1), 700px 20px 0 0 rgba(168, 90, 150, 1),
  705px 20px 0 0 rgba(203, 109, 181, 1), 5px 25px 0 0 rgba(203, 109, 181, 1),
  10px 25px 0 0 rgba(252, 231, 243, 1), 15px 25px 0 0 rgba(255, 205, 234, 1),
  20px 25px 0 0 rgba(255, 205, 234, 1), 25px 25px 0 0 rgba(203, 109, 181, 1),
  30px 25px 0 0 rgba(110, 205, 199, 1), 35px 25px 0 0 rgba(110, 205, 199, 1),
  40px 25px 0 0 rgba(110, 205, 199, 1), 45px 25px 0 0 rgba(255, 255, 255, 1),
  50px 25px 0 0 rgba(110, 205, 199, 1), 55px 25px 0 0 rgba(110, 205, 199, 1),
  60px 25px 0 0 rgba(110, 205, 199, 1), 65px 25px 0 0 rgba(110, 205, 199, 1),
  70px 25px 0 0 rgba(110, 205, 199, 1), 75px 25px 0 0 rgba(110, 205, 199, 1),
  80px 25px 0 0 rgba(255, 255, 255, 1), 85px 25px 0 0 rgba(110, 205, 199, 1),
  90px 25px 0 0 rgba(110, 205, 199, 1), 95px 25px 0 0 rgba(110, 205, 199, 1),
  100px 25px 0 0 rgba(110, 205, 199, 1), 105px 25px 0 0 rgba(110, 205, 199, 1),
  110px 25px 0 0 rgba(110, 205, 199, 1), 115px 25px 0 0 rgba(255, 255, 255, 1),
  120px 25px 0 0 rgba(110, 205, 199, 1), 125px 25px 0 0 rgba(110, 205, 199, 1),
  130px 25px 0 0 rgba(110, 205, 199, 1), 135px 25px 0 0 rgba(110, 205, 199, 1),
  140px 25px 0 0 rgba(110, 205, 199, 1), 145px 25px 0 0 rgba(110, 205, 199, 1),
  150px 25px 0 0 rgba(255, 255, 255, 1), 155px 25px 0 0 rgba(110, 205, 199, 1),
  160px 25px 0 0 rgba(110, 205, 199, 1), 165px 25px 0 0 rgba(110, 205, 199, 1),
  170px 25px 0 0 rgba(110, 205, 199, 1), 175px 25px 0 0 rgba(110, 205, 199, 1),
  180px 25px 0 0 rgba(110, 205, 199, 1), 185px 25px 0 0 rgba(255, 255, 255, 1),
  190px 25px 0 0 rgba(110, 205, 199, 1), 195px 25px 0 0 rgba(110, 205, 199, 1),
  200px 25px 0 0 rgba(110, 205, 199, 1), 205px 25px 0 0 rgba(110, 205, 199, 1),
  210px 25px 0 0 rgba(110, 205, 199, 1), 215px 25px 0 0 rgba(110, 205, 199, 1),
  220px 25px 0 0 rgba(255, 255, 255, 1), 225px 25px 0 0 rgba(110, 205, 199, 1),
  230px 25px 0 0 rgba(110, 205, 199, 1), 235px 25px 0 0 rgba(110, 205, 199, 1),
  240px 25px 0 0 rgba(110, 205, 199, 1), 245px 25px 0 0 rgba(110, 205, 199, 1),
  250px 25px 0 0 rgba(110, 205, 199, 1), 255px 25px 0 0 rgba(255, 255, 255, 1),
  260px 25px 0 0 rgba(110, 205, 199, 1), 265px 25px 0 0 rgba(110, 205, 199, 1),
  270px 25px 0 0 rgba(110, 205, 199, 1), 275px 25px 0 0 rgba(110, 205, 199, 1),
  280px 25px 0 0 rgba(110, 205, 199, 1), 285px 25px 0 0 rgba(110, 205, 199, 1),
  290px 25px 0 0 rgba(255, 255, 255, 1), 295px 25px 0 0 rgba(110, 205, 199, 1),
  300px 25px 0 0 rgba(110, 205, 199, 1), 305px 25px 0 0 rgba(110, 205, 199, 1),
  310px 25px 0 0 rgba(110, 205, 199, 1), 315px 25px 0 0 rgba(110, 205, 199, 1),
  320px 25px 0 0 rgba(110, 205, 199, 1), 325px 25px 0 0 rgba(255, 255, 255, 1),
  330px 25px 0 0 rgba(110, 205, 199, 1), 335px 25px 0 0 rgba(110, 205, 199, 1),
  340px 25px 0 0 rgba(110, 205, 199, 1), 345px 25px 0 0 rgba(110, 205, 199, 1),
  350px 25px 0 0 rgba(110, 205, 199, 1), 355px 25px 0 0 rgba(110, 205, 199, 1),
  360px 25px 0 0 rgba(255, 255, 255, 1), 365px 25px 0 0 rgba(110, 205, 199, 1),
  370px 25px 0 0 rgba(110, 205, 199, 1), 375px 25px 0 0 rgba(110, 205, 199, 1),
  380px 25px 0 0 rgba(110, 205, 199, 1), 385px 25px 0 0 rgba(110, 205, 199, 1),
  390px 25px 0 0 rgba(110, 205, 199, 1), 395px 25px 0 0 rgba(255, 255, 255, 1),
  400px 25px 0 0 rgba(110, 205, 199, 1), 405px 25px 0 0 rgba(110, 205, 199, 1),
  410px 25px 0 0 rgba(110, 205, 199, 1), 415px 25px 0 0 rgba(110, 205, 199, 1),
  420px 25px 0 0 rgba(110, 205, 199, 1), 425px 25px 0 0 rgba(110, 205, 199, 1),
  430px 25px 0 0 rgba(255, 255, 255, 1), 435px 25px 0 0 rgba(110, 205, 199, 1),
  440px 25px 0 0 rgba(110, 205, 199, 1), 445px 25px 0 0 rgba(110, 205, 199, 1),
  450px 25px 0 0 rgba(110, 205, 199, 1), 455px 25px 0 0 rgba(110, 205, 199, 1),
  460px 25px 0 0 rgba(110, 205, 199, 1), 465px 25px 0 0 rgba(255, 255, 255, 1),
  470px 25px 0 0 rgba(110, 205, 199, 1), 475px 25px 0 0 rgba(110, 205, 199, 1),
  480px 25px 0 0 rgba(110, 205, 199, 1), 485px 25px 0 0 rgba(110, 205, 199, 1),
  490px 25px 0 0 rgba(110, 205, 199, 1), 495px 25px 0 0 rgba(110, 205, 199, 1),
  500px 25px 0 0 rgba(255, 255, 255, 1), 505px 25px 0 0 rgba(110, 205, 199, 1),
  510px 25px 0 0 rgba(110, 205, 199, 1), 515px 25px 0 0 rgba(110, 205, 199, 1),
  520px 25px 0 0 rgba(110, 205, 199, 1), 525px 25px 0 0 rgba(110, 205, 199, 1),
  530px 25px 0 0 rgba(110, 205, 199, 1), 535px 25px 0 0 rgba(255, 255, 255, 1),
  540px 25px 0 0 rgba(110, 205, 199, 1), 545px 25px 0 0 rgba(110, 205, 199, 1),
  550px 25px 0 0 rgba(110, 205, 199, 1), 555px 25px 0 0 rgba(110, 205, 199, 1),
  560px 25px 0 0 rgba(110, 205, 199, 1), 565px 25px 0 0 rgba(110, 205, 199, 1),
  570px 25px 0 0 rgba(255, 255, 255, 1), 575px 25px 0 0 rgba(110, 205, 199, 1),
  580px 25px 0 0 rgba(110, 205, 199, 1), 585px 25px 0 0 rgba(110, 205, 199, 1),
  590px 25px 0 0 rgba(110, 205, 199, 1), 595px 25px 0 0 rgba(110, 205, 199, 1),
  600px 25px 0 0 rgba(110, 205, 199, 1), 605px 25px 0 0 rgba(255, 255, 255, 1),
  610px 25px 0 0 rgba(110, 205, 199, 1), 615px 25px 0 0 rgba(110, 205, 199, 1),
  620px 25px 0 0 rgba(110, 205, 199, 1), 625px 25px 0 0 rgba(110, 205, 199, 1),
  630px 25px 0 0 rgba(110, 205, 199, 1), 635px 25px 0 0 rgba(110, 205, 199, 1),
  640px 25px 0 0 rgba(255, 255, 255, 1), 645px 25px 0 0 rgba(110, 205, 199, 1),
  650px 25px 0 0 rgba(110, 205, 199, 1), 655px 25px 0 0 rgba(110, 205, 199, 1),
  660px 25px 0 0 rgba(110, 205, 199, 1), 665px 25px 0 0 rgba(110, 205, 199, 1),
  670px 25px 0 0 rgba(110, 205, 199, 1), 675px 25px 0 0 rgba(255, 255, 255, 1),
  680px 25px 0 0 rgba(110, 205, 199, 1), 685px 25px 0 0 rgba(203, 109, 181, 1),
  690px 25px 0 0 rgba(255, 205, 234, 1), 695px 25px 0 0 rgba(255, 205, 234, 1),
  700px 25px 0 0 rgba(168, 90, 150, 1), 705px 25px 0 0 rgba(203, 109, 181, 1),
  5px 30px 0 0 rgba(203, 109, 181, 1), 10px 30px 0 0 rgba(252, 231, 243, 1),
  15px 30px 0 0 rgba(255, 205, 234, 1), 20px 30px 0 0 rgba(255, 205, 234, 1),
  25px 30px 0 0 rgba(203, 109, 181, 1), 30px 30px 0 0 rgba(110, 205, 199, 1),
  35px 30px 0 0 rgba(110, 205, 199, 1), 40px 30px 0 0 rgba(255, 255, 255, 1),
  45px 30px 0 0 rgba(110, 205, 199, 1), 50px 30px 0 0 rgba(110, 205, 199, 1),
  55px 30px 0 0 rgba(110, 205, 199, 1), 60px 30px 0 0 rgba(110, 205, 199, 1),
  65px 30px 0 0 rgba(110, 205, 199, 1), 70px 30px 0 0 rgba(110, 205, 199, 1),
  75px 30px 0 0 rgba(255, 255, 255, 1), 80px 30px 0 0 rgba(110, 205, 199, 1),
  85px 30px 0 0 rgba(110, 205, 199, 1), 90px 30px 0 0 rgba(110, 205, 199, 1),
  95px 30px 0 0 rgba(110, 205, 199, 1), 100px 30px 0 0 rgba(110, 205, 199, 1),
  105px 30px 0 0 rgba(110, 205, 199, 1), 110px 30px 0 0 rgba(255, 255, 255, 1),
  115px 30px 0 0 rgba(110, 205, 199, 1), 120px 30px 0 0 rgba(110, 205, 199, 1),
  125px 30px 0 0 rgba(110, 205, 199, 1), 130px 30px 0 0 rgba(110, 205, 199, 1),
  135px 30px 0 0 rgba(110, 205, 199, 1), 140px 30px 0 0 rgba(110, 205, 199, 1),
  145px 30px 0 0 rgba(255, 255, 255, 1), 150px 30px 0 0 rgba(110, 205, 199, 1),
  155px 30px 0 0 rgba(110, 205, 199, 1), 160px 30px 0 0 rgba(110, 205, 199, 1),
  165px 30px 0 0 rgba(110, 205, 199, 1), 170px 30px 0 0 rgba(110, 205, 199, 1),
  175px 30px 0 0 rgba(110, 205, 199, 1), 180px 30px 0 0 rgba(255, 255, 255, 1),
  185px 30px 0 0 rgba(110, 205, 199, 1), 190px 30px 0 0 rgba(110, 205, 199, 1),
  195px 30px 0 0 rgba(110, 205, 199, 1), 200px 30px 0 0 rgba(110, 205, 199, 1),
  205px 30px 0 0 rgba(110, 205, 199, 1), 210px 30px 0 0 rgba(110, 205, 199, 1),
  215px 30px 0 0 rgba(255, 255, 255, 1), 220px 30px 0 0 rgba(110, 205, 199, 1),
  225px 30px 0 0 rgba(110, 205, 199, 1), 230px 30px 0 0 rgba(110, 205, 199, 1),
  235px 30px 0 0 rgba(110, 205, 199, 1), 240px 30px 0 0 rgba(110, 205, 199, 1),
  245px 30px 0 0 rgba(110, 205, 199, 1), 250px 30px 0 0 rgba(255, 255, 255, 1),
  255px 30px 0 0 rgba(110, 205, 199, 1), 260px 30px 0 0 rgba(110, 205, 199, 1),
  265px 30px 0 0 rgba(110, 205, 199, 1), 270px 30px 0 0 rgba(110, 205, 199, 1),
  275px 30px 0 0 rgba(110, 205, 199, 1), 280px 30px 0 0 rgba(110, 205, 199, 1),
  285px 30px 0 0 rgba(255, 255, 255, 1), 290px 30px 0 0 rgba(110, 205, 199, 1),
  295px 30px 0 0 rgba(110, 205, 199, 1), 300px 30px 0 0 rgba(110, 205, 199, 1),
  305px 30px 0 0 rgba(110, 205, 199, 1), 310px 30px 0 0 rgba(110, 205, 199, 1),
  315px 30px 0 0 rgba(110, 205, 199, 1), 320px 30px 0 0 rgba(255, 255, 255, 1),
  325px 30px 0 0 rgba(110, 205, 199, 1), 330px 30px 0 0 rgba(110, 205, 199, 1),
  335px 30px 0 0 rgba(110, 205, 199, 1), 340px 30px 0 0 rgba(110, 205, 199, 1),
  345px 30px 0 0 rgba(110, 205, 199, 1), 350px 30px 0 0 rgba(110, 205, 199, 1),
  355px 30px 0 0 rgba(255, 255, 255, 1), 360px 30px 0 0 rgba(110, 205, 199, 1),
  365px 30px 0 0 rgba(110, 205, 199, 1), 370px 30px 0 0 rgba(110, 205, 199, 1),
  375px 30px 0 0 rgba(110, 205, 199, 1), 380px 30px 0 0 rgba(110, 205, 199, 1),
  385px 30px 0 0 rgba(110, 205, 199, 1), 390px 30px 0 0 rgba(255, 255, 255, 1),
  395px 30px 0 0 rgba(110, 205, 199, 1), 400px 30px 0 0 rgba(110, 205, 199, 1),
  405px 30px 0 0 rgba(110, 205, 199, 1), 410px 30px 0 0 rgba(110, 205, 199, 1),
  415px 30px 0 0 rgba(110, 205, 199, 1), 420px 30px 0 0 rgba(110, 205, 199, 1),
  425px 30px 0 0 rgba(255, 255, 255, 1), 430px 30px 0 0 rgba(110, 205, 199, 1),
  435px 30px 0 0 rgba(110, 205, 199, 1), 440px 30px 0 0 rgba(110, 205, 199, 1),
  445px 30px 0 0 rgba(110, 205, 199, 1), 450px 30px 0 0 rgba(110, 205, 199, 1),
  455px 30px 0 0 rgba(110, 205, 199, 1), 460px 30px 0 0 rgba(255, 255, 255, 1),
  465px 30px 0 0 rgba(110, 205, 199, 1), 470px 30px 0 0 rgba(110, 205, 199, 1),
  475px 30px 0 0 rgba(110, 205, 199, 1), 480px 30px 0 0 rgba(110, 205, 199, 1),
  485px 30px 0 0 rgba(110, 205, 199, 1), 490px 30px 0 0 rgba(110, 205, 199, 1),
  495px 30px 0 0 rgba(255, 255, 255, 1), 500px 30px 0 0 rgba(110, 205, 199, 1),
  505px 30px 0 0 rgba(110, 205, 199, 1), 510px 30px 0 0 rgba(110, 205, 199, 1),
  515px 30px 0 0 rgba(110, 205, 199, 1), 520px 30px 0 0 rgba(110, 205, 199, 1),
  525px 30px 0 0 rgba(110, 205, 199, 1), 530px 30px 0 0 rgba(255, 255, 255, 1),
  535px 30px 0 0 rgba(110, 205, 199, 1), 540px 30px 0 0 rgba(110, 205, 199, 1),
  545px 30px 0 0 rgba(110, 205, 199, 1), 550px 30px 0 0 rgba(110, 205, 199, 1),
  555px 30px 0 0 rgba(110, 205, 199, 1), 560px 30px 0 0 rgba(110, 205, 199, 1),
  565px 30px 0 0 rgba(255, 255, 255, 1), 570px 30px 0 0 rgba(110, 205, 199, 1),
  575px 30px 0 0 rgba(110, 205, 199, 1), 580px 30px 0 0 rgba(110, 205, 199, 1),
  585px 30px 0 0 rgba(110, 205, 199, 1), 590px 30px 0 0 rgba(110, 205, 199, 1),
  595px 30px 0 0 rgba(110, 205, 199, 1), 600px 30px 0 0 rgba(255, 255, 255, 1),
  605px 30px 0 0 rgba(110, 205, 199, 1), 610px 30px 0 0 rgba(110, 205, 199, 1),
  615px 30px 0 0 rgba(110, 205, 199, 1), 620px 30px 0 0 rgba(110, 205, 199, 1),
  625px 30px 0 0 rgba(110, 205, 199, 1), 630px 30px 0 0 rgba(110, 205, 199, 1),
  635px 30px 0 0 rgba(255, 255, 255, 1), 640px 30px 0 0 rgba(110, 205, 199, 1),
  645px 30px 0 0 rgba(110, 205, 199, 1), 650px 30px 0 0 rgba(110, 205, 199, 1),
  655px 30px 0 0 rgba(110, 205, 199, 1), 660px 30px 0 0 rgba(110, 205, 199, 1),
  665px 30px 0 0 rgba(110, 205, 199, 1), 670px 30px 0 0 rgba(255, 255, 255, 1),
  675px 30px 0 0 rgba(110, 205, 199, 1), 680px 30px 0 0 rgba(110, 205, 199, 1),
  685px 30px 0 0 rgba(203, 109, 181, 1), 690px 30px 0 0 rgba(255, 205, 234, 1),
  695px 30px 0 0 rgba(255, 205, 234, 1), 700px 30px 0 0 rgba(168, 90, 150, 1),
  705px 30px 0 0 rgba(203, 109, 181, 1), 5px 35px 0 0 rgba(203, 109, 181, 1),
  10px 35px 0 0 rgba(252, 231, 243, 1), 15px 35px 0 0 rgba(255, 205, 234, 1),
  20px 35px 0 0 rgba(255, 205, 234, 1), 25px 35px 0 0 rgba(203, 109, 181, 1),
  30px 35px 0 0 rgba(110, 205, 199, 1), 35px 35px 0 0 rgba(255, 255, 255, 1),
  40px 35px 0 0 rgba(110, 205, 199, 1), 45px 35px 0 0 rgba(110, 205, 199, 1),
  50px 35px 0 0 rgba(110, 205, 199, 1), 55px 35px 0 0 rgba(110, 205, 199, 1),
  60px 35px 0 0 rgba(110, 205, 199, 1), 65px 35px 0 0 rgba(110, 205, 199, 1),
  70px 35px 0 0 rgba(255, 255, 255, 1), 75px 35px 0 0 rgba(110, 205, 199, 1),
  80px 35px 0 0 rgba(110, 205, 199, 1), 85px 35px 0 0 rgba(110, 205, 199, 1),
  90px 35px 0 0 rgba(110, 205, 199, 1), 95px 35px 0 0 rgba(110, 205, 199, 1),
  100px 35px 0 0 rgba(110, 205, 199, 1), 105px 35px 0 0 rgba(255, 255, 255, 1),
  110px 35px 0 0 rgba(110, 205, 199, 1), 115px 35px 0 0 rgba(110, 205, 199, 1),
  120px 35px 0 0 rgba(110, 205, 199, 1), 125px 35px 0 0 rgba(110, 205, 199, 1),
  130px 35px 0 0 rgba(110, 205, 199, 1), 135px 35px 0 0 rgba(110, 205, 199, 1),
  140px 35px 0 0 rgba(255, 255, 255, 1), 145px 35px 0 0 rgba(110, 205, 199, 1),
  150px 35px 0 0 rgba(110, 205, 199, 1), 155px 35px 0 0 rgba(110, 205, 199, 1),
  160px 35px 0 0 rgba(110, 205, 199, 1), 165px 35px 0 0 rgba(110, 205, 199, 1),
  170px 35px 0 0 rgba(110, 205, 199, 1), 175px 35px 0 0 rgba(255, 255, 255, 1),
  180px 35px 0 0 rgba(110, 205, 199, 1), 185px 35px 0 0 rgba(110, 205, 199, 1),
  190px 35px 0 0 rgba(110, 205, 199, 1), 195px 35px 0 0 rgba(110, 205, 199, 1),
  200px 35px 0 0 rgba(110, 205, 199, 1), 205px 35px 0 0 rgba(110, 205, 199, 1),
  210px 35px 0 0 rgba(255, 255, 255, 1), 215px 35px 0 0 rgba(110, 205, 199, 1),
  220px 35px 0 0 rgba(110, 205, 199, 1), 225px 35px 0 0 rgba(110, 205, 199, 1),
  230px 35px 0 0 rgba(110, 205, 199, 1), 235px 35px 0 0 rgba(110, 205, 199, 1),
  240px 35px 0 0 rgba(110, 205, 199, 1), 245px 35px 0 0 rgba(255, 255, 255, 1),
  250px 35px 0 0 rgba(110, 205, 199, 1), 255px 35px 0 0 rgba(110, 205, 199, 1),
  260px 35px 0 0 rgba(110, 205, 199, 1), 265px 35px 0 0 rgba(110, 205, 199, 1),
  270px 35px 0 0 rgba(110, 205, 199, 1), 275px 35px 0 0 rgba(110, 205, 199, 1),
  280px 35px 0 0 rgba(255, 255, 255, 1), 285px 35px 0 0 rgba(110, 205, 199, 1),
  290px 35px 0 0 rgba(110, 205, 199, 1), 295px 35px 0 0 rgba(110, 205, 199, 1),
  300px 35px 0 0 rgba(110, 205, 199, 1), 305px 35px 0 0 rgba(110, 205, 199, 1),
  310px 35px 0 0 rgba(110, 205, 199, 1), 315px 35px 0 0 rgba(255, 255, 255, 1),
  320px 35px 0 0 rgba(110, 205, 199, 1), 325px 35px 0 0 rgba(110, 205, 199, 1),
  330px 35px 0 0 rgba(110, 205, 199, 1), 335px 35px 0 0 rgba(110, 205, 199, 1),
  340px 35px 0 0 rgba(110, 205, 199, 1), 345px 35px 0 0 rgba(110, 205, 199, 1),
  350px 35px 0 0 rgba(255, 255, 255, 1), 355px 35px 0 0 rgba(110, 205, 199, 1),
  360px 35px 0 0 rgba(110, 205, 199, 1), 365px 35px 0 0 rgba(110, 205, 199, 1),
  370px 35px 0 0 rgba(110, 205, 199, 1), 375px 35px 0 0 rgba(110, 205, 199, 1),
  380px 35px 0 0 rgba(110, 205, 199, 1), 385px 35px 0 0 rgba(255, 255, 255, 1),
  390px 35px 0 0 rgba(110, 205, 199, 1), 395px 35px 0 0 rgba(110, 205, 199, 1),
  400px 35px 0 0 rgba(110, 205, 199, 1), 405px 35px 0 0 rgba(110, 205, 199, 1),
  410px 35px 0 0 rgba(110, 205, 199, 1), 415px 35px 0 0 rgba(110, 205, 199, 1),
  420px 35px 0 0 rgba(255, 255, 255, 1), 425px 35px 0 0 rgba(110, 205, 199, 1),
  430px 35px 0 0 rgba(110, 205, 199, 1), 435px 35px 0 0 rgba(110, 205, 199, 1),
  440px 35px 0 0 rgba(110, 205, 199, 1), 445px 35px 0 0 rgba(110, 205, 199, 1),
  450px 35px 0 0 rgba(110, 205, 199, 1), 455px 35px 0 0 rgba(255, 255, 255, 1),
  460px 35px 0 0 rgba(110, 205, 199, 1), 465px 35px 0 0 rgba(110, 205, 199, 1),
  470px 35px 0 0 rgba(110, 205, 199, 1), 475px 35px 0 0 rgba(110, 205, 199, 1),
  480px 35px 0 0 rgba(110, 205, 199, 1), 485px 35px 0 0 rgba(110, 205, 199, 1),
  490px 35px 0 0 rgba(255, 255, 255, 1), 495px 35px 0 0 rgba(110, 205, 199, 1),
  500px 35px 0 0 rgba(110, 205, 199, 1), 505px 35px 0 0 rgba(110, 205, 199, 1),
  510px 35px 0 0 rgba(110, 205, 199, 1), 515px 35px 0 0 rgba(110, 205, 199, 1),
  520px 35px 0 0 rgba(110, 205, 199, 1), 525px 35px 0 0 rgba(255, 255, 255, 1),
  530px 35px 0 0 rgba(110, 205, 199, 1), 535px 35px 0 0 rgba(110, 205, 199, 1),
  540px 35px 0 0 rgba(110, 205, 199, 1), 545px 35px 0 0 rgba(110, 205, 199, 1),
  550px 35px 0 0 rgba(110, 205, 199, 1), 555px 35px 0 0 rgba(110, 205, 199, 1),
  560px 35px 0 0 rgba(255, 255, 255, 1), 565px 35px 0 0 rgba(110, 205, 199, 1),
  570px 35px 0 0 rgba(110, 205, 199, 1), 575px 35px 0 0 rgba(110, 205, 199, 1),
  580px 35px 0 0 rgba(110, 205, 199, 1), 585px 35px 0 0 rgba(110, 205, 199, 1),
  590px 35px 0 0 rgba(110, 205, 199, 1), 595px 35px 0 0 rgba(255, 255, 255, 1),
  600px 35px 0 0 rgba(110, 205, 199, 1), 605px 35px 0 0 rgba(110, 205, 199, 1),
  610px 35px 0 0 rgba(110, 205, 199, 1), 615px 35px 0 0 rgba(110, 205, 199, 1),
  620px 35px 0 0 rgba(110, 205, 199, 1), 625px 35px 0 0 rgba(110, 205, 199, 1),
  630px 35px 0 0 rgba(255, 255, 255, 1), 635px 35px 0 0 rgba(110, 205, 199, 1),
  640px 35px 0 0 rgba(110, 205, 199, 1), 645px 35px 0 0 rgba(110, 205, 199, 1),
  650px 35px 0 0 rgba(110, 205, 199, 1), 655px 35px 0 0 rgba(110, 205, 199, 1),
  660px 35px 0 0 rgba(110, 205, 199, 1), 665px 35px 0 0 rgba(255, 255, 255, 1),
  670px 35px 0 0 rgba(110, 205, 199, 1), 675px 35px 0 0 rgba(110, 205, 199, 1),
  680px 35px 0 0 rgba(110, 205, 199, 1), 685px 35px 0 0 rgba(203, 109, 181, 1),
  690px 35px 0 0 rgba(255, 205, 234, 1), 695px 35px 0 0 rgba(255, 205, 234, 1),
  700px 35px 0 0 rgba(168, 90, 150, 1), 705px 35px 0 0 rgba(203, 109, 181, 1),
  5px 40px 0 0 rgba(203, 109, 181, 1), 10px 40px 0 0 rgba(252, 231, 243, 1),
  15px 40px 0 0 rgba(255, 205, 234, 1), 20px 40px 0 0 rgba(255, 205, 234, 1),
  25px 40px 0 0 rgba(203, 109, 181, 1), 30px 40px 0 0 rgba(255, 255, 255, 1),
  35px 40px 0 0 rgba(110, 205, 199, 1), 40px 40px 0 0 rgba(110, 205, 199, 1),
  45px 40px 0 0 rgba(110, 205, 199, 1), 50px 40px 0 0 rgba(110, 205, 199, 1),
  55px 40px 0 0 rgba(110, 205, 199, 1), 60px 40px 0 0 rgba(110, 205, 199, 1),
  65px 40px 0 0 rgba(255, 255, 255, 1), 70px 40px 0 0 rgba(110, 205, 199, 1),
  75px 40px 0 0 rgba(110, 205, 199, 1), 80px 40px 0 0 rgba(110, 205, 199, 1),
  85px 40px 0 0 rgba(110, 205, 199, 1), 90px 40px 0 0 rgba(110, 205, 199, 1),
  95px 40px 0 0 rgba(110, 205, 199, 1), 100px 40px 0 0 rgba(255, 255, 255, 1),
  105px 40px 0 0 rgba(110, 205, 199, 1), 110px 40px 0 0 rgba(110, 205, 199, 1),
  115px 40px 0 0 rgba(110, 205, 199, 1), 120px 40px 0 0 rgba(110, 205, 199, 1),
  125px 40px 0 0 rgba(110, 205, 199, 1), 130px 40px 0 0 rgba(110, 205, 199, 1),
  135px 40px 0 0 rgba(255, 255, 255, 1), 140px 40px 0 0 rgba(110, 205, 199, 1),
  145px 40px 0 0 rgba(110, 205, 199, 1), 150px 40px 0 0 rgba(110, 205, 199, 1),
  155px 40px 0 0 rgba(110, 205, 199, 1), 160px 40px 0 0 rgba(110, 205, 199, 1),
  165px 40px 0 0 rgba(110, 205, 199, 1), 170px 40px 0 0 rgba(255, 255, 255, 1),
  175px 40px 0 0 rgba(110, 205, 199, 1), 180px 40px 0 0 rgba(110, 205, 199, 1),
  185px 40px 0 0 rgba(110, 205, 199, 1), 190px 40px 0 0 rgba(110, 205, 199, 1),
  195px 40px 0 0 rgba(110, 205, 199, 1), 200px 40px 0 0 rgba(110, 205, 199, 1),
  205px 40px 0 0 rgba(255, 255, 255, 1), 210px 40px 0 0 rgba(110, 205, 199, 1),
  215px 40px 0 0 rgba(110, 205, 199, 1), 220px 40px 0 0 rgba(110, 205, 199, 1),
  225px 40px 0 0 rgba(110, 205, 199, 1), 230px 40px 0 0 rgba(110, 205, 199, 1),
  235px 40px 0 0 rgba(110, 205, 199, 1), 240px 40px 0 0 rgba(255, 255, 255, 1),
  245px 40px 0 0 rgba(110, 205, 199, 1), 250px 40px 0 0 rgba(110, 205, 199, 1),
  255px 40px 0 0 rgba(110, 205, 199, 1), 260px 40px 0 0 rgba(110, 205, 199, 1),
  265px 40px 0 0 rgba(110, 205, 199, 1), 270px 40px 0 0 rgba(110, 205, 199, 1),
  275px 40px 0 0 rgba(255, 255, 255, 1), 280px 40px 0 0 rgba(110, 205, 199, 1),
  285px 40px 0 0 rgba(110, 205, 199, 1), 290px 40px 0 0 rgba(110, 205, 199, 1),
  295px 40px 0 0 rgba(110, 205, 199, 1), 300px 40px 0 0 rgba(110, 205, 199, 1),
  305px 40px 0 0 rgba(110, 205, 199, 1), 310px 40px 0 0 rgba(255, 255, 255, 1),
  315px 40px 0 0 rgba(110, 205, 199, 1), 320px 40px 0 0 rgba(110, 205, 199, 1),
  325px 40px 0 0 rgba(110, 205, 199, 1), 330px 40px 0 0 rgba(110, 205, 199, 1),
  335px 40px 0 0 rgba(110, 205, 199, 1), 340px 40px 0 0 rgba(110, 205, 199, 1),
  345px 40px 0 0 rgba(255, 255, 255, 1), 350px 40px 0 0 rgba(110, 205, 199, 1),
  355px 40px 0 0 rgba(110, 205, 199, 1), 360px 40px 0 0 rgba(110, 205, 199, 1),
  365px 40px 0 0 rgba(110, 205, 199, 1), 370px 40px 0 0 rgba(110, 205, 199, 1),
  375px 40px 0 0 rgba(110, 205, 199, 1), 380px 40px 0 0 rgba(255, 255, 255, 1),
  385px 40px 0 0 rgba(110, 205, 199, 1), 390px 40px 0 0 rgba(110, 205, 199, 1),
  395px 40px 0 0 rgba(110, 205, 199, 1), 400px 40px 0 0 rgba(110, 205, 199, 1),
  405px 40px 0 0 rgba(110, 205, 199, 1), 410px 40px 0 0 rgba(110, 205, 199, 1),
  415px 40px 0 0 rgba(255, 255, 255, 1), 420px 40px 0 0 rgba(110, 205, 199, 1),
  425px 40px 0 0 rgba(110, 205, 199, 1), 430px 40px 0 0 rgba(110, 205, 199, 1),
  435px 40px 0 0 rgba(110, 205, 199, 1), 440px 40px 0 0 rgba(110, 205, 199, 1),
  445px 40px 0 0 rgba(110, 205, 199, 1), 450px 40px 0 0 rgba(255, 255, 255, 1),
  455px 40px 0 0 rgba(110, 205, 199, 1), 460px 40px 0 0 rgba(110, 205, 199, 1),
  465px 40px 0 0 rgba(110, 205, 199, 1), 470px 40px 0 0 rgba(110, 205, 199, 1),
  475px 40px 0 0 rgba(110, 205, 199, 1), 480px 40px 0 0 rgba(110, 205, 199, 1),
  485px 40px 0 0 rgba(255, 255, 255, 1), 490px 40px 0 0 rgba(110, 205, 199, 1),
  495px 40px 0 0 rgba(110, 205, 199, 1), 500px 40px 0 0 rgba(110, 205, 199, 1),
  505px 40px 0 0 rgba(110, 205, 199, 1), 510px 40px 0 0 rgba(110, 205, 199, 1),
  515px 40px 0 0 rgba(110, 205, 199, 1), 520px 40px 0 0 rgba(255, 255, 255, 1),
  525px 40px 0 0 rgba(110, 205, 199, 1), 530px 40px 0 0 rgba(110, 205, 199, 1),
  535px 40px 0 0 rgba(110, 205, 199, 1), 540px 40px 0 0 rgba(110, 205, 199, 1),
  545px 40px 0 0 rgba(110, 205, 199, 1), 550px 40px 0 0 rgba(110, 205, 199, 1),
  555px 40px 0 0 rgba(255, 255, 255, 1), 560px 40px 0 0 rgba(110, 205, 199, 1),
  565px 40px 0 0 rgba(110, 205, 199, 1), 570px 40px 0 0 rgba(110, 205, 199, 1),
  575px 40px 0 0 rgba(110, 205, 199, 1), 580px 40px 0 0 rgba(110, 205, 199, 1),
  585px 40px 0 0 rgba(110, 205, 199, 1), 590px 40px 0 0 rgba(255, 255, 255, 1),
  595px 40px 0 0 rgba(110, 205, 199, 1), 600px 40px 0 0 rgba(110, 205, 199, 1),
  605px 40px 0 0 rgba(110, 205, 199, 1), 610px 40px 0 0 rgba(110, 205, 199, 1),
  615px 40px 0 0 rgba(110, 205, 199, 1), 620px 40px 0 0 rgba(110, 205, 199, 1),
  625px 40px 0 0 rgba(255, 255, 255, 1), 630px 40px 0 0 rgba(110, 205, 199, 1),
  635px 40px 0 0 rgba(110, 205, 199, 1), 640px 40px 0 0 rgba(110, 205, 199, 1),
  645px 40px 0 0 rgba(110, 205, 199, 1), 650px 40px 0 0 rgba(110, 205, 199, 1),
  655px 40px 0 0 rgba(110, 205, 199, 1), 660px 40px 0 0 rgba(255, 255, 255, 1),
  665px 40px 0 0 rgba(110, 205, 199, 1), 670px 40px 0 0 rgba(110, 205, 199, 1),
  675px 40px 0 0 rgba(110, 205, 199, 1), 680px 40px 0 0 rgba(110, 205, 199, 1),
  685px 40px 0 0 rgba(203, 109, 181, 1), 690px 40px 0 0 rgba(255, 205, 234, 1),
  695px 40px 0 0 rgba(255, 205, 234, 1), 700px 40px 0 0 rgba(168, 90, 150, 1),
  705px 40px 0 0 rgba(203, 109, 181, 1), 5px 45px 0 0 rgba(203, 109, 181, 1),
  10px 45px 0 0 rgba(252, 231, 243, 1), 15px 45px 0 0 rgba(255, 205, 234, 1),
  20px 45px 0 0 rgba(255, 205, 234, 1), 25px 45px 0 0 rgba(203, 109, 181, 1),
  30px 45px 0 0 rgba(110, 205, 199, 1), 35px 45px 0 0 rgba(110, 205, 199, 1),
  40px 45px 0 0 rgba(110, 205, 199, 1), 45px 45px 0 0 rgba(110, 205, 199, 1),
  50px 45px 0 0 rgba(110, 205, 199, 1), 55px 45px 0 0 rgba(110, 205, 199, 1),
  60px 45px 0 0 rgba(255, 255, 255, 1), 65px 45px 0 0 rgba(110, 205, 199, 1),
  70px 45px 0 0 rgba(110, 205, 199, 1), 75px 45px 0 0 rgba(110, 205, 199, 1),
  80px 45px 0 0 rgba(110, 205, 199, 1), 85px 45px 0 0 rgba(110, 205, 199, 1),
  90px 45px 0 0 rgba(110, 205, 199, 1), 95px 45px 0 0 rgba(255, 255, 255, 1),
  100px 45px 0 0 rgba(110, 205, 199, 1), 105px 45px 0 0 rgba(110, 205, 199, 1),
  110px 45px 0 0 rgba(110, 205, 199, 1), 115px 45px 0 0 rgba(110, 205, 199, 1),
  120px 45px 0 0 rgba(110, 205, 199, 1), 125px 45px 0 0 rgba(110, 205, 199, 1),
  130px 45px 0 0 rgba(255, 255, 255, 1), 135px 45px 0 0 rgba(110, 205, 199, 1),
  140px 45px 0 0 rgba(110, 205, 199, 1), 145px 45px 0 0 rgba(110, 205, 199, 1),
  150px 45px 0 0 rgba(110, 205, 199, 1), 155px 45px 0 0 rgba(110, 205, 199, 1),
  160px 45px 0 0 rgba(110, 205, 199, 1), 165px 45px 0 0 rgba(255, 255, 255, 1),
  170px 45px 0 0 rgba(110, 205, 199, 1), 175px 45px 0 0 rgba(110, 205, 199, 1),
  180px 45px 0 0 rgba(110, 205, 199, 1), 185px 45px 0 0 rgba(110, 205, 199, 1),
  190px 45px 0 0 rgba(110, 205, 199, 1), 195px 45px 0 0 rgba(110, 205, 199, 1),
  200px 45px 0 0 rgba(255, 255, 255, 1), 205px 45px 0 0 rgba(110, 205, 199, 1),
  210px 45px 0 0 rgba(110, 205, 199, 1), 215px 45px 0 0 rgba(110, 205, 199, 1),
  220px 45px 0 0 rgba(110, 205, 199, 1), 225px 45px 0 0 rgba(110, 205, 199, 1),
  230px 45px 0 0 rgba(110, 205, 199, 1), 235px 45px 0 0 rgba(255, 255, 255, 1),
  240px 45px 0 0 rgba(110, 205, 199, 1), 245px 45px 0 0 rgba(110, 205, 199, 1),
  250px 45px 0 0 rgba(110, 205, 199, 1), 255px 45px 0 0 rgba(110, 205, 199, 1),
  260px 45px 0 0 rgba(110, 205, 199, 1), 265px 45px 0 0 rgba(110, 205, 199, 1),
  270px 45px 0 0 rgba(255, 255, 255, 1), 275px 45px 0 0 rgba(110, 205, 199, 1),
  280px 45px 0 0 rgba(110, 205, 199, 1), 285px 45px 0 0 rgba(110, 205, 199, 1),
  290px 45px 0 0 rgba(110, 205, 199, 1), 295px 45px 0 0 rgba(110, 205, 199, 1),
  300px 45px 0 0 rgba(110, 205, 199, 1), 305px 45px 0 0 rgba(255, 255, 255, 1),
  310px 45px 0 0 rgba(110, 205, 199, 1), 315px 45px 0 0 rgba(110, 205, 199, 1),
  320px 45px 0 0 rgba(110, 205, 199, 1), 325px 45px 0 0 rgba(110, 205, 199, 1),
  330px 45px 0 0 rgba(110, 205, 199, 1), 335px 45px 0 0 rgba(110, 205, 199, 1),
  340px 45px 0 0 rgba(255, 255, 255, 1), 345px 45px 0 0 rgba(110, 205, 199, 1),
  350px 45px 0 0 rgba(110, 205, 199, 1), 355px 45px 0 0 rgba(110, 205, 199, 1),
  360px 45px 0 0 rgba(110, 205, 199, 1), 365px 45px 0 0 rgba(110, 205, 199, 1),
  370px 45px 0 0 rgba(110, 205, 199, 1), 375px 45px 0 0 rgba(255, 255, 255, 1),
  380px 45px 0 0 rgba(110, 205, 199, 1), 385px 45px 0 0 rgba(110, 205, 199, 1),
  390px 45px 0 0 rgba(110, 205, 199, 1), 395px 45px 0 0 rgba(110, 205, 199, 1),
  400px 45px 0 0 rgba(110, 205, 199, 1), 405px 45px 0 0 rgba(110, 205, 199, 1),
  410px 45px 0 0 rgba(255, 255, 255, 1), 415px 45px 0 0 rgba(110, 205, 199, 1),
  420px 45px 0 0 rgba(110, 205, 199, 1), 425px 45px 0 0 rgba(110, 205, 199, 1),
  430px 45px 0 0 rgba(110, 205, 199, 1), 435px 45px 0 0 rgba(110, 205, 199, 1),
  440px 45px 0 0 rgba(110, 205, 199, 1), 445px 45px 0 0 rgba(255, 255, 255, 1),
  450px 45px 0 0 rgba(110, 205, 199, 1), 455px 45px 0 0 rgba(110, 205, 199, 1),
  460px 45px 0 0 rgba(110, 205, 199, 1), 465px 45px 0 0 rgba(110, 205, 199, 1),
  470px 45px 0 0 rgba(110, 205, 199, 1), 475px 45px 0 0 rgba(110, 205, 199, 1),
  480px 45px 0 0 rgba(255, 255, 255, 1), 485px 45px 0 0 rgba(110, 205, 199, 1),
  490px 45px 0 0 rgba(110, 205, 199, 1), 495px 45px 0 0 rgba(110, 205, 199, 1),
  500px 45px 0 0 rgba(110, 205, 199, 1), 505px 45px 0 0 rgba(110, 205, 199, 1),
  510px 45px 0 0 rgba(110, 205, 199, 1), 515px 45px 0 0 rgba(255, 255, 255, 1),
  520px 45px 0 0 rgba(110, 205, 199, 1), 525px 45px 0 0 rgba(110, 205, 199, 1),
  530px 45px 0 0 rgba(110, 205, 199, 1), 535px 45px 0 0 rgba(110, 205, 199, 1),
  540px 45px 0 0 rgba(110, 205, 199, 1), 545px 45px 0 0 rgba(110, 205, 199, 1),
  550px 45px 0 0 rgba(255, 255, 255, 1), 555px 45px 0 0 rgba(110, 205, 199, 1),
  560px 45px 0 0 rgba(110, 205, 199, 1), 565px 45px 0 0 rgba(110, 205, 199, 1),
  570px 45px 0 0 rgba(110, 205, 199, 1), 575px 45px 0 0 rgba(110, 205, 199, 1),
  580px 45px 0 0 rgba(110, 205, 199, 1), 585px 45px 0 0 rgba(255, 255, 255, 1),
  590px 45px 0 0 rgba(110, 205, 199, 1), 595px 45px 0 0 rgba(110, 205, 199, 1),
  600px 45px 0 0 rgba(110, 205, 199, 1), 605px 45px 0 0 rgba(110, 205, 199, 1),
  610px 45px 0 0 rgba(110, 205, 199, 1), 615px 45px 0 0 rgba(110, 205, 199, 1),
  620px 45px 0 0 rgba(255, 255, 255, 1), 625px 45px 0 0 rgba(110, 205, 199, 1),
  630px 45px 0 0 rgba(110, 205, 199, 1), 635px 45px 0 0 rgba(110, 205, 199, 1),
  640px 45px 0 0 rgba(110, 205, 199, 1), 645px 45px 0 0 rgba(110, 205, 199, 1),
  650px 45px 0 0 rgba(110, 205, 199, 1), 655px 45px 0 0 rgba(255, 255, 255, 1),
  660px 45px 0 0 rgba(110, 205, 199, 1), 665px 45px 0 0 rgba(110, 205, 199, 1),
  670px 45px 0 0 rgba(110, 205, 199, 1), 675px 45px 0 0 rgba(110, 205, 199, 1),
  680px 45px 0 0 rgba(110, 205, 199, 1), 685px 45px 0 0 rgba(203, 109, 181, 1),
  690px 45px 0 0 rgba(255, 205, 234, 1), 695px 45px 0 0 rgba(255, 205, 234, 1),
  700px 45px 0 0 rgba(168, 90, 150, 1), 705px 45px 0 0 rgba(203, 109, 181, 1),
  5px 50px 0 0 rgba(203, 109, 181, 1), 10px 50px 0 0 rgba(252, 231, 243, 1),
  15px 50px 0 0 rgba(255, 205, 234, 1), 20px 50px 0 0 rgba(255, 205, 234, 1),
  25px 50px 0 0 rgba(203, 109, 181, 1), 30px 50px 0 0 rgba(110, 205, 199, 1),
  35px 50px 0 0 rgba(110, 205, 199, 1), 40px 50px 0 0 rgba(110, 205, 199, 1),
  45px 50px 0 0 rgba(110, 205, 199, 1), 50px 50px 0 0 rgba(110, 205, 199, 1),
  55px 50px 0 0 rgba(110, 205, 199, 1), 60px 50px 0 0 rgba(110, 205, 199, 1),
  65px 50px 0 0 rgba(110, 205, 199, 1), 70px 50px 0 0 rgba(110, 205, 199, 1),
  75px 50px 0 0 rgba(110, 205, 199, 1), 80px 50px 0 0 rgba(110, 205, 199, 1),
  85px 50px 0 0 rgba(110, 205, 199, 1), 90px 50px 0 0 rgba(110, 205, 199, 1),
  95px 50px 0 0 rgba(110, 205, 199, 1), 100px 50px 0 0 rgba(110, 205, 199, 1),
  105px 50px 0 0 rgba(110, 205, 199, 1), 110px 50px 0 0 rgba(110, 205, 199, 1),
  115px 50px 0 0 rgba(110, 205, 199, 1), 120px 50px 0 0 rgba(110, 205, 199, 1),
  125px 50px 0 0 rgba(110, 205, 199, 1), 130px 50px 0 0 rgba(110, 205, 199, 1),
  135px 50px 0 0 rgba(110, 205, 199, 1), 140px 50px 0 0 rgba(110, 205, 199, 1),
  145px 50px 0 0 rgba(110, 205, 199, 1), 150px 50px 0 0 rgba(110, 205, 199, 1),
  155px 50px 0 0 rgba(110, 205, 199, 1), 160px 50px 0 0 rgba(110, 205, 199, 1),
  165px 50px 0 0 rgba(110, 205, 199, 1), 170px 50px 0 0 rgba(110, 205, 199, 1),
  175px 50px 0 0 rgba(110, 205, 199, 1), 180px 50px 0 0 rgba(110, 205, 199, 1),
  185px 50px 0 0 rgba(110, 205, 199, 1), 190px 50px 0 0 rgba(110, 205, 199, 1),
  195px 50px 0 0 rgba(110, 205, 199, 1), 200px 50px 0 0 rgba(110, 205, 199, 1),
  205px 50px 0 0 rgba(110, 205, 199, 1), 210px 50px 0 0 rgba(110, 205, 199, 1),
  215px 50px 0 0 rgba(110, 205, 199, 1), 220px 50px 0 0 rgba(110, 205, 199, 1),
  225px 50px 0 0 rgba(110, 205, 199, 1), 230px 50px 0 0 rgba(110, 205, 199, 1),
  235px 50px 0 0 rgba(110, 205, 199, 1), 240px 50px 0 0 rgba(110, 205, 199, 1),
  245px 50px 0 0 rgba(110, 205, 199, 1), 250px 50px 0 0 rgba(110, 205, 199, 1),
  255px 50px 0 0 rgba(110, 205, 199, 1), 260px 50px 0 0 rgba(110, 205, 199, 1),
  265px 50px 0 0 rgba(110, 205, 199, 1), 270px 50px 0 0 rgba(110, 205, 199, 1),
  275px 50px 0 0 rgba(110, 205, 199, 1), 280px 50px 0 0 rgba(110, 205, 199, 1),
  285px 50px 0 0 rgba(110, 205, 199, 1), 290px 50px 0 0 rgba(110, 205, 199, 1),
  295px 50px 0 0 rgba(110, 205, 199, 1), 300px 50px 0 0 rgba(110, 205, 199, 1),
  305px 50px 0 0 rgba(110, 205, 199, 1), 310px 50px 0 0 rgba(110, 205, 199, 1),
  315px 50px 0 0 rgba(110, 205, 199, 1), 320px 50px 0 0 rgba(110, 205, 199, 1),
  325px 50px 0 0 rgba(110, 205, 199, 1), 330px 50px 0 0 rgba(110, 205, 199, 1),
  335px 50px 0 0 rgba(110, 205, 199, 1), 340px 50px 0 0 rgba(110, 205, 199, 1),
  345px 50px 0 0 rgba(110, 205, 199, 1), 350px 50px 0 0 rgba(110, 205, 199, 1),
  355px 50px 0 0 rgba(110, 205, 199, 1), 360px 50px 0 0 rgba(110, 205, 199, 1),
  365px 50px 0 0 rgba(110, 205, 199, 1), 370px 50px 0 0 rgba(110, 205, 199, 1),
  375px 50px 0 0 rgba(110, 205, 199, 1), 380px 50px 0 0 rgba(110, 205, 199, 1),
  385px 50px 0 0 rgba(110, 205, 199, 1), 390px 50px 0 0 rgba(110, 205, 199, 1),
  395px 50px 0 0 rgba(110, 205, 199, 1), 400px 50px 0 0 rgba(110, 205, 199, 1),
  405px 50px 0 0 rgba(110, 205, 199, 1), 410px 50px 0 0 rgba(110, 205, 199, 1),
  415px 50px 0 0 rgba(110, 205, 199, 1), 420px 50px 0 0 rgba(110, 205, 199, 1),
  425px 50px 0 0 rgba(110, 205, 199, 1), 430px 50px 0 0 rgba(110, 205, 199, 1),
  435px 50px 0 0 rgba(110, 205, 199, 1), 440px 50px 0 0 rgba(110, 205, 199, 1),
  445px 50px 0 0 rgba(110, 205, 199, 1), 450px 50px 0 0 rgba(110, 205, 199, 1),
  455px 50px 0 0 rgba(110, 205, 199, 1), 460px 50px 0 0 rgba(110, 205, 199, 1),
  465px 50px 0 0 rgba(110, 205, 199, 1), 470px 50px 0 0 rgba(110, 205, 199, 1),
  475px 50px 0 0 rgba(110, 205, 199, 1), 480px 50px 0 0 rgba(110, 205, 199, 1),
  485px 50px 0 0 rgba(110, 205, 199, 1), 490px 50px 0 0 rgba(110, 205, 199, 1),
  495px 50px 0 0 rgba(110, 205, 199, 1), 500px 50px 0 0 rgba(110, 205, 199, 1),
  505px 50px 0 0 rgba(110, 205, 199, 1), 510px 50px 0 0 rgba(110, 205, 199, 1),
  515px 50px 0 0 rgba(110, 205, 199, 1), 520px 50px 0 0 rgba(110, 205, 199, 1),
  525px 50px 0 0 rgba(110, 205, 199, 1), 530px 50px 0 0 rgba(110, 205, 199, 1),
  535px 50px 0 0 rgba(110, 205, 199, 1), 540px 50px 0 0 rgba(110, 205, 199, 1),
  545px 50px 0 0 rgba(110, 205, 199, 1), 550px 50px 0 0 rgba(110, 205, 199, 1),
  555px 50px 0 0 rgba(110, 205, 199, 1), 560px 50px 0 0 rgba(110, 205, 199, 1),
  565px 50px 0 0 rgba(110, 205, 199, 1), 570px 50px 0 0 rgba(110, 205, 199, 1),
  575px 50px 0 0 rgba(110, 205, 199, 1), 580px 50px 0 0 rgba(110, 205, 199, 1),
  585px 50px 0 0 rgba(110, 205, 199, 1), 590px 50px 0 0 rgba(110, 205, 199, 1),
  595px 50px 0 0 rgba(110, 205, 199, 1), 600px 50px 0 0 rgba(110, 205, 199, 1),
  605px 50px 0 0 rgba(110, 205, 199, 1), 610px 50px 0 0 rgba(110, 205, 199, 1),
  615px 50px 0 0 rgba(110, 205, 199, 1), 620px 50px 0 0 rgba(110, 205, 199, 1),
  625px 50px 0 0 rgba(110, 205, 199, 1), 630px 50px 0 0 rgba(110, 205, 199, 1),
  635px 50px 0 0 rgba(110, 205, 199, 1), 640px 50px 0 0 rgba(110, 205, 199, 1),
  645px 50px 0 0 rgba(110, 205, 199, 1), 650px 50px 0 0 rgba(110, 205, 199, 1),
  655px 50px 0 0 rgba(110, 205, 199, 1), 660px 50px 0 0 rgba(110, 205, 199, 1),
  665px 50px 0 0 rgba(110, 205, 199, 1), 670px 50px 0 0 rgba(110, 205, 199, 1),
  675px 50px 0 0 rgba(110, 205, 199, 1), 680px 50px 0 0 rgba(110, 205, 199, 1),
  685px 50px 0 0 rgba(203, 109, 181, 1), 690px 50px 0 0 rgba(255, 205, 234, 1),
  695px 50px 0 0 rgba(255, 205, 234, 1), 700px 50px 0 0 rgba(168, 90, 150, 1),
  705px 50px 0 0 rgba(203, 109, 181, 1), 5px 55px 0 0 rgba(203, 109, 181, 1),
  10px 55px 0 0 rgba(252, 231, 243, 1), 15px 55px 0 0 rgba(255, 205, 234, 1),
  20px 55px 0 0 rgba(255, 205, 234, 1), 25px 55px 0 0 rgba(203, 109, 181, 1),
  30px 55px 0 0 rgba(110, 205, 199, 1), 35px 55px 0 0 rgba(110, 205, 199, 1),
  40px 55px 0 0 rgba(110, 205, 199, 1), 45px 55px 0 0 rgba(110, 205, 199, 1),
  50px 55px 0 0 rgba(110, 205, 199, 1), 55px 55px 0 0 rgba(110, 205, 199, 1),
  60px 55px 0 0 rgba(110, 205, 199, 1), 65px 55px 0 0 rgba(110, 205, 199, 1),
  70px 55px 0 0 rgba(110, 205, 199, 1), 75px 55px 0 0 rgba(110, 205, 199, 1),
  80px 55px 0 0 rgba(110, 205, 199, 1), 85px 55px 0 0 rgba(110, 205, 199, 1),
  90px 55px 0 0 rgba(110, 205, 199, 1), 95px 55px 0 0 rgba(110, 205, 199, 1),
  100px 55px 0 0 rgba(110, 205, 199, 1), 105px 55px 0 0 rgba(110, 205, 199, 1),
  110px 55px 0 0 rgba(110, 205, 199, 1), 115px 55px 0 0 rgba(110, 205, 199, 1),
  120px 55px 0 0 rgba(110, 205, 199, 1), 125px 55px 0 0 rgba(110, 205, 199, 1),
  130px 55px 0 0 rgba(110, 205, 199, 1), 135px 55px 0 0 rgba(110, 205, 199, 1),
  140px 55px 0 0 rgba(110, 205, 199, 1), 145px 55px 0 0 rgba(110, 205, 199, 1),
  150px 55px 0 0 rgba(110, 205, 199, 1), 155px 55px 0 0 rgba(110, 205, 199, 1),
  160px 55px 0 0 rgba(110, 205, 199, 1), 165px 55px 0 0 rgba(110, 205, 199, 1),
  170px 55px 0 0 rgba(110, 205, 199, 1), 175px 55px 0 0 rgba(110, 205, 199, 1),
  180px 55px 0 0 rgba(110, 205, 199, 1), 185px 55px 0 0 rgba(110, 205, 199, 1),
  190px 55px 0 0 rgba(110, 205, 199, 1), 195px 55px 0 0 rgba(110, 205, 199, 1),
  200px 55px 0 0 rgba(110, 205, 199, 1), 205px 55px 0 0 rgba(110, 205, 199, 1),
  210px 55px 0 0 rgba(110, 205, 199, 1), 215px 55px 0 0 rgba(110, 205, 199, 1),
  220px 55px 0 0 rgba(110, 205, 199, 1), 225px 55px 0 0 rgba(110, 205, 199, 1),
  230px 55px 0 0 rgba(110, 205, 199, 1), 235px 55px 0 0 rgba(110, 205, 199, 1),
  240px 55px 0 0 rgba(110, 205, 199, 1), 245px 55px 0 0 rgba(110, 205, 199, 1),
  250px 55px 0 0 rgba(110, 205, 199, 1), 255px 55px 0 0 rgba(110, 205, 199, 1),
  260px 55px 0 0 rgba(110, 205, 199, 1), 265px 55px 0 0 rgba(110, 205, 199, 1),
  270px 55px 0 0 rgba(110, 205, 199, 1), 275px 55px 0 0 rgba(110, 205, 199, 1),
  280px 55px 0 0 rgba(110, 205, 199, 1), 285px 55px 0 0 rgba(110, 205, 199, 1),
  290px 55px 0 0 rgba(110, 205, 199, 1), 295px 55px 0 0 rgba(110, 205, 199, 1),
  300px 55px 0 0 rgba(110, 205, 199, 1), 305px 55px 0 0 rgba(110, 205, 199, 1),
  310px 55px 0 0 rgba(110, 205, 199, 1), 315px 55px 0 0 rgba(110, 205, 199, 1),
  320px 55px 0 0 rgba(110, 205, 199, 1), 325px 55px 0 0 rgba(110, 205, 199, 1),
  330px 55px 0 0 rgba(110, 205, 199, 1), 335px 55px 0 0 rgba(110, 205, 199, 1),
  340px 55px 0 0 rgba(110, 205, 199, 1), 345px 55px 0 0 rgba(110, 205, 199, 1),
  350px 55px 0 0 rgba(110, 205, 199, 1), 355px 55px 0 0 rgba(110, 205, 199, 1),
  360px 55px 0 0 rgba(110, 205, 199, 1), 365px 55px 0 0 rgba(110, 205, 199, 1),
  370px 55px 0 0 rgba(110, 205, 199, 1), 375px 55px 0 0 rgba(110, 205, 199, 1),
  380px 55px 0 0 rgba(110, 205, 199, 1), 385px 55px 0 0 rgba(110, 205, 199, 1),
  390px 55px 0 0 rgba(110, 205, 199, 1), 395px 55px 0 0 rgba(110, 205, 199, 1),
  400px 55px 0 0 rgba(110, 205, 199, 1), 405px 55px 0 0 rgba(110, 205, 199, 1),
  410px 55px 0 0 rgba(110, 205, 199, 1), 415px 55px 0 0 rgba(110, 205, 199, 1),
  420px 55px 0 0 rgba(110, 205, 199, 1), 425px 55px 0 0 rgba(110, 205, 199, 1),
  430px 55px 0 0 rgba(110, 205, 199, 1), 435px 55px 0 0 rgba(110, 205, 199, 1),
  440px 55px 0 0 rgba(110, 205, 199, 1), 445px 55px 0 0 rgba(110, 205, 199, 1),
  450px 55px 0 0 rgba(110, 205, 199, 1), 455px 55px 0 0 rgba(110, 205, 199, 1),
  460px 55px 0 0 rgba(110, 205, 199, 1), 465px 55px 0 0 rgba(110, 205, 199, 1),
  470px 55px 0 0 rgba(110, 205, 199, 1), 475px 55px 0 0 rgba(110, 205, 199, 1),
  480px 55px 0 0 rgba(110, 205, 199, 1), 485px 55px 0 0 rgba(110, 205, 199, 1),
  490px 55px 0 0 rgba(110, 205, 199, 1), 495px 55px 0 0 rgba(110, 205, 199, 1),
  500px 55px 0 0 rgba(110, 205, 199, 1), 505px 55px 0 0 rgba(110, 205, 199, 1),
  510px 55px 0 0 rgba(110, 205, 199, 1), 515px 55px 0 0 rgba(110, 205, 199, 1),
  520px 55px 0 0 rgba(110, 205, 199, 1), 525px 55px 0 0 rgba(110, 205, 199, 1),
  530px 55px 0 0 rgba(110, 205, 199, 1), 535px 55px 0 0 rgba(110, 205, 199, 1),
  540px 55px 0 0 rgba(110, 205, 199, 1), 545px 55px 0 0 rgba(110, 205, 199, 1),
  550px 55px 0 0 rgba(110, 205, 199, 1), 555px 55px 0 0 rgba(110, 205, 199, 1),
  560px 55px 0 0 rgba(110, 205, 199, 1), 565px 55px 0 0 rgba(110, 205, 199, 1),
  570px 55px 0 0 rgba(110, 205, 199, 1), 575px 55px 0 0 rgba(110, 205, 199, 1),
  580px 55px 0 0 rgba(110, 205, 199, 1), 585px 55px 0 0 rgba(110, 205, 199, 1),
  590px 55px 0 0 rgba(110, 205, 199, 1), 595px 55px 0 0 rgba(110, 205, 199, 1),
  600px 55px 0 0 rgba(110, 205, 199, 1), 605px 55px 0 0 rgba(110, 205, 199, 1),
  610px 55px 0 0 rgba(110, 205, 199, 1), 615px 55px 0 0 rgba(110, 205, 199, 1),
  620px 55px 0 0 rgba(110, 205, 199, 1), 625px 55px 0 0 rgba(110, 205, 199, 1),
  630px 55px 0 0 rgba(110, 205, 199, 1), 635px 55px 0 0 rgba(110, 205, 199, 1),
  640px 55px 0 0 rgba(110, 205, 199, 1), 645px 55px 0 0 rgba(110, 205, 199, 1),
  650px 55px 0 0 rgba(110, 205, 199, 1), 655px 55px 0 0 rgba(110, 205, 199, 1),
  660px 55px 0 0 rgba(110, 205, 199, 1), 665px 55px 0 0 rgba(110, 205, 199, 1),
  670px 55px 0 0 rgba(110, 205, 199, 1), 675px 55px 0 0 rgba(110, 205, 199, 1),
  680px 55px 0 0 rgba(110, 205, 199, 1), 685px 55px 0 0 rgba(203, 109, 181, 1),
  690px 55px 0 0 rgba(255, 205, 234, 1), 695px 55px 0 0 rgba(255, 205, 234, 1),
  700px 55px 0 0 rgba(168, 90, 150, 1), 705px 55px 0 0 rgba(203, 109, 181, 1),
  5px 60px 0 0 rgba(203, 109, 181, 1), 10px 60px 0 0 rgba(252, 231, 243, 1),
  15px 60px 0 0 rgba(255, 205, 234, 1), 20px 60px 0 0 rgba(255, 205, 234, 1),
  25px 60px 0 0 rgba(203, 109, 181, 1), 30px 60px 0 0 rgba(110, 205, 199, 1),
  35px 60px 0 0 rgba(110, 205, 199, 1), 40px 60px 0 0 rgba(110, 205, 199, 1),
  45px 60px 0 0 rgba(110, 205, 199, 1), 50px 60px 0 0 rgba(110, 205, 199, 1),
  55px 60px 0 0 rgba(110, 205, 199, 1), 60px 60px 0 0 rgba(110, 205, 199, 1),
  65px 60px 0 0 rgba(110, 205, 199, 1), 70px 60px 0 0 rgba(110, 205, 199, 1),
  75px 60px 0 0 rgba(110, 205, 199, 1), 80px 60px 0 0 rgba(110, 205, 199, 1),
  85px 60px 0 0 rgba(110, 205, 199, 1), 90px 60px 0 0 rgba(110, 205, 199, 1),
  95px 60px 0 0 rgba(110, 205, 199, 1), 100px 60px 0 0 rgba(110, 205, 199, 1),
  105px 60px 0 0 rgba(110, 205, 199, 1), 110px 60px 0 0 rgba(110, 205, 199, 1),
  115px 60px 0 0 rgba(110, 205, 199, 1), 120px 60px 0 0 rgba(110, 205, 199, 1),
  125px 60px 0 0 rgba(110, 205, 199, 1), 130px 60px 0 0 rgba(110, 205, 199, 1),
  135px 60px 0 0 rgba(110, 205, 199, 1), 140px 60px 0 0 rgba(110, 205, 199, 1),
  145px 60px 0 0 rgba(110, 205, 199, 1), 150px 60px 0 0 rgba(110, 205, 199, 1),
  155px 60px 0 0 rgba(110, 205, 199, 1), 160px 60px 0 0 rgba(110, 205, 199, 1),
  165px 60px 0 0 rgba(110, 205, 199, 1), 170px 60px 0 0 rgba(110, 205, 199, 1),
  175px 60px 0 0 rgba(110, 205, 199, 1), 180px 60px 0 0 rgba(110, 205, 199, 1),
  185px 60px 0 0 rgba(110, 205, 199, 1), 190px 60px 0 0 rgba(110, 205, 199, 1),
  195px 60px 0 0 rgba(110, 205, 199, 1), 200px 60px 0 0 rgba(110, 205, 199, 1),
  205px 60px 0 0 rgba(110, 205, 199, 1), 210px 60px 0 0 rgba(110, 205, 199, 1),
  215px 60px 0 0 rgba(110, 205, 199, 1), 220px 60px 0 0 rgba(110, 205, 199, 1),
  225px 60px 0 0 rgba(110, 205, 199, 1), 230px 60px 0 0 rgba(110, 205, 199, 1),
  235px 60px 0 0 rgba(110, 205, 199, 1), 240px 60px 0 0 rgba(110, 205, 199, 1),
  245px 60px 0 0 rgba(110, 205, 199, 1), 250px 60px 0 0 rgba(110, 205, 199, 1),
  255px 60px 0 0 rgba(110, 205, 199, 1), 260px 60px 0 0 rgba(110, 205, 199, 1),
  265px 60px 0 0 rgba(110, 205, 199, 1), 270px 60px 0 0 rgba(110, 205, 199, 1),
  275px 60px 0 0 rgba(110, 205, 199, 1), 280px 60px 0 0 rgba(110, 205, 199, 1),
  285px 60px 0 0 rgba(110, 205, 199, 1), 290px 60px 0 0 rgba(110, 205, 199, 1),
  295px 60px 0 0 rgba(110, 205, 199, 1), 300px 60px 0 0 rgba(110, 205, 199, 1),
  305px 60px 0 0 rgba(110, 205, 199, 1), 310px 60px 0 0 rgba(110, 205, 199, 1),
  315px 60px 0 0 rgba(110, 205, 199, 1), 320px 60px 0 0 rgba(110, 205, 199, 1),
  325px 60px 0 0 rgba(110, 205, 199, 1), 330px 60px 0 0 rgba(110, 205, 199, 1),
  335px 60px 0 0 rgba(110, 205, 199, 1), 340px 60px 0 0 rgba(110, 205, 199, 1),
  345px 60px 0 0 rgba(110, 205, 199, 1), 350px 60px 0 0 rgba(110, 205, 199, 1),
  355px 60px 0 0 rgba(110, 205, 199, 1), 360px 60px 0 0 rgba(110, 205, 199, 1),
  365px 60px 0 0 rgba(110, 205, 199, 1), 370px 60px 0 0 rgba(110, 205, 199, 1),
  375px 60px 0 0 rgba(110, 205, 199, 1), 380px 60px 0 0 rgba(110, 205, 199, 1),
  385px 60px 0 0 rgba(110, 205, 199, 1), 390px 60px 0 0 rgba(110, 205, 199, 1),
  395px 60px 0 0 rgba(110, 205, 199, 1), 400px 60px 0 0 rgba(110, 205, 199, 1),
  405px 60px 0 0 rgba(110, 205, 199, 1), 410px 60px 0 0 rgba(110, 205, 199, 1),
  415px 60px 0 0 rgba(110, 205, 199, 1), 420px 60px 0 0 rgba(110, 205, 199, 1),
  425px 60px 0 0 rgba(110, 205, 199, 1), 430px 60px 0 0 rgba(110, 205, 199, 1),
  435px 60px 0 0 rgba(110, 205, 199, 1), 440px 60px 0 0 rgba(110, 205, 199, 1),
  445px 60px 0 0 rgba(110, 205, 199, 1), 450px 60px 0 0 rgba(110, 205, 199, 1),
  455px 60px 0 0 rgba(110, 205, 199, 1), 460px 60px 0 0 rgba(110, 205, 199, 1),
  465px 60px 0 0 rgba(110, 205, 199, 1), 470px 60px 0 0 rgba(110, 205, 199, 1),
  475px 60px 0 0 rgba(110, 205, 199, 1), 480px 60px 0 0 rgba(110, 205, 199, 1),
  485px 60px 0 0 rgba(110, 205, 199, 1), 490px 60px 0 0 rgba(110, 205, 199, 1),
  495px 60px 0 0 rgba(110, 205, 199, 1), 500px 60px 0 0 rgba(110, 205, 199, 1),
  505px 60px 0 0 rgba(110, 205, 199, 1), 510px 60px 0 0 rgba(110, 205, 199, 1),
  515px 60px 0 0 rgba(110, 205, 199, 1), 520px 60px 0 0 rgba(110, 205, 199, 1),
  525px 60px 0 0 rgba(110, 205, 199, 1), 530px 60px 0 0 rgba(110, 205, 199, 1),
  535px 60px 0 0 rgba(110, 205, 199, 1), 540px 60px 0 0 rgba(110, 205, 199, 1),
  545px 60px 0 0 rgba(110, 205, 199, 1), 550px 60px 0 0 rgba(110, 205, 199, 1),
  555px 60px 0 0 rgba(110, 205, 199, 1), 560px 60px 0 0 rgba(110, 205, 199, 1),
  565px 60px 0 0 rgba(110, 205, 199, 1), 570px 60px 0 0 rgba(110, 205, 199, 1),
  575px 60px 0 0 rgba(110, 205, 199, 1), 580px 60px 0 0 rgba(110, 205, 199, 1),
  585px 60px 0 0 rgba(110, 205, 199, 1), 590px 60px 0 0 rgba(110, 205, 199, 1),
  595px 60px 0 0 rgba(110, 205, 199, 1), 600px 60px 0 0 rgba(110, 205, 199, 1),
  605px 60px 0 0 rgba(110, 205, 199, 1), 610px 60px 0 0 rgba(110, 205, 199, 1),
  615px 60px 0 0 rgba(110, 205, 199, 1), 620px 60px 0 0 rgba(110, 205, 199, 1),
  625px 60px 0 0 rgba(110, 205, 199, 1), 630px 60px 0 0 rgba(110, 205, 199, 1),
  635px 60px 0 0 rgba(110, 205, 199, 1), 640px 60px 0 0 rgba(110, 205, 199, 1),
  645px 60px 0 0 rgba(110, 205, 199, 1), 650px 60px 0 0 rgba(110, 205, 199, 1),
  655px 60px 0 0 rgba(110, 205, 199, 1), 660px 60px 0 0 rgba(110, 205, 199, 1),
  665px 60px 0 0 rgba(110, 205, 199, 1), 670px 60px 0 0 rgba(110, 205, 199, 1),
  675px 60px 0 0 rgba(110, 205, 199, 1), 680px 60px 0 0 rgba(110, 205, 199, 1),
  685px 60px 0 0 rgba(203, 109, 181, 1), 690px 60px 0 0 rgba(255, 205, 234, 1),
  695px 60px 0 0 rgba(255, 205, 234, 1), 700px 60px 0 0 rgba(168, 90, 150, 1),
  705px 60px 0 0 rgba(203, 109, 181, 1), 5px 65px 0 0 rgba(203, 109, 181, 1),
  10px 65px 0 0 rgba(252, 231, 243, 1), 15px 65px 0 0 rgba(255, 205, 234, 1),
  20px 65px 0 0 rgba(255, 205, 234, 1), 25px 65px 0 0 rgba(203, 109, 181, 1),
  30px 65px 0 0 rgba(110, 205, 199, 1), 35px 65px 0 0 rgba(110, 205, 199, 1),
  40px 65px 0 0 rgba(110, 205, 199, 1), 45px 65px 0 0 rgba(110, 205, 199, 1),
  50px 65px 0 0 rgba(110, 205, 199, 1), 55px 65px 0 0 rgba(110, 205, 199, 1),
  60px 65px 0 0 rgba(110, 205, 199, 1), 65px 65px 0 0 rgba(110, 205, 199, 1),
  70px 65px 0 0 rgba(110, 205, 199, 1), 75px 65px 0 0 rgba(110, 205, 199, 1),
  80px 65px 0 0 rgba(110, 205, 199, 1), 85px 65px 0 0 rgba(110, 205, 199, 1),
  90px 65px 0 0 rgba(110, 205, 199, 1), 95px 65px 0 0 rgba(110, 205, 199, 1),
  100px 65px 0 0 rgba(110, 205, 199, 1), 105px 65px 0 0 rgba(110, 205, 199, 1),
  110px 65px 0 0 rgba(110, 205, 199, 1), 115px 65px 0 0 rgba(110, 205, 199, 1),
  120px 65px 0 0 rgba(110, 205, 199, 1), 125px 65px 0 0 rgba(110, 205, 199, 1),
  130px 65px 0 0 rgba(110, 205, 199, 1), 135px 65px 0 0 rgba(110, 205, 199, 1),
  140px 65px 0 0 rgba(110, 205, 199, 1), 145px 65px 0 0 rgba(110, 205, 199, 1),
  150px 65px 0 0 rgba(110, 205, 199, 1), 155px 65px 0 0 rgba(110, 205, 199, 1),
  160px 65px 0 0 rgba(110, 205, 199, 1), 165px 65px 0 0 rgba(110, 205, 199, 1),
  170px 65px 0 0 rgba(110, 205, 199, 1), 175px 65px 0 0 rgba(110, 205, 199, 1),
  180px 65px 0 0 rgba(110, 205, 199, 1), 185px 65px 0 0 rgba(110, 205, 199, 1),
  190px 65px 0 0 rgba(110, 205, 199, 1), 195px 65px 0 0 rgba(110, 205, 199, 1),
  200px 65px 0 0 rgba(110, 205, 199, 1), 205px 65px 0 0 rgba(110, 205, 199, 1),
  210px 65px 0 0 rgba(110, 205, 199, 1), 215px 65px 0 0 rgba(110, 205, 199, 1),
  220px 65px 0 0 rgba(110, 205, 199, 1), 225px 65px 0 0 rgba(110, 205, 199, 1),
  230px 65px 0 0 rgba(110, 205, 199, 1), 235px 65px 0 0 rgba(110, 205, 199, 1),
  240px 65px 0 0 rgba(110, 205, 199, 1), 245px 65px 0 0 rgba(110, 205, 199, 1),
  250px 65px 0 0 rgba(110, 205, 199, 1), 255px 65px 0 0 rgba(110, 205, 199, 1),
  260px 65px 0 0 rgba(110, 205, 199, 1), 265px 65px 0 0 rgba(110, 205, 199, 1),
  270px 65px 0 0 rgba(110, 205, 199, 1), 275px 65px 0 0 rgba(110, 205, 199, 1),
  280px 65px 0 0 rgba(110, 205, 199, 1), 285px 65px 0 0 rgba(110, 205, 199, 1),
  290px 65px 0 0 rgba(110, 205, 199, 1), 295px 65px 0 0 rgba(110, 205, 199, 1),
  300px 65px 0 0 rgba(110, 205, 199, 1), 305px 65px 0 0 rgba(110, 205, 199, 1),
  310px 65px 0 0 rgba(110, 205, 199, 1), 315px 65px 0 0 rgba(110, 205, 199, 1),
  320px 65px 0 0 rgba(110, 205, 199, 1), 325px 65px 0 0 rgba(110, 205, 199, 1),
  330px 65px 0 0 rgba(110, 205, 199, 1), 335px 65px 0 0 rgba(110, 205, 199, 1),
  340px 65px 0 0 rgba(110, 205, 199, 1), 345px 65px 0 0 rgba(110, 205, 199, 1),
  350px 65px 0 0 rgba(110, 205, 199, 1), 355px 65px 0 0 rgba(110, 205, 199, 1),
  360px 65px 0 0 rgba(110, 205, 199, 1), 365px 65px 0 0 rgba(110, 205, 199, 1),
  370px 65px 0 0 rgba(110, 205, 199, 1), 375px 65px 0 0 rgba(110, 205, 199, 1),
  380px 65px 0 0 rgba(110, 205, 199, 1), 385px 65px 0 0 rgba(110, 205, 199, 1),
  390px 65px 0 0 rgba(110, 205, 199, 1), 395px 65px 0 0 rgba(110, 205, 199, 1),
  400px 65px 0 0 rgba(110, 205, 199, 1), 405px 65px 0 0 rgba(110, 205, 199, 1),
  410px 65px 0 0 rgba(110, 205, 199, 1), 415px 65px 0 0 rgba(110, 205, 199, 1),
  420px 65px 0 0 rgba(110, 205, 199, 1), 425px 65px 0 0 rgba(110, 205, 199, 1),
  430px 65px 0 0 rgba(110, 205, 199, 1), 435px 65px 0 0 rgba(110, 205, 199, 1),
  440px 65px 0 0 rgba(110, 205, 199, 1), 445px 65px 0 0 rgba(110, 205, 199, 1),
  450px 65px 0 0 rgba(110, 205, 199, 1), 455px 65px 0 0 rgba(110, 205, 199, 1),
  460px 65px 0 0 rgba(110, 205, 199, 1), 465px 65px 0 0 rgba(110, 205, 199, 1),
  470px 65px 0 0 rgba(110, 205, 199, 1), 475px 65px 0 0 rgba(110, 205, 199, 1),
  480px 65px 0 0 rgba(110, 205, 199, 1), 485px 65px 0 0 rgba(110, 205, 199, 1),
  490px 65px 0 0 rgba(110, 205, 199, 1), 495px 65px 0 0 rgba(110, 205, 199, 1),
  500px 65px 0 0 rgba(110, 205, 199, 1), 505px 65px 0 0 rgba(110, 205, 199, 1),
  510px 65px 0 0 rgba(110, 205, 199, 1), 515px 65px 0 0 rgba(110, 205, 199, 1),
  520px 65px 0 0 rgba(110, 205, 199, 1), 525px 65px 0 0 rgba(110, 205, 199, 1),
  530px 65px 0 0 rgba(110, 205, 199, 1), 535px 65px 0 0 rgba(110, 205, 199, 1),
  540px 65px 0 0 rgba(110, 205, 199, 1), 545px 65px 0 0 rgba(110, 205, 199, 1),
  550px 65px 0 0 rgba(110, 205, 199, 1), 555px 65px 0 0 rgba(110, 205, 199, 1),
  560px 65px 0 0 rgba(110, 205, 199, 1), 565px 65px 0 0 rgba(110, 205, 199, 1),
  570px 65px 0 0 rgba(110, 205, 199, 1), 575px 65px 0 0 rgba(110, 205, 199, 1),
  580px 65px 0 0 rgba(110, 205, 199, 1), 585px 65px 0 0 rgba(110, 205, 199, 1),
  590px 65px 0 0 rgba(110, 205, 199, 1), 595px 65px 0 0 rgba(110, 205, 199, 1),
  600px 65px 0 0 rgba(110, 205, 199, 1), 605px 65px 0 0 rgba(110, 205, 199, 1),
  610px 65px 0 0 rgba(110, 205, 199, 1), 615px 65px 0 0 rgba(110, 205, 199, 1),
  620px 65px 0 0 rgba(110, 205, 199, 1), 625px 65px 0 0 rgba(110, 205, 199, 1),
  630px 65px 0 0 rgba(110, 205, 199, 1), 635px 65px 0 0 rgba(110, 205, 199, 1),
  640px 65px 0 0 rgba(110, 205, 199, 1), 645px 65px 0 0 rgba(110, 205, 199, 1),
  650px 65px 0 0 rgba(110, 205, 199, 1), 655px 65px 0 0 rgba(110, 205, 199, 1),
  660px 65px 0 0 rgba(110, 205, 199, 1), 665px 65px 0 0 rgba(110, 205, 199, 1),
  670px 65px 0 0 rgba(110, 205, 199, 1), 675px 65px 0 0 rgba(110, 205, 199, 1),
  680px 65px 0 0 rgba(110, 205, 199, 1), 685px 65px 0 0 rgba(203, 109, 181, 1),
  690px 65px 0 0 rgba(255, 205, 234, 1), 695px 65px 0 0 rgba(255, 205, 234, 1),
  700px 65px 0 0 rgba(168, 90, 150, 1), 705px 65px 0 0 rgba(203, 109, 181, 1),
  5px 70px 0 0 rgba(203, 109, 181, 1), 10px 70px 0 0 rgba(252, 231, 243, 1),
  15px 70px 0 0 rgba(255, 205, 234, 1), 20px 70px 0 0 rgba(255, 205, 234, 1),
  25px 70px 0 0 rgba(203, 109, 181, 1), 30px 70px 0 0 rgba(110, 205, 199, 1),
  35px 70px 0 0 rgba(110, 205, 199, 1), 40px 70px 0 0 rgba(110, 205, 199, 1),
  45px 70px 0 0 rgba(110, 205, 199, 1), 50px 70px 0 0 rgba(110, 205, 199, 1),
  55px 70px 0 0 rgba(110, 205, 199, 1), 60px 70px 0 0 rgba(110, 205, 199, 1),
  65px 70px 0 0 rgba(110, 205, 199, 1), 70px 70px 0 0 rgba(110, 205, 199, 1),
  75px 70px 0 0 rgba(110, 205, 199, 1), 80px 70px 0 0 rgba(110, 205, 199, 1),
  85px 70px 0 0 rgba(110, 205, 199, 1), 90px 70px 0 0 rgba(110, 205, 199, 1),
  95px 70px 0 0 rgba(110, 205, 199, 1), 100px 70px 0 0 rgba(110, 205, 199, 1),
  105px 70px 0 0 rgba(110, 205, 199, 1), 110px 70px 0 0 rgba(110, 205, 199, 1),
  115px 70px 0 0 rgba(110, 205, 199, 1), 120px 70px 0 0 rgba(110, 205, 199, 1),
  125px 70px 0 0 rgba(110, 205, 199, 1), 130px 70px 0 0 rgba(110, 205, 199, 1),
  135px 70px 0 0 rgba(110, 205, 199, 1), 140px 70px 0 0 rgba(110, 205, 199, 1),
  145px 70px 0 0 rgba(110, 205, 199, 1), 150px 70px 0 0 rgba(110, 205, 199, 1),
  155px 70px 0 0 rgba(110, 205, 199, 1), 160px 70px 0 0 rgba(110, 205, 199, 1),
  165px 70px 0 0 rgba(110, 205, 199, 1), 170px 70px 0 0 rgba(110, 205, 199, 1),
  175px 70px 0 0 rgba(110, 205, 199, 1), 180px 70px 0 0 rgba(110, 205, 199, 1),
  185px 70px 0 0 rgba(110, 205, 199, 1), 190px 70px 0 0 rgba(110, 205, 199, 1),
  195px 70px 0 0 rgba(110, 205, 199, 1), 200px 70px 0 0 rgba(110, 205, 199, 1),
  205px 70px 0 0 rgba(110, 205, 199, 1), 210px 70px 0 0 rgba(110, 205, 199, 1),
  215px 70px 0 0 rgba(110, 205, 199, 1), 220px 70px 0 0 rgba(110, 205, 199, 1),
  225px 70px 0 0 rgba(110, 205, 199, 1), 230px 70px 0 0 rgba(110, 205, 199, 1),
  235px 70px 0 0 rgba(110, 205, 199, 1), 240px 70px 0 0 rgba(110, 205, 199, 1),
  245px 70px 0 0 rgba(110, 205, 199, 1), 250px 70px 0 0 rgba(110, 205, 199, 1),
  255px 70px 0 0 rgba(110, 205, 199, 1), 260px 70px 0 0 rgba(110, 205, 199, 1),
  265px 70px 0 0 rgba(110, 205, 199, 1), 270px 70px 0 0 rgba(110, 205, 199, 1),
  275px 70px 0 0 rgba(110, 205, 199, 1), 280px 70px 0 0 rgba(110, 205, 199, 1),
  285px 70px 0 0 rgba(110, 205, 199, 1), 290px 70px 0 0 rgba(110, 205, 199, 1),
  295px 70px 0 0 rgba(110, 205, 199, 1), 300px 70px 0 0 rgba(110, 205, 199, 1),
  305px 70px 0 0 rgba(110, 205, 199, 1), 310px 70px 0 0 rgba(110, 205, 199, 1),
  315px 70px 0 0 rgba(110, 205, 199, 1), 320px 70px 0 0 rgba(110, 205, 199, 1),
  325px 70px 0 0 rgba(110, 205, 199, 1), 330px 70px 0 0 rgba(110, 205, 199, 1),
  335px 70px 0 0 rgba(110, 205, 199, 1), 340px 70px 0 0 rgba(110, 205, 199, 1),
  345px 70px 0 0 rgba(110, 205, 199, 1), 350px 70px 0 0 rgba(110, 205, 199, 1),
  355px 70px 0 0 rgba(110, 205, 199, 1), 360px 70px 0 0 rgba(110, 205, 199, 1),
  365px 70px 0 0 rgba(110, 205, 199, 1), 370px 70px 0 0 rgba(110, 205, 199, 1),
  375px 70px 0 0 rgba(110, 205, 199, 1), 380px 70px 0 0 rgba(110, 205, 199, 1),
  385px 70px 0 0 rgba(110, 205, 199, 1), 390px 70px 0 0 rgba(110, 205, 199, 1),
  395px 70px 0 0 rgba(110, 205, 199, 1), 400px 70px 0 0 rgba(110, 205, 199, 1),
  405px 70px 0 0 rgba(110, 205, 199, 1), 410px 70px 0 0 rgba(110, 205, 199, 1),
  415px 70px 0 0 rgba(110, 205, 199, 1), 420px 70px 0 0 rgba(110, 205, 199, 1),
  425px 70px 0 0 rgba(110, 205, 199, 1), 430px 70px 0 0 rgba(110, 205, 199, 1),
  435px 70px 0 0 rgba(110, 205, 199, 1), 440px 70px 0 0 rgba(110, 205, 199, 1),
  445px 70px 0 0 rgba(110, 205, 199, 1), 450px 70px 0 0 rgba(110, 205, 199, 1),
  455px 70px 0 0 rgba(110, 205, 199, 1), 460px 70px 0 0 rgba(110, 205, 199, 1),
  465px 70px 0 0 rgba(110, 205, 199, 1), 470px 70px 0 0 rgba(110, 205, 199, 1),
  475px 70px 0 0 rgba(110, 205, 199, 1), 480px 70px 0 0 rgba(110, 205, 199, 1),
  485px 70px 0 0 rgba(110, 205, 199, 1), 490px 70px 0 0 rgba(110, 205, 199, 1),
  495px 70px 0 0 rgba(110, 205, 199, 1), 500px 70px 0 0 rgba(110, 205, 199, 1),
  505px 70px 0 0 rgba(110, 205, 199, 1), 510px 70px 0 0 rgba(110, 205, 199, 1),
  515px 70px 0 0 rgba(110, 205, 199, 1), 520px 70px 0 0 rgba(110, 205, 199, 1),
  525px 70px 0 0 rgba(110, 205, 199, 1), 530px 70px 0 0 rgba(110, 205, 199, 1),
  535px 70px 0 0 rgba(110, 205, 199, 1), 540px 70px 0 0 rgba(110, 205, 199, 1),
  545px 70px 0 0 rgba(110, 205, 199, 1), 550px 70px 0 0 rgba(110, 205, 199, 1),
  555px 70px 0 0 rgba(110, 205, 199, 1), 560px 70px 0 0 rgba(110, 205, 199, 1),
  565px 70px 0 0 rgba(110, 205, 199, 1), 570px 70px 0 0 rgba(110, 205, 199, 1),
  575px 70px 0 0 rgba(110, 205, 199, 1), 580px 70px 0 0 rgba(110, 205, 199, 1),
  585px 70px 0 0 rgba(110, 205, 199, 1), 590px 70px 0 0 rgba(110, 205, 199, 1),
  595px 70px 0 0 rgba(110, 205, 199, 1), 600px 70px 0 0 rgba(110, 205, 199, 1),
  605px 70px 0 0 rgba(110, 205, 199, 1), 610px 70px 0 0 rgba(110, 205, 199, 1),
  615px 70px 0 0 rgba(110, 205, 199, 1), 620px 70px 0 0 rgba(110, 205, 199, 1),
  625px 70px 0 0 rgba(110, 205, 199, 1), 630px 70px 0 0 rgba(110, 205, 199, 1),
  635px 70px 0 0 rgba(110, 205, 199, 1), 640px 70px 0 0 rgba(110, 205, 199, 1),
  645px 70px 0 0 rgba(110, 205, 199, 1), 650px 70px 0 0 rgba(110, 205, 199, 1),
  655px 70px 0 0 rgba(110, 205, 199, 1), 660px 70px 0 0 rgba(110, 205, 199, 1),
  665px 70px 0 0 rgba(110, 205, 199, 1), 670px 70px 0 0 rgba(110, 205, 199, 1),
  675px 70px 0 0 rgba(110, 205, 199, 1), 680px 70px 0 0 rgba(110, 205, 199, 1),
  685px 70px 0 0 rgba(203, 109, 181, 1), 690px 70px 0 0 rgba(255, 205, 234, 1),
  695px 70px 0 0 rgba(255, 205, 234, 1), 700px 70px 0 0 rgba(168, 90, 150, 1),
  705px 70px 0 0 rgba(203, 109, 181, 1), 5px 75px 0 0 rgba(203, 109, 181, 1),
  10px 75px 0 0 rgba(252, 231, 243, 1), 15px 75px 0 0 rgba(255, 205, 234, 1),
  20px 75px 0 0 rgba(255, 205, 234, 1), 25px 75px 0 0 rgba(203, 109, 181, 1),
  30px 75px 0 0 rgba(110, 205, 199, 1), 35px 75px 0 0 rgba(110, 205, 199, 1),
  40px 75px 0 0 rgba(110, 205, 199, 1), 45px 75px 0 0 rgba(110, 205, 199, 1),
  50px 75px 0 0 rgba(110, 205, 199, 1), 55px 75px 0 0 rgba(110, 205, 199, 1),
  60px 75px 0 0 rgba(110, 205, 199, 1), 65px 75px 0 0 rgba(110, 205, 199, 1),
  70px 75px 0 0 rgba(110, 205, 199, 1), 75px 75px 0 0 rgba(110, 205, 199, 1),
  80px 75px 0 0 rgba(110, 205, 199, 1), 85px 75px 0 0 rgba(110, 205, 199, 1),
  90px 75px 0 0 rgba(110, 205, 199, 1), 95px 75px 0 0 rgba(110, 205, 199, 1),
  100px 75px 0 0 rgba(110, 205, 199, 1), 105px 75px 0 0 rgba(110, 205, 199, 1),
  110px 75px 0 0 rgba(110, 205, 199, 1), 115px 75px 0 0 rgba(110, 205, 199, 1),
  120px 75px 0 0 rgba(110, 205, 199, 1), 125px 75px 0 0 rgba(110, 205, 199, 1),
  130px 75px 0 0 rgba(110, 205, 199, 1), 135px 75px 0 0 rgba(110, 205, 199, 1),
  140px 75px 0 0 rgba(110, 205, 199, 1), 145px 75px 0 0 rgba(110, 205, 199, 1),
  150px 75px 0 0 rgba(110, 205, 199, 1), 155px 75px 0 0 rgba(110, 205, 199, 1),
  160px 75px 0 0 rgba(110, 205, 199, 1), 165px 75px 0 0 rgba(110, 205, 199, 1),
  170px 75px 0 0 rgba(110, 205, 199, 1), 175px 75px 0 0 rgba(110, 205, 199, 1),
  180px 75px 0 0 rgba(110, 205, 199, 1), 185px 75px 0 0 rgba(110, 205, 199, 1),
  190px 75px 0 0 rgba(110, 205, 199, 1), 195px 75px 0 0 rgba(110, 205, 199, 1),
  200px 75px 0 0 rgba(110, 205, 199, 1), 205px 75px 0 0 rgba(110, 205, 199, 1),
  210px 75px 0 0 rgba(110, 205, 199, 1), 215px 75px 0 0 rgba(110, 205, 199, 1),
  220px 75px 0 0 rgba(110, 205, 199, 1), 225px 75px 0 0 rgba(110, 205, 199, 1),
  230px 75px 0 0 rgba(110, 205, 199, 1), 235px 75px 0 0 rgba(110, 205, 199, 1),
  240px 75px 0 0 rgba(110, 205, 199, 1), 245px 75px 0 0 rgba(110, 205, 199, 1),
  250px 75px 0 0 rgba(110, 205, 199, 1), 255px 75px 0 0 rgba(110, 205, 199, 1),
  260px 75px 0 0 rgba(110, 205, 199, 1), 265px 75px 0 0 rgba(110, 205, 199, 1),
  270px 75px 0 0 rgba(110, 205, 199, 1), 275px 75px 0 0 rgba(110, 205, 199, 1),
  280px 75px 0 0 rgba(110, 205, 199, 1), 285px 75px 0 0 rgba(110, 205, 199, 1),
  290px 75px 0 0 rgba(110, 205, 199, 1), 295px 75px 0 0 rgba(110, 205, 199, 1),
  300px 75px 0 0 rgba(110, 205, 199, 1), 305px 75px 0 0 rgba(110, 205, 199, 1),
  310px 75px 0 0 rgba(110, 205, 199, 1), 315px 75px 0 0 rgba(110, 205, 199, 1),
  320px 75px 0 0 rgba(110, 205, 199, 1), 325px 75px 0 0 rgba(110, 205, 199, 1),
  330px 75px 0 0 rgba(110, 205, 199, 1), 335px 75px 0 0 rgba(110, 205, 199, 1),
  340px 75px 0 0 rgba(110, 205, 199, 1), 345px 75px 0 0 rgba(110, 205, 199, 1),
  350px 75px 0 0 rgba(110, 205, 199, 1), 355px 75px 0 0 rgba(110, 205, 199, 1),
  360px 75px 0 0 rgba(110, 205, 199, 1), 365px 75px 0 0 rgba(110, 205, 199, 1),
  370px 75px 0 0 rgba(110, 205, 199, 1), 375px 75px 0 0 rgba(110, 205, 199, 1),
  380px 75px 0 0 rgba(110, 205, 199, 1), 385px 75px 0 0 rgba(110, 205, 199, 1),
  390px 75px 0 0 rgba(110, 205, 199, 1), 395px 75px 0 0 rgba(110, 205, 199, 1),
  400px 75px 0 0 rgba(110, 205, 199, 1), 405px 75px 0 0 rgba(110, 205, 199, 1),
  410px 75px 0 0 rgba(110, 205, 199, 1), 415px 75px 0 0 rgba(110, 205, 199, 1),
  420px 75px 0 0 rgba(110, 205, 199, 1), 425px 75px 0 0 rgba(110, 205, 199, 1),
  430px 75px 0 0 rgba(110, 205, 199, 1), 435px 75px 0 0 rgba(110, 205, 199, 1),
  440px 75px 0 0 rgba(110, 205, 199, 1), 445px 75px 0 0 rgba(110, 205, 199, 1),
  450px 75px 0 0 rgba(110, 205, 199, 1), 455px 75px 0 0 rgba(110, 205, 199, 1),
  460px 75px 0 0 rgba(110, 205, 199, 1), 465px 75px 0 0 rgba(110, 205, 199, 1),
  470px 75px 0 0 rgba(110, 205, 199, 1), 475px 75px 0 0 rgba(110, 205, 199, 1),
  480px 75px 0 0 rgba(110, 205, 199, 1), 485px 75px 0 0 rgba(110, 205, 199, 1),
  490px 75px 0 0 rgba(110, 205, 199, 1), 495px 75px 0 0 rgba(110, 205, 199, 1),
  500px 75px 0 0 rgba(110, 205, 199, 1), 505px 75px 0 0 rgba(110, 205, 199, 1),
  510px 75px 0 0 rgba(110, 205, 199, 1), 515px 75px 0 0 rgba(110, 205, 199, 1),
  520px 75px 0 0 rgba(110, 205, 199, 1), 525px 75px 0 0 rgba(110, 205, 199, 1),
  530px 75px 0 0 rgba(110, 205, 199, 1), 535px 75px 0 0 rgba(110, 205, 199, 1),
  540px 75px 0 0 rgba(110, 205, 199, 1), 545px 75px 0 0 rgba(110, 205, 199, 1),
  550px 75px 0 0 rgba(110, 205, 199, 1), 555px 75px 0 0 rgba(110, 205, 199, 1),
  560px 75px 0 0 rgba(110, 205, 199, 1), 565px 75px 0 0 rgba(110, 205, 199, 1),
  570px 75px 0 0 rgba(110, 205, 199, 1), 575px 75px 0 0 rgba(110, 205, 199, 1),
  580px 75px 0 0 rgba(110, 205, 199, 1), 585px 75px 0 0 rgba(110, 205, 199, 1),
  590px 75px 0 0 rgba(110, 205, 199, 1), 595px 75px 0 0 rgba(110, 205, 199, 1),
  600px 75px 0 0 rgba(110, 205, 199, 1), 605px 75px 0 0 rgba(110, 205, 199, 1),
  610px 75px 0 0 rgba(110, 205, 199, 1), 615px 75px 0 0 rgba(110, 205, 199, 1),
  620px 75px 0 0 rgba(110, 205, 199, 1), 625px 75px 0 0 rgba(110, 205, 199, 1),
  630px 75px 0 0 rgba(110, 205, 199, 1), 635px 75px 0 0 rgba(110, 205, 199, 1),
  640px 75px 0 0 rgba(110, 205, 199, 1), 645px 75px 0 0 rgba(110, 205, 199, 1),
  650px 75px 0 0 rgba(110, 205, 199, 1), 655px 75px 0 0 rgba(110, 205, 199, 1),
  660px 75px 0 0 rgba(110, 205, 199, 1), 665px 75px 0 0 rgba(110, 205, 199, 1),
  670px 75px 0 0 rgba(110, 205, 199, 1), 675px 75px 0 0 rgba(110, 205, 199, 1),
  680px 75px 0 0 rgba(110, 205, 199, 1), 685px 75px 0 0 rgba(203, 109, 181, 1),
  690px 75px 0 0 rgba(255, 205, 234, 1), 695px 75px 0 0 rgba(255, 205, 234, 1),
  700px 75px 0 0 rgba(168, 90, 150, 1), 705px 75px 0 0 rgba(203, 109, 181, 1),
  5px 80px 0 0 rgba(203, 109, 181, 1), 10px 80px 0 0 rgba(252, 231, 243, 1),
  15px 80px 0 0 rgba(255, 205, 234, 1), 20px 80px 0 0 rgba(255, 205, 234, 1),
  25px 80px 0 0 rgba(203, 109, 181, 1), 30px 80px 0 0 rgba(110, 205, 199, 1),
  35px 80px 0 0 rgba(110, 205, 199, 1), 40px 80px 0 0 rgba(110, 205, 199, 1),
  45px 80px 0 0 rgba(110, 205, 199, 1), 50px 80px 0 0 rgba(110, 205, 199, 1),
  55px 80px 0 0 rgba(110, 205, 199, 1), 60px 80px 0 0 rgba(110, 205, 199, 1),
  65px 80px 0 0 rgba(110, 205, 199, 1), 70px 80px 0 0 rgba(110, 205, 199, 1),
  75px 80px 0 0 rgba(110, 205, 199, 1), 80px 80px 0 0 rgba(110, 205, 199, 1),
  85px 80px 0 0 rgba(110, 205, 199, 1), 90px 80px 0 0 rgba(110, 205, 199, 1),
  95px 80px 0 0 rgba(110, 205, 199, 1), 100px 80px 0 0 rgba(110, 205, 199, 1),
  105px 80px 0 0 rgba(110, 205, 199, 1), 110px 80px 0 0 rgba(110, 205, 199, 1),
  115px 80px 0 0 rgba(110, 205, 199, 1), 120px 80px 0 0 rgba(110, 205, 199, 1),
  125px 80px 0 0 rgba(110, 205, 199, 1), 130px 80px 0 0 rgba(110, 205, 199, 1),
  135px 80px 0 0 rgba(110, 205, 199, 1), 140px 80px 0 0 rgba(110, 205, 199, 1),
  145px 80px 0 0 rgba(110, 205, 199, 1), 150px 80px 0 0 rgba(110, 205, 199, 1),
  155px 80px 0 0 rgba(110, 205, 199, 1), 160px 80px 0 0 rgba(110, 205, 199, 1),
  165px 80px 0 0 rgba(110, 205, 199, 1), 170px 80px 0 0 rgba(110, 205, 199, 1),
  175px 80px 0 0 rgba(110, 205, 199, 1), 180px 80px 0 0 rgba(110, 205, 199, 1),
  185px 80px 0 0 rgba(110, 205, 199, 1), 190px 80px 0 0 rgba(110, 205, 199, 1),
  195px 80px 0 0 rgba(110, 205, 199, 1), 200px 80px 0 0 rgba(110, 205, 199, 1),
  205px 80px 0 0 rgba(110, 205, 199, 1), 210px 80px 0 0 rgba(110, 205, 199, 1),
  215px 80px 0 0 rgba(110, 205, 199, 1), 220px 80px 0 0 rgba(110, 205, 199, 1),
  225px 80px 0 0 rgba(110, 205, 199, 1), 230px 80px 0 0 rgba(110, 205, 199, 1),
  235px 80px 0 0 rgba(110, 205, 199, 1), 240px 80px 0 0 rgba(110, 205, 199, 1),
  245px 80px 0 0 rgba(110, 205, 199, 1), 250px 80px 0 0 rgba(110, 205, 199, 1),
  255px 80px 0 0 rgba(110, 205, 199, 1), 260px 80px 0 0 rgba(110, 205, 199, 1),
  265px 80px 0 0 rgba(110, 205, 199, 1), 270px 80px 0 0 rgba(110, 205, 199, 1),
  275px 80px 0 0 rgba(110, 205, 199, 1), 280px 80px 0 0 rgba(110, 205, 199, 1),
  285px 80px 0 0 rgba(110, 205, 199, 1), 290px 80px 0 0 rgba(110, 205, 199, 1),
  295px 80px 0 0 rgba(110, 205, 199, 1), 300px 80px 0 0 rgba(110, 205, 199, 1),
  305px 80px 0 0 rgba(110, 205, 199, 1), 310px 80px 0 0 rgba(110, 205, 199, 1),
  315px 80px 0 0 rgba(110, 205, 199, 1), 320px 80px 0 0 rgba(110, 205, 199, 1),
  325px 80px 0 0 rgba(110, 205, 199, 1), 330px 80px 0 0 rgba(110, 205, 199, 1),
  335px 80px 0 0 rgba(110, 205, 199, 1), 340px 80px 0 0 rgba(110, 205, 199, 1),
  345px 80px 0 0 rgba(110, 205, 199, 1), 350px 80px 0 0 rgba(110, 205, 199, 1),
  355px 80px 0 0 rgba(110, 205, 199, 1), 360px 80px 0 0 rgba(110, 205, 199, 1),
  365px 80px 0 0 rgba(110, 205, 199, 1), 370px 80px 0 0 rgba(110, 205, 199, 1),
  375px 80px 0 0 rgba(110, 205, 199, 1), 380px 80px 0 0 rgba(110, 205, 199, 1),
  385px 80px 0 0 rgba(110, 205, 199, 1), 390px 80px 0 0 rgba(110, 205, 199, 1),
  395px 80px 0 0 rgba(110, 205, 199, 1), 400px 80px 0 0 rgba(110, 205, 199, 1),
  405px 80px 0 0 rgba(110, 205, 199, 1), 410px 80px 0 0 rgba(110, 205, 199, 1),
  415px 80px 0 0 rgba(110, 205, 199, 1), 420px 80px 0 0 rgba(110, 205, 199, 1),
  425px 80px 0 0 rgba(110, 205, 199, 1), 430px 80px 0 0 rgba(110, 205, 199, 1),
  435px 80px 0 0 rgba(110, 205, 199, 1), 440px 80px 0 0 rgba(110, 205, 199, 1),
  445px 80px 0 0 rgba(110, 205, 199, 1), 450px 80px 0 0 rgba(110, 205, 199, 1),
  455px 80px 0 0 rgba(110, 205, 199, 1), 460px 80px 0 0 rgba(110, 205, 199, 1),
  465px 80px 0 0 rgba(110, 205, 199, 1), 470px 80px 0 0 rgba(110, 205, 199, 1),
  475px 80px 0 0 rgba(110, 205, 199, 1), 480px 80px 0 0 rgba(110, 205, 199, 1),
  485px 80px 0 0 rgba(110, 205, 199, 1), 490px 80px 0 0 rgba(110, 205, 199, 1),
  495px 80px 0 0 rgba(110, 205, 199, 1), 500px 80px 0 0 rgba(110, 205, 199, 1),
  505px 80px 0 0 rgba(110, 205, 199, 1), 510px 80px 0 0 rgba(110, 205, 199, 1),
  515px 80px 0 0 rgba(110, 205, 199, 1), 520px 80px 0 0 rgba(110, 205, 199, 1),
  525px 80px 0 0 rgba(110, 205, 199, 1), 530px 80px 0 0 rgba(110, 205, 199, 1),
  535px 80px 0 0 rgba(110, 205, 199, 1), 540px 80px 0 0 rgba(110, 205, 199, 1),
  545px 80px 0 0 rgba(110, 205, 199, 1), 550px 80px 0 0 rgba(110, 205, 199, 1),
  555px 80px 0 0 rgba(110, 205, 199, 1), 560px 80px 0 0 rgba(110, 205, 199, 1),
  565px 80px 0 0 rgba(110, 205, 199, 1), 570px 80px 0 0 rgba(110, 205, 199, 1),
  575px 80px 0 0 rgba(110, 205, 199, 1), 580px 80px 0 0 rgba(110, 205, 199, 1),
  585px 80px 0 0 rgba(110, 205, 199, 1), 590px 80px 0 0 rgba(110, 205, 199, 1),
  595px 80px 0 0 rgba(110, 205, 199, 1), 600px 80px 0 0 rgba(110, 205, 199, 1),
  605px 80px 0 0 rgba(110, 205, 199, 1), 610px 80px 0 0 rgba(110, 205, 199, 1),
  615px 80px 0 0 rgba(110, 205, 199, 1), 620px 80px 0 0 rgba(110, 205, 199, 1),
  625px 80px 0 0 rgba(110, 205, 199, 1), 630px 80px 0 0 rgba(110, 205, 199, 1),
  635px 80px 0 0 rgba(110, 205, 199, 1), 640px 80px 0 0 rgba(110, 205, 199, 1),
  645px 80px 0 0 rgba(110, 205, 199, 1), 650px 80px 0 0 rgba(110, 205, 199, 1),
  655px 80px 0 0 rgba(110, 205, 199, 1), 660px 80px 0 0 rgba(110, 205, 199, 1),
  665px 80px 0 0 rgba(110, 205, 199, 1), 670px 80px 0 0 rgba(110, 205, 199, 1),
  675px 80px 0 0 rgba(110, 205, 199, 1), 680px 80px 0 0 rgba(110, 205, 199, 1),
  685px 80px 0 0 rgba(203, 109, 181, 1), 690px 80px 0 0 rgba(255, 205, 234, 1),
  695px 80px 0 0 rgba(255, 205, 234, 1), 700px 80px 0 0 rgba(168, 90, 150, 1),
  705px 80px 0 0 rgba(203, 109, 181, 1), 5px 85px 0 0 rgba(203, 109, 181, 1),
  10px 85px 0 0 rgba(252, 231, 243, 1), 15px 85px 0 0 rgba(255, 205, 234, 1),
  20px 85px 0 0 rgba(255, 205, 234, 1), 25px 85px 0 0 rgba(203, 109, 181, 1),
  30px 85px 0 0 rgba(110, 205, 199, 1), 35px 85px 0 0 rgba(110, 205, 199, 1),
  40px 85px 0 0 rgba(110, 205, 199, 1), 45px 85px 0 0 rgba(110, 205, 199, 1),
  50px 85px 0 0 rgba(110, 205, 199, 1), 55px 85px 0 0 rgba(110, 205, 199, 1),
  60px 85px 0 0 rgba(110, 205, 199, 1), 65px 85px 0 0 rgba(110, 205, 199, 1),
  70px 85px 0 0 rgba(110, 205, 199, 1), 75px 85px 0 0 rgba(110, 205, 199, 1),
  80px 85px 0 0 rgba(110, 205, 199, 1), 85px 85px 0 0 rgba(110, 205, 199, 1),
  90px 85px 0 0 rgba(110, 205, 199, 1), 95px 85px 0 0 rgba(110, 205, 199, 1),
  100px 85px 0 0 rgba(110, 205, 199, 1), 105px 85px 0 0 rgba(110, 205, 199, 1),
  110px 85px 0 0 rgba(110, 205, 199, 1), 115px 85px 0 0 rgba(110, 205, 199, 1),
  120px 85px 0 0 rgba(110, 205, 199, 1), 125px 85px 0 0 rgba(110, 205, 199, 1),
  130px 85px 0 0 rgba(110, 205, 199, 1), 135px 85px 0 0 rgba(110, 205, 199, 1),
  140px 85px 0 0 rgba(110, 205, 199, 1), 145px 85px 0 0 rgba(110, 205, 199, 1),
  150px 85px 0 0 rgba(110, 205, 199, 1), 155px 85px 0 0 rgba(110, 205, 199, 1),
  160px 85px 0 0 rgba(110, 205, 199, 1), 165px 85px 0 0 rgba(110, 205, 199, 1),
  170px 85px 0 0 rgba(110, 205, 199, 1), 175px 85px 0 0 rgba(110, 205, 199, 1),
  180px 85px 0 0 rgba(110, 205, 199, 1), 185px 85px 0 0 rgba(110, 205, 199, 1),
  190px 85px 0 0 rgba(110, 205, 199, 1), 195px 85px 0 0 rgba(110, 205, 199, 1),
  200px 85px 0 0 rgba(110, 205, 199, 1), 205px 85px 0 0 rgba(110, 205, 199, 1),
  210px 85px 0 0 rgba(110, 205, 199, 1), 215px 85px 0 0 rgba(110, 205, 199, 1),
  220px 85px 0 0 rgba(110, 205, 199, 1), 225px 85px 0 0 rgba(110, 205, 199, 1),
  230px 85px 0 0 rgba(110, 205, 199, 1), 235px 85px 0 0 rgba(110, 205, 199, 1),
  240px 85px 0 0 rgba(110, 205, 199, 1), 245px 85px 0 0 rgba(110, 205, 199, 1),
  250px 85px 0 0 rgba(110, 205, 199, 1), 255px 85px 0 0 rgba(110, 205, 199, 1),
  260px 85px 0 0 rgba(110, 205, 199, 1), 265px 85px 0 0 rgba(110, 205, 199, 1),
  270px 85px 0 0 rgba(110, 205, 199, 1), 275px 85px 0 0 rgba(110, 205, 199, 1),
  280px 85px 0 0 rgba(110, 205, 199, 1), 285px 85px 0 0 rgba(110, 205, 199, 1),
  290px 85px 0 0 rgba(110, 205, 199, 1), 295px 85px 0 0 rgba(110, 205, 199, 1),
  300px 85px 0 0 rgba(110, 205, 199, 1), 305px 85px 0 0 rgba(110, 205, 199, 1),
  310px 85px 0 0 rgba(110, 205, 199, 1), 315px 85px 0 0 rgba(110, 205, 199, 1),
  320px 85px 0 0 rgba(110, 205, 199, 1), 325px 85px 0 0 rgba(110, 205, 199, 1),
  330px 85px 0 0 rgba(110, 205, 199, 1), 335px 85px 0 0 rgba(110, 205, 199, 1),
  340px 85px 0 0 rgba(110, 205, 199, 1), 345px 85px 0 0 rgba(110, 205, 199, 1),
  350px 85px 0 0 rgba(110, 205, 199, 1), 355px 85px 0 0 rgba(110, 205, 199, 1),
  360px 85px 0 0 rgba(110, 205, 199, 1), 365px 85px 0 0 rgba(110, 205, 199, 1),
  370px 85px 0 0 rgba(110, 205, 199, 1), 375px 85px 0 0 rgba(110, 205, 199, 1),
  380px 85px 0 0 rgba(110, 205, 199, 1), 385px 85px 0 0 rgba(110, 205, 199, 1),
  390px 85px 0 0 rgba(110, 205, 199, 1), 395px 85px 0 0 rgba(110, 205, 199, 1),
  400px 85px 0 0 rgba(110, 205, 199, 1), 405px 85px 0 0 rgba(110, 205, 199, 1),
  410px 85px 0 0 rgba(110, 205, 199, 1), 415px 85px 0 0 rgba(110, 205, 199, 1),
  420px 85px 0 0 rgba(110, 205, 199, 1), 425px 85px 0 0 rgba(110, 205, 199, 1),
  430px 85px 0 0 rgba(110, 205, 199, 1), 435px 85px 0 0 rgba(110, 205, 199, 1),
  440px 85px 0 0 rgba(110, 205, 199, 1), 445px 85px 0 0 rgba(110, 205, 199, 1),
  450px 85px 0 0 rgba(110, 205, 199, 1), 455px 85px 0 0 rgba(110, 205, 199, 1),
  460px 85px 0 0 rgba(110, 205, 199, 1), 465px 85px 0 0 rgba(110, 205, 199, 1),
  470px 85px 0 0 rgba(110, 205, 199, 1), 475px 85px 0 0 rgba(110, 205, 199, 1),
  480px 85px 0 0 rgba(110, 205, 199, 1), 485px 85px 0 0 rgba(110, 205, 199, 1),
  490px 85px 0 0 rgba(110, 205, 199, 1), 495px 85px 0 0 rgba(110, 205, 199, 1),
  500px 85px 0 0 rgba(110, 205, 199, 1), 505px 85px 0 0 rgba(110, 205, 199, 1),
  510px 85px 0 0 rgba(110, 205, 199, 1), 515px 85px 0 0 rgba(110, 205, 199, 1),
  520px 85px 0 0 rgba(110, 205, 199, 1), 525px 85px 0 0 rgba(110, 205, 199, 1),
  530px 85px 0 0 rgba(110, 205, 199, 1), 535px 85px 0 0 rgba(110, 205, 199, 1),
  540px 85px 0 0 rgba(110, 205, 199, 1), 545px 85px 0 0 rgba(110, 205, 199, 1),
  550px 85px 0 0 rgba(110, 205, 199, 1), 555px 85px 0 0 rgba(110, 205, 199, 1),
  560px 85px 0 0 rgba(110, 205, 199, 1), 565px 85px 0 0 rgba(110, 205, 199, 1),
  570px 85px 0 0 rgba(110, 205, 199, 1), 575px 85px 0 0 rgba(110, 205, 199, 1),
  580px 85px 0 0 rgba(110, 205, 199, 1), 585px 85px 0 0 rgba(110, 205, 199, 1),
  590px 85px 0 0 rgba(110, 205, 199, 1), 595px 85px 0 0 rgba(110, 205, 199, 1),
  600px 85px 0 0 rgba(110, 205, 199, 1), 605px 85px 0 0 rgba(110, 205, 199, 1),
  610px 85px 0 0 rgba(110, 205, 199, 1), 615px 85px 0 0 rgba(110, 205, 199, 1),
  620px 85px 0 0 rgba(110, 205, 199, 1), 625px 85px 0 0 rgba(110, 205, 199, 1),
  630px 85px 0 0 rgba(110, 205, 199, 1), 635px 85px 0 0 rgba(110, 205, 199, 1),
  640px 85px 0 0 rgba(110, 205, 199, 1), 645px 85px 0 0 rgba(110, 205, 199, 1),
  650px 85px 0 0 rgba(110, 205, 199, 1), 655px 85px 0 0 rgba(110, 205, 199, 1),
  660px 85px 0 0 rgba(110, 205, 199, 1), 665px 85px 0 0 rgba(110, 205, 199, 1),
  670px 85px 0 0 rgba(110, 205, 199, 1), 675px 85px 0 0 rgba(110, 205, 199, 1),
  680px 85px 0 0 rgba(110, 205, 199, 1), 685px 85px 0 0 rgba(203, 109, 181, 1),
  690px 85px 0 0 rgba(255, 205, 234, 1), 695px 85px 0 0 rgba(255, 205, 234, 1),
  700px 85px 0 0 rgba(168, 90, 150, 1), 705px 85px 0 0 rgba(203, 109, 181, 1),
  5px 90px 0 0 rgba(203, 109, 181, 1), 10px 90px 0 0 rgba(252, 231, 243, 1),
  15px 90px 0 0 rgba(255, 205, 234, 1), 20px 90px 0 0 rgba(255, 205, 234, 1),
  25px 90px 0 0 rgba(203, 109, 181, 1), 30px 90px 0 0 rgba(110, 205, 199, 1),
  35px 90px 0 0 rgba(110, 205, 199, 1), 40px 90px 0 0 rgba(110, 205, 199, 1),
  45px 90px 0 0 rgba(110, 205, 199, 1), 50px 90px 0 0 rgba(110, 205, 199, 1),
  55px 90px 0 0 rgba(110, 205, 199, 1), 60px 90px 0 0 rgba(110, 205, 199, 1),
  65px 90px 0 0 rgba(110, 205, 199, 1), 70px 90px 0 0 rgba(110, 205, 199, 1),
  75px 90px 0 0 rgba(110, 205, 199, 1), 80px 90px 0 0 rgba(110, 205, 199, 1),
  85px 90px 0 0 rgba(110, 205, 199, 1), 90px 90px 0 0 rgba(110, 205, 199, 1),
  95px 90px 0 0 rgba(110, 205, 199, 1), 100px 90px 0 0 rgba(110, 205, 199, 1),
  105px 90px 0 0 rgba(110, 205, 199, 1), 110px 90px 0 0 rgba(110, 205, 199, 1),
  115px 90px 0 0 rgba(110, 205, 199, 1), 120px 90px 0 0 rgba(110, 205, 199, 1),
  125px 90px 0 0 rgba(110, 205, 199, 1), 130px 90px 0 0 rgba(110, 205, 199, 1),
  135px 90px 0 0 rgba(110, 205, 199, 1), 140px 90px 0 0 rgba(110, 205, 199, 1),
  145px 90px 0 0 rgba(110, 205, 199, 1), 150px 90px 0 0 rgba(110, 205, 199, 1),
  155px 90px 0 0 rgba(110, 205, 199, 1), 160px 90px 0 0 rgba(110, 205, 199, 1),
  165px 90px 0 0 rgba(110, 205, 199, 1), 170px 90px 0 0 rgba(110, 205, 199, 1),
  175px 90px 0 0 rgba(110, 205, 199, 1), 180px 90px 0 0 rgba(110, 205, 199, 1),
  185px 90px 0 0 rgba(110, 205, 199, 1), 190px 90px 0 0 rgba(110, 205, 199, 1),
  195px 90px 0 0 rgba(110, 205, 199, 1), 200px 90px 0 0 rgba(110, 205, 199, 1),
  205px 90px 0 0 rgba(110, 205, 199, 1), 210px 90px 0 0 rgba(110, 205, 199, 1),
  215px 90px 0 0 rgba(110, 205, 199, 1), 220px 90px 0 0 rgba(110, 205, 199, 1),
  225px 90px 0 0 rgba(110, 205, 199, 1), 230px 90px 0 0 rgba(110, 205, 199, 1),
  235px 90px 0 0 rgba(110, 205, 199, 1), 240px 90px 0 0 rgba(110, 205, 199, 1),
  245px 90px 0 0 rgba(110, 205, 199, 1), 250px 90px 0 0 rgba(110, 205, 199, 1),
  255px 90px 0 0 rgba(110, 205, 199, 1), 260px 90px 0 0 rgba(110, 205, 199, 1),
  265px 90px 0 0 rgba(110, 205, 199, 1), 270px 90px 0 0 rgba(110, 205, 199, 1),
  275px 90px 0 0 rgba(110, 205, 199, 1), 280px 90px 0 0 rgba(110, 205, 199, 1),
  285px 90px 0 0 rgba(110, 205, 199, 1), 290px 90px 0 0 rgba(110, 205, 199, 1),
  295px 90px 0 0 rgba(110, 205, 199, 1), 300px 90px 0 0 rgba(110, 205, 199, 1),
  305px 90px 0 0 rgba(110, 205, 199, 1), 310px 90px 0 0 rgba(110, 205, 199, 1),
  315px 90px 0 0 rgba(110, 205, 199, 1), 320px 90px 0 0 rgba(110, 205, 199, 1),
  325px 90px 0 0 rgba(110, 205, 199, 1), 330px 90px 0 0 rgba(110, 205, 199, 1),
  335px 90px 0 0 rgba(110, 205, 199, 1), 340px 90px 0 0 rgba(110, 205, 199, 1),
  345px 90px 0 0 rgba(110, 205, 199, 1), 350px 90px 0 0 rgba(110, 205, 199, 1),
  355px 90px 0 0 rgba(110, 205, 199, 1), 360px 90px 0 0 rgba(110, 205, 199, 1),
  365px 90px 0 0 rgba(110, 205, 199, 1), 370px 90px 0 0 rgba(110, 205, 199, 1),
  375px 90px 0 0 rgba(110, 205, 199, 1), 380px 90px 0 0 rgba(110, 205, 199, 1),
  385px 90px 0 0 rgba(110, 205, 199, 1), 390px 90px 0 0 rgba(110, 205, 199, 1),
  395px 90px 0 0 rgba(110, 205, 199, 1), 400px 90px 0 0 rgba(110, 205, 199, 1),
  405px 90px 0 0 rgba(110, 205, 199, 1), 410px 90px 0 0 rgba(110, 205, 199, 1),
  415px 90px 0 0 rgba(110, 205, 199, 1), 420px 90px 0 0 rgba(110, 205, 199, 1),
  425px 90px 0 0 rgba(110, 205, 199, 1), 430px 90px 0 0 rgba(110, 205, 199, 1),
  435px 90px 0 0 rgba(110, 205, 199, 1), 440px 90px 0 0 rgba(110, 205, 199, 1),
  445px 90px 0 0 rgba(110, 205, 199, 1), 450px 90px 0 0 rgba(110, 205, 199, 1),
  455px 90px 0 0 rgba(110, 205, 199, 1), 460px 90px 0 0 rgba(110, 205, 199, 1),
  465px 90px 0 0 rgba(110, 205, 199, 1), 470px 90px 0 0 rgba(110, 205, 199, 1),
  475px 90px 0 0 rgba(110, 205, 199, 1), 480px 90px 0 0 rgba(110, 205, 199, 1),
  485px 90px 0 0 rgba(110, 205, 199, 1), 490px 90px 0 0 rgba(110, 205, 199, 1),
  495px 90px 0 0 rgba(110, 205, 199, 1), 500px 90px 0 0 rgba(110, 205, 199, 1),
  505px 90px 0 0 rgba(110, 205, 199, 1), 510px 90px 0 0 rgba(110, 205, 199, 1),
  515px 90px 0 0 rgba(110, 205, 199, 1), 520px 90px 0 0 rgba(110, 205, 199, 1),
  525px 90px 0 0 rgba(110, 205, 199, 1), 530px 90px 0 0 rgba(110, 205, 199, 1),
  535px 90px 0 0 rgba(110, 205, 199, 1), 540px 90px 0 0 rgba(110, 205, 199, 1),
  545px 90px 0 0 rgba(110, 205, 199, 1), 550px 90px 0 0 rgba(110, 205, 199, 1),
  555px 90px 0 0 rgba(110, 205, 199, 1), 560px 90px 0 0 rgba(110, 205, 199, 1),
  565px 90px 0 0 rgba(110, 205, 199, 1), 570px 90px 0 0 rgba(110, 205, 199, 1),
  575px 90px 0 0 rgba(110, 205, 199, 1), 580px 90px 0 0 rgba(110, 205, 199, 1),
  585px 90px 0 0 rgba(110, 205, 199, 1), 590px 90px 0 0 rgba(110, 205, 199, 1),
  595px 90px 0 0 rgba(110, 205, 199, 1), 600px 90px 0 0 rgba(110, 205, 199, 1),
  605px 90px 0 0 rgba(110, 205, 199, 1), 610px 90px 0 0 rgba(110, 205, 199, 1),
  615px 90px 0 0 rgba(110, 205, 199, 1), 620px 90px 0 0 rgba(110, 205, 199, 1),
  625px 90px 0 0 rgba(110, 205, 199, 1), 630px 90px 0 0 rgba(110, 205, 199, 1),
  635px 90px 0 0 rgba(110, 205, 199, 1), 640px 90px 0 0 rgba(110, 205, 199, 1),
  645px 90px 0 0 rgba(110, 205, 199, 1), 650px 90px 0 0 rgba(110, 205, 199, 1),
  655px 90px 0 0 rgba(110, 205, 199, 1), 660px 90px 0 0 rgba(110, 205, 199, 1),
  665px 90px 0 0 rgba(110, 205, 199, 1), 670px 90px 0 0 rgba(110, 205, 199, 1),
  675px 90px 0 0 rgba(110, 205, 199, 1), 680px 90px 0 0 rgba(110, 205, 199, 1),
  685px 90px 0 0 rgba(203, 109, 181, 1), 690px 90px 0 0 rgba(255, 205, 234, 1),
  695px 90px 0 0 rgba(255, 205, 234, 1), 700px 90px 0 0 rgba(168, 90, 150, 1),
  705px 90px 0 0 rgba(203, 109, 181, 1), 5px 95px 0 0 rgba(203, 109, 181, 1),
  10px 95px 0 0 rgba(252, 231, 243, 1), 15px 95px 0 0 rgba(255, 205, 234, 1),
  20px 95px 0 0 rgba(255, 205, 234, 1), 25px 95px 0 0 rgba(203, 109, 181, 1),
  30px 95px 0 0 rgba(110, 205, 199, 1), 35px 95px 0 0 rgba(110, 205, 199, 1),
  40px 95px 0 0 rgba(110, 205, 199, 1), 45px 95px 0 0 rgba(110, 205, 199, 1),
  50px 95px 0 0 rgba(110, 205, 199, 1), 55px 95px 0 0 rgba(110, 205, 199, 1),
  60px 95px 0 0 rgba(110, 205, 199, 1), 65px 95px 0 0 rgba(110, 205, 199, 1),
  70px 95px 0 0 rgba(110, 205, 199, 1), 75px 95px 0 0 rgba(110, 205, 199, 1),
  80px 95px 0 0 rgba(110, 205, 199, 1), 85px 95px 0 0 rgba(110, 205, 199, 1),
  90px 95px 0 0 rgba(110, 205, 199, 1), 95px 95px 0 0 rgba(110, 205, 199, 1),
  100px 95px 0 0 rgba(110, 205, 199, 1), 105px 95px 0 0 rgba(110, 205, 199, 1),
  110px 95px 0 0 rgba(110, 205, 199, 1), 115px 95px 0 0 rgba(110, 205, 199, 1),
  120px 95px 0 0 rgba(110, 205, 199, 1), 125px 95px 0 0 rgba(110, 205, 199, 1),
  130px 95px 0 0 rgba(110, 205, 199, 1), 135px 95px 0 0 rgba(110, 205, 199, 1),
  140px 95px 0 0 rgba(110, 205, 199, 1), 145px 95px 0 0 rgba(110, 205, 199, 1),
  150px 95px 0 0 rgba(110, 205, 199, 1), 155px 95px 0 0 rgba(110, 205, 199, 1),
  160px 95px 0 0 rgba(110, 205, 199, 1), 165px 95px 0 0 rgba(110, 205, 199, 1),
  170px 95px 0 0 rgba(110, 205, 199, 1), 175px 95px 0 0 rgba(110, 205, 199, 1),
  180px 95px 0 0 rgba(110, 205, 199, 1), 185px 95px 0 0 rgba(110, 205, 199, 1),
  190px 95px 0 0 rgba(110, 205, 199, 1), 195px 95px 0 0 rgba(110, 205, 199, 1),
  200px 95px 0 0 rgba(110, 205, 199, 1), 205px 95px 0 0 rgba(110, 205, 199, 1),
  210px 95px 0 0 rgba(110, 205, 199, 1), 215px 95px 0 0 rgba(110, 205, 199, 1),
  220px 95px 0 0 rgba(110, 205, 199, 1), 225px 95px 0 0 rgba(110, 205, 199, 1),
  230px 95px 0 0 rgba(110, 205, 199, 1), 235px 95px 0 0 rgba(110, 205, 199, 1),
  240px 95px 0 0 rgba(110, 205, 199, 1), 245px 95px 0 0 rgba(110, 205, 199, 1),
  250px 95px 0 0 rgba(110, 205, 199, 1), 255px 95px 0 0 rgba(110, 205, 199, 1),
  260px 95px 0 0 rgba(110, 205, 199, 1), 265px 95px 0 0 rgba(110, 205, 199, 1),
  270px 95px 0 0 rgba(110, 205, 199, 1), 275px 95px 0 0 rgba(110, 205, 199, 1),
  280px 95px 0 0 rgba(110, 205, 199, 1), 285px 95px 0 0 rgba(110, 205, 199, 1),
  290px 95px 0 0 rgba(110, 205, 199, 1), 295px 95px 0 0 rgba(110, 205, 199, 1),
  300px 95px 0 0 rgba(110, 205, 199, 1), 305px 95px 0 0 rgba(110, 205, 199, 1),
  310px 95px 0 0 rgba(110, 205, 199, 1), 315px 95px 0 0 rgba(110, 205, 199, 1),
  320px 95px 0 0 rgba(110, 205, 199, 1), 325px 95px 0 0 rgba(110, 205, 199, 1),
  330px 95px 0 0 rgba(110, 205, 199, 1), 335px 95px 0 0 rgba(110, 205, 199, 1),
  340px 95px 0 0 rgba(110, 205, 199, 1), 345px 95px 0 0 rgba(110, 205, 199, 1),
  350px 95px 0 0 rgba(110, 205, 199, 1), 355px 95px 0 0 rgba(110, 205, 199, 1),
  360px 95px 0 0 rgba(110, 205, 199, 1), 365px 95px 0 0 rgba(110, 205, 199, 1),
  370px 95px 0 0 rgba(110, 205, 199, 1), 375px 95px 0 0 rgba(110, 205, 199, 1),
  380px 95px 0 0 rgba(110, 205, 199, 1), 385px 95px 0 0 rgba(110, 205, 199, 1),
  390px 95px 0 0 rgba(110, 205, 199, 1), 395px 95px 0 0 rgba(110, 205, 199, 1),
  400px 95px 0 0 rgba(110, 205, 199, 1), 405px 95px 0 0 rgba(110, 205, 199, 1),
  410px 95px 0 0 rgba(110, 205, 199, 1), 415px 95px 0 0 rgba(110, 205, 199, 1),
  420px 95px 0 0 rgba(110, 205, 199, 1), 425px 95px 0 0 rgba(110, 205, 199, 1),
  430px 95px 0 0 rgba(110, 205, 199, 1), 435px 95px 0 0 rgba(110, 205, 199, 1),
  440px 95px 0 0 rgba(110, 205, 199, 1), 445px 95px 0 0 rgba(110, 205, 199, 1),
  450px 95px 0 0 rgba(110, 205, 199, 1), 455px 95px 0 0 rgba(110, 205, 199, 1),
  460px 95px 0 0 rgba(110, 205, 199, 1), 465px 95px 0 0 rgba(110, 205, 199, 1),
  470px 95px 0 0 rgba(110, 205, 199, 1), 475px 95px 0 0 rgba(110, 205, 199, 1),
  480px 95px 0 0 rgba(110, 205, 199, 1), 485px 95px 0 0 rgba(110, 205, 199, 1),
  490px 95px 0 0 rgba(110, 205, 199, 1), 495px 95px 0 0 rgba(110, 205, 199, 1),
  500px 95px 0 0 rgba(110, 205, 199, 1), 505px 95px 0 0 rgba(110, 205, 199, 1),
  510px 95px 0 0 rgba(110, 205, 199, 1), 515px 95px 0 0 rgba(110, 205, 199, 1),
  520px 95px 0 0 rgba(110, 205, 199, 1), 525px 95px 0 0 rgba(110, 205, 199, 1),
  530px 95px 0 0 rgba(110, 205, 199, 1), 535px 95px 0 0 rgba(110, 205, 199, 1),
  540px 95px 0 0 rgba(110, 205, 199, 1), 545px 95px 0 0 rgba(110, 205, 199, 1),
  550px 95px 0 0 rgba(110, 205, 199, 1), 555px 95px 0 0 rgba(110, 205, 199, 1),
  560px 95px 0 0 rgba(110, 205, 199, 1), 565px 95px 0 0 rgba(110, 205, 199, 1),
  570px 95px 0 0 rgba(110, 205, 199, 1), 575px 95px 0 0 rgba(110, 205, 199, 1),
  580px 95px 0 0 rgba(110, 205, 199, 1), 585px 95px 0 0 rgba(110, 205, 199, 1),
  590px 95px 0 0 rgba(110, 205, 199, 1), 595px 95px 0 0 rgba(110, 205, 199, 1),
  600px 95px 0 0 rgba(110, 205, 199, 1), 605px 95px 0 0 rgba(110, 205, 199, 1),
  610px 95px 0 0 rgba(110, 205, 199, 1), 615px 95px 0 0 rgba(110, 205, 199, 1),
  620px 95px 0 0 rgba(110, 205, 199, 1), 625px 95px 0 0 rgba(110, 205, 199, 1),
  630px 95px 0 0 rgba(110, 205, 199, 1), 635px 95px 0 0 rgba(110, 205, 199, 1),
  640px 95px 0 0 rgba(110, 205, 199, 1), 645px 95px 0 0 rgba(110, 205, 199, 1),
  650px 95px 0 0 rgba(110, 205, 199, 1), 655px 95px 0 0 rgba(110, 205, 199, 1),
  660px 95px 0 0 rgba(110, 205, 199, 1), 665px 95px 0 0 rgba(110, 205, 199, 1),
  670px 95px 0 0 rgba(110, 205, 199, 1), 675px 95px 0 0 rgba(110, 205, 199, 1),
  680px 95px 0 0 rgba(110, 205, 199, 1), 685px 95px 0 0 rgba(203, 109, 181, 1),
  690px 95px 0 0 rgba(255, 205, 234, 1), 695px 95px 0 0 rgba(255, 205, 234, 1),
  700px 95px 0 0 rgba(168, 90, 150, 1), 705px 95px 0 0 rgba(203, 109, 181, 1),
  5px 100px 0 0 rgba(203, 109, 181, 1), 10px 100px 0 0 rgba(252, 231, 243, 1),
  15px 100px 0 0 rgba(255, 205, 234, 1), 20px 100px 0 0 rgba(255, 205, 234, 1),
  25px 100px 0 0 rgba(203, 109, 181, 1), 30px 100px 0 0 rgba(110, 205, 199, 1),
  35px 100px 0 0 rgba(110, 205, 199, 1), 40px 100px 0 0 rgba(110, 205, 199, 1),
  45px 100px 0 0 rgba(110, 205, 199, 1), 50px 100px 0 0 rgba(110, 205, 199, 1),
  55px 100px 0 0 rgba(110, 205, 199, 1), 60px 100px 0 0 rgba(110, 205, 199, 1),
  65px 100px 0 0 rgba(110, 205, 199, 1), 70px 100px 0 0 rgba(110, 205, 199, 1),
  75px 100px 0 0 rgba(110, 205, 199, 1), 80px 100px 0 0 rgba(110, 205, 199, 1),
  85px 100px 0 0 rgba(110, 205, 199, 1), 90px 100px 0 0 rgba(110, 205, 199, 1),
  95px 100px 0 0 rgba(110, 205, 199, 1), 100px 100px 0 0 rgba(110, 205, 199, 1),
  105px 100px 0 0 rgba(110, 205, 199, 1), 110px 100px 0 0 rgba(110, 205, 199, 1),
  115px 100px 0 0 rgba(110, 205, 199, 1), 120px 100px 0 0 rgba(110, 205, 199, 1),
  125px 100px 0 0 rgba(110, 205, 199, 1), 130px 100px 0 0 rgba(110, 205, 199, 1),
  135px 100px 0 0 rgba(110, 205, 199, 1), 140px 100px 0 0 rgba(110, 205, 199, 1),
  145px 100px 0 0 rgba(110, 205, 199, 1), 150px 100px 0 0 rgba(110, 205, 199, 1),
  155px 100px 0 0 rgba(110, 205, 199, 1), 160px 100px 0 0 rgba(110, 205, 199, 1),
  165px 100px 0 0 rgba(110, 205, 199, 1), 170px 100px 0 0 rgba(110, 205, 199, 1),
  175px 100px 0 0 rgba(110, 205, 199, 1), 180px 100px 0 0 rgba(110, 205, 199, 1),
  185px 100px 0 0 rgba(110, 205, 199, 1), 190px 100px 0 0 rgba(110, 205, 199, 1),
  195px 100px 0 0 rgba(110, 205, 199, 1), 200px 100px 0 0 rgba(110, 205, 199, 1),
  205px 100px 0 0 rgba(110, 205, 199, 1), 210px 100px 0 0 rgba(110, 205, 199, 1),
  215px 100px 0 0 rgba(110, 205, 199, 1), 220px 100px 0 0 rgba(110, 205, 199, 1),
  225px 100px 0 0 rgba(110, 205, 199, 1), 230px 100px 0 0 rgba(110, 205, 199, 1),
  235px 100px 0 0 rgba(110, 205, 199, 1), 240px 100px 0 0 rgba(110, 205, 199, 1),
  245px 100px 0 0 rgba(110, 205, 199, 1), 250px 100px 0 0 rgba(110, 205, 199, 1),
  255px 100px 0 0 rgba(110, 205, 199, 1), 260px 100px 0 0 rgba(110, 205, 199, 1),
  265px 100px 0 0 rgba(110, 205, 199, 1), 270px 100px 0 0 rgba(110, 205, 199, 1),
  275px 100px 0 0 rgba(110, 205, 199, 1), 280px 100px 0 0 rgba(110, 205, 199, 1),
  285px 100px 0 0 rgba(110, 205, 199, 1), 290px 100px 0 0 rgba(110, 205, 199, 1),
  295px 100px 0 0 rgba(110, 205, 199, 1), 300px 100px 0 0 rgba(110, 205, 199, 1),
  305px 100px 0 0 rgba(110, 205, 199, 1), 310px 100px 0 0 rgba(110, 205, 199, 1),
  315px 100px 0 0 rgba(110, 205, 199, 1), 320px 100px 0 0 rgba(110, 205, 199, 1),
  325px 100px 0 0 rgba(110, 205, 199, 1), 330px 100px 0 0 rgba(110, 205, 199, 1),
  335px 100px 0 0 rgba(110, 205, 199, 1), 340px 100px 0 0 rgba(110, 205, 199, 1),
  345px 100px 0 0 rgba(110, 205, 199, 1), 350px 100px 0 0 rgba(110, 205, 199, 1),
  355px 100px 0 0 rgba(110, 205, 199, 1), 360px 100px 0 0 rgba(110, 205, 199, 1),
  365px 100px 0 0 rgba(110, 205, 199, 1), 370px 100px 0 0 rgba(110, 205, 199, 1),
  375px 100px 0 0 rgba(110, 205, 199, 1), 380px 100px 0 0 rgba(110, 205, 199, 1),
  385px 100px 0 0 rgba(110, 205, 199, 1), 390px 100px 0 0 rgba(110, 205, 199, 1),
  395px 100px 0 0 rgba(110, 205, 199, 1), 400px 100px 0 0 rgba(110, 205, 199, 1),
  405px 100px 0 0 rgba(110, 205, 199, 1), 410px 100px 0 0 rgba(110, 205, 199, 1),
  415px 100px 0 0 rgba(110, 205, 199, 1), 420px 100px 0 0 rgba(110, 205, 199, 1),
  425px 100px 0 0 rgba(110, 205, 199, 1), 430px 100px 0 0 rgba(110, 205, 199, 1),
  435px 100px 0 0 rgba(110, 205, 199, 1), 440px 100px 0 0 rgba(110, 205, 199, 1),
  445px 100px 0 0 rgba(110, 205, 199, 1), 450px 100px 0 0 rgba(110, 205, 199, 1),
  455px 100px 0 0 rgba(110, 205, 199, 1), 460px 100px 0 0 rgba(110, 205, 199, 1),
  465px 100px 0 0 rgba(110, 205, 199, 1), 470px 100px 0 0 rgba(110, 205, 199, 1),
  475px 100px 0 0 rgba(110, 205, 199, 1), 480px 100px 0 0 rgba(110, 205, 199, 1),
  485px 100px 0 0 rgba(110, 205, 199, 1), 490px 100px 0 0 rgba(110, 205, 199, 1),
  495px 100px 0 0 rgba(110, 205, 199, 1), 500px 100px 0 0 rgba(110, 205, 199, 1),
  505px 100px 0 0 rgba(110, 205, 199, 1), 510px 100px 0 0 rgba(110, 205, 199, 1),
  515px 100px 0 0 rgba(110, 205, 199, 1), 520px 100px 0 0 rgba(110, 205, 199, 1),
  525px 100px 0 0 rgba(110, 205, 199, 1), 530px 100px 0 0 rgba(110, 205, 199, 1),
  535px 100px 0 0 rgba(110, 205, 199, 1), 540px 100px 0 0 rgba(110, 205, 199, 1),
  545px 100px 0 0 rgba(110, 205, 199, 1), 550px 100px 0 0 rgba(110, 205, 199, 1),
  555px 100px 0 0 rgba(110, 205, 199, 1), 560px 100px 0 0 rgba(110, 205, 199, 1),
  565px 100px 0 0 rgba(110, 205, 199, 1), 570px 100px 0 0 rgba(110, 205, 199, 1),
  575px 100px 0 0 rgba(110, 205, 199, 1), 580px 100px 0 0 rgba(110, 205, 199, 1),
  585px 100px 0 0 rgba(110, 205, 199, 1), 590px 100px 0 0 rgba(110, 205, 199, 1),
  595px 100px 0 0 rgba(110, 205, 199, 1), 600px 100px 0 0 rgba(110, 205, 199, 1),
  605px 100px 0 0 rgba(110, 205, 199, 1), 610px 100px 0 0 rgba(110, 205, 199, 1),
  615px 100px 0 0 rgba(110, 205, 199, 1), 620px 100px 0 0 rgba(110, 205, 199, 1),
  625px 100px 0 0 rgba(110, 205, 199, 1), 630px 100px 0 0 rgba(110, 205, 199, 1),
  635px 100px 0 0 rgba(110, 205, 199, 1), 640px 100px 0 0 rgba(110, 205, 199, 1),
  645px 100px 0 0 rgba(110, 205, 199, 1), 650px 100px 0 0 rgba(110, 205, 199, 1),
  655px 100px 0 0 rgba(110, 205, 199, 1), 660px 100px 0 0 rgba(110, 205, 199, 1),
  665px 100px 0 0 rgba(110, 205, 199, 1), 670px 100px 0 0 rgba(110, 205, 199, 1),
  675px 100px 0 0 rgba(110, 205, 199, 1), 680px 100px 0 0 rgba(110, 205, 199, 1),
  685px 100px 0 0 rgba(203, 109, 181, 1), 690px 100px 0 0 rgba(255, 205, 234, 1),
  695px 100px 0 0 rgba(255, 205, 234, 1), 700px 100px 0 0 rgba(168, 90, 150, 1),
  705px 100px 0 0 rgba(203, 109, 181, 1), 5px 105px 0 0 rgba(203, 109, 181, 1),
  10px 105px 0 0 rgba(252, 231, 243, 1), 15px 105px 0 0 rgba(255, 205, 234, 1),
  20px 105px 0 0 rgba(255, 205, 234, 1), 25px 105px 0 0 rgba(203, 109, 181, 1),
  30px 105px 0 0 rgba(110, 205, 199, 1), 35px 105px 0 0 rgba(110, 205, 199, 1),
  40px 105px 0 0 rgba(110, 205, 199, 1), 45px 105px 0 0 rgba(110, 205, 199, 1),
  50px 105px 0 0 rgba(110, 205, 199, 1), 55px 105px 0 0 rgba(110, 205, 199, 1),
  60px 105px 0 0 rgba(110, 205, 199, 1), 65px 105px 0 0 rgba(110, 205, 199, 1),
  70px 105px 0 0 rgba(110, 205, 199, 1), 75px 105px 0 0 rgba(110, 205, 199, 1),
  80px 105px 0 0 rgba(110, 205, 199, 1), 85px 105px 0 0 rgba(110, 205, 199, 1),
  90px 105px 0 0 rgba(110, 205, 199, 1), 95px 105px 0 0 rgba(110, 205, 199, 1),
  100px 105px 0 0 rgba(110, 205, 199, 1), 105px 105px 0 0 rgba(110, 205, 199, 1),
  110px 105px 0 0 rgba(110, 205, 199, 1), 115px 105px 0 0 rgba(110, 205, 199, 1),
  120px 105px 0 0 rgba(110, 205, 199, 1), 125px 105px 0 0 rgba(110, 205, 199, 1),
  130px 105px 0 0 rgba(110, 205, 199, 1), 135px 105px 0 0 rgba(110, 205, 199, 1),
  140px 105px 0 0 rgba(110, 205, 199, 1), 145px 105px 0 0 rgba(110, 205, 199, 1),
  150px 105px 0 0 rgba(110, 205, 199, 1), 155px 105px 0 0 rgba(110, 205, 199, 1),
  160px 105px 0 0 rgba(110, 205, 199, 1), 165px 105px 0 0 rgba(110, 205, 199, 1),
  170px 105px 0 0 rgba(110, 205, 199, 1), 175px 105px 0 0 rgba(110, 205, 199, 1),
  180px 105px 0 0 rgba(110, 205, 199, 1), 185px 105px 0 0 rgba(110, 205, 199, 1),
  190px 105px 0 0 rgba(110, 205, 199, 1), 195px 105px 0 0 rgba(110, 205, 199, 1),
  200px 105px 0 0 rgba(110, 205, 199, 1), 205px 105px 0 0 rgba(110, 205, 199, 1),
  210px 105px 0 0 rgba(110, 205, 199, 1), 215px 105px 0 0 rgba(110, 205, 199, 1),
  220px 105px 0 0 rgba(110, 205, 199, 1), 225px 105px 0 0 rgba(110, 205, 199, 1),
  230px 105px 0 0 rgba(110, 205, 199, 1), 235px 105px 0 0 rgba(110, 205, 199, 1),
  240px 105px 0 0 rgba(110, 205, 199, 1), 245px 105px 0 0 rgba(110, 205, 199, 1),
  250px 105px 0 0 rgba(110, 205, 199, 1), 255px 105px 0 0 rgba(110, 205, 199, 1),
  260px 105px 0 0 rgba(110, 205, 199, 1), 265px 105px 0 0 rgba(110, 205, 199, 1),
  270px 105px 0 0 rgba(110, 205, 199, 1), 275px 105px 0 0 rgba(110, 205, 199, 1),
  280px 105px 0 0 rgba(110, 205, 199, 1), 285px 105px 0 0 rgba(110, 205, 199, 1),
  290px 105px 0 0 rgba(110, 205, 199, 1), 295px 105px 0 0 rgba(110, 205, 199, 1),
  300px 105px 0 0 rgba(110, 205, 199, 1), 305px 105px 0 0 rgba(110, 205, 199, 1),
  310px 105px 0 0 rgba(110, 205, 199, 1), 315px 105px 0 0 rgba(110, 205, 199, 1),
  320px 105px 0 0 rgba(110, 205, 199, 1), 325px 105px 0 0 rgba(110, 205, 199, 1),
  330px 105px 0 0 rgba(110, 205, 199, 1), 335px 105px 0 0 rgba(110, 205, 199, 1),
  340px 105px 0 0 rgba(110, 205, 199, 1), 345px 105px 0 0 rgba(110, 205, 199, 1),
  350px 105px 0 0 rgba(110, 205, 199, 1), 355px 105px 0 0 rgba(110, 205, 199, 1),
  360px 105px 0 0 rgba(110, 205, 199, 1), 365px 105px 0 0 rgba(110, 205, 199, 1),
  370px 105px 0 0 rgba(110, 205, 199, 1), 375px 105px 0 0 rgba(110, 205, 199, 1),
  380px 105px 0 0 rgba(110, 205, 199, 1), 385px 105px 0 0 rgba(110, 205, 199, 1),
  390px 105px 0 0 rgba(110, 205, 199, 1), 395px 105px 0 0 rgba(110, 205, 199, 1),
  400px 105px 0 0 rgba(110, 205, 199, 1), 405px 105px 0 0 rgba(110, 205, 199, 1),
  410px 105px 0 0 rgba(110, 205, 199, 1), 415px 105px 0 0 rgba(110, 205, 199, 1),
  420px 105px 0 0 rgba(110, 205, 199, 1), 425px 105px 0 0 rgba(110, 205, 199, 1),
  430px 105px 0 0 rgba(110, 205, 199, 1), 435px 105px 0 0 rgba(110, 205, 199, 1),
  440px 105px 0 0 rgba(110, 205, 199, 1), 445px 105px 0 0 rgba(110, 205, 199, 1),
  450px 105px 0 0 rgba(110, 205, 199, 1), 455px 105px 0 0 rgba(110, 205, 199, 1),
  460px 105px 0 0 rgba(110, 205, 199, 1), 465px 105px 0 0 rgba(110, 205, 199, 1),
  470px 105px 0 0 rgba(110, 205, 199, 1), 475px 105px 0 0 rgba(110, 205, 199, 1),
  480px 105px 0 0 rgba(110, 205, 199, 1), 485px 105px 0 0 rgba(110, 205, 199, 1),
  490px 105px 0 0 rgba(110, 205, 199, 1), 495px 105px 0 0 rgba(110, 205, 199, 1),
  500px 105px 0 0 rgba(110, 205, 199, 1), 505px 105px 0 0 rgba(110, 205, 199, 1),
  510px 105px 0 0 rgba(110, 205, 199, 1), 515px 105px 0 0 rgba(110, 205, 199, 1),
  520px 105px 0 0 rgba(110, 205, 199, 1), 525px 105px 0 0 rgba(110, 205, 199, 1),
  530px 105px 0 0 rgba(110, 205, 199, 1), 535px 105px 0 0 rgba(110, 205, 199, 1),
  540px 105px 0 0 rgba(110, 205, 199, 1), 545px 105px 0 0 rgba(110, 205, 199, 1),
  550px 105px 0 0 rgba(110, 205, 199, 1), 555px 105px 0 0 rgba(110, 205, 199, 1),
  560px 105px 0 0 rgba(110, 205, 199, 1), 565px 105px 0 0 rgba(110, 205, 199, 1),
  570px 105px 0 0 rgba(110, 205, 199, 1), 575px 105px 0 0 rgba(110, 205, 199, 1),
  580px 105px 0 0 rgba(110, 205, 199, 1), 585px 105px 0 0 rgba(110, 205, 199, 1),
  590px 105px 0 0 rgba(110, 205, 199, 1), 595px 105px 0 0 rgba(110, 205, 199, 1),
  600px 105px 0 0 rgba(110, 205, 199, 1), 605px 105px 0 0 rgba(110, 205, 199, 1),
  610px 105px 0 0 rgba(110, 205, 199, 1), 615px 105px 0 0 rgba(110, 205, 199, 1),
  620px 105px 0 0 rgba(110, 205, 199, 1), 625px 105px 0 0 rgba(110, 205, 199, 1),
  630px 105px 0 0 rgba(110, 205, 199, 1), 635px 105px 0 0 rgba(110, 205, 199, 1),
  640px 105px 0 0 rgba(110, 205, 199, 1), 645px 105px 0 0 rgba(110, 205, 199, 1),
  650px 105px 0 0 rgba(110, 205, 199, 1), 655px 105px 0 0 rgba(110, 205, 199, 1),
  660px 105px 0 0 rgba(110, 205, 199, 1), 665px 105px 0 0 rgba(110, 205, 199, 1),
  670px 105px 0 0 rgba(110, 205, 199, 1), 675px 105px 0 0 rgba(110, 205, 199, 1),
  680px 105px 0 0 rgba(110, 205, 199, 1), 685px 105px 0 0 rgba(203, 109, 181, 1),
  690px 105px 0 0 rgba(255, 205, 234, 1), 695px 105px 0 0 rgba(255, 205, 234, 1),
  700px 105px 0 0 rgba(168, 90, 150, 1), 705px 105px 0 0 rgba(203, 109, 181, 1),
  5px 110px 0 0 rgba(203, 109, 181, 1), 10px 110px 0 0 rgba(252, 231, 243, 1),
  15px 110px 0 0 rgba(255, 205, 234, 1), 20px 110px 0 0 rgba(255, 205, 234, 1),
  25px 110px 0 0 rgba(203, 109, 181, 1), 30px 110px 0 0 rgba(110, 205, 199, 1),
  35px 110px 0 0 rgba(110, 205, 199, 1), 40px 110px 0 0 rgba(110, 205, 199, 1),
  45px 110px 0 0 rgba(110, 205, 199, 1), 50px 110px 0 0 rgba(110, 205, 199, 1),
  55px 110px 0 0 rgba(110, 205, 199, 1), 60px 110px 0 0 rgba(110, 205, 199, 1),
  65px 110px 0 0 rgba(110, 205, 199, 1), 70px 110px 0 0 rgba(110, 205, 199, 1),
  75px 110px 0 0 rgba(110, 205, 199, 1), 80px 110px 0 0 rgba(110, 205, 199, 1),
  85px 110px 0 0 rgba(110, 205, 199, 1), 90px 110px 0 0 rgba(110, 205, 199, 1),
  95px 110px 0 0 rgba(110, 205, 199, 1), 100px 110px 0 0 rgba(110, 205, 199, 1),
  105px 110px 0 0 rgba(110, 205, 199, 1), 110px 110px 0 0 rgba(110, 205, 199, 1),
  115px 110px 0 0 rgba(110, 205, 199, 1), 120px 110px 0 0 rgba(110, 205, 199, 1),
  125px 110px 0 0 rgba(110, 205, 199, 1), 130px 110px 0 0 rgba(110, 205, 199, 1),
  135px 110px 0 0 rgba(110, 205, 199, 1), 140px 110px 0 0 rgba(110, 205, 199, 1),
  145px 110px 0 0 rgba(110, 205, 199, 1), 150px 110px 0 0 rgba(110, 205, 199, 1),
  155px 110px 0 0 rgba(110, 205, 199, 1), 160px 110px 0 0 rgba(110, 205, 199, 1),
  165px 110px 0 0 rgba(110, 205, 199, 1), 170px 110px 0 0 rgba(110, 205, 199, 1),
  175px 110px 0 0 rgba(110, 205, 199, 1), 180px 110px 0 0 rgba(110, 205, 199, 1),
  185px 110px 0 0 rgba(110, 205, 199, 1), 190px 110px 0 0 rgba(110, 205, 199, 1),
  195px 110px 0 0 rgba(110, 205, 199, 1), 200px 110px 0 0 rgba(110, 205, 199, 1),
  205px 110px 0 0 rgba(110, 205, 199, 1), 210px 110px 0 0 rgba(110, 205, 199, 1),
  215px 110px 0 0 rgba(110, 205, 199, 1), 220px 110px 0 0 rgba(110, 205, 199, 1),
  225px 110px 0 0 rgba(110, 205, 199, 1), 230px 110px 0 0 rgba(110, 205, 199, 1),
  235px 110px 0 0 rgba(110, 205, 199, 1), 240px 110px 0 0 rgba(110, 205, 199, 1),
  245px 110px 0 0 rgba(110, 205, 199, 1), 250px 110px 0 0 rgba(110, 205, 199, 1),
  255px 110px 0 0 rgba(110, 205, 199, 1), 260px 110px 0 0 rgba(110, 205, 199, 1),
  265px 110px 0 0 rgba(110, 205, 199, 1), 270px 110px 0 0 rgba(110, 205, 199, 1),
  275px 110px 0 0 rgba(110, 205, 199, 1), 280px 110px 0 0 rgba(110, 205, 199, 1),
  285px 110px 0 0 rgba(110, 205, 199, 1), 290px 110px 0 0 rgba(110, 205, 199, 1),
  295px 110px 0 0 rgba(110, 205, 199, 1), 300px 110px 0 0 rgba(110, 205, 199, 1),
  305px 110px 0 0 rgba(110, 205, 199, 1), 310px 110px 0 0 rgba(110, 205, 199, 1),
  315px 110px 0 0 rgba(110, 205, 199, 1), 320px 110px 0 0 rgba(110, 205, 199, 1),
  325px 110px 0 0 rgba(110, 205, 199, 1), 330px 110px 0 0 rgba(110, 205, 199, 1),
  335px 110px 0 0 rgba(110, 205, 199, 1), 340px 110px 0 0 rgba(110, 205, 199, 1),
  345px 110px 0 0 rgba(110, 205, 199, 1), 350px 110px 0 0 rgba(110, 205, 199, 1),
  355px 110px 0 0 rgba(110, 205, 199, 1), 360px 110px 0 0 rgba(110, 205, 199, 1),
  365px 110px 0 0 rgba(110, 205, 199, 1), 370px 110px 0 0 rgba(110, 205, 199, 1),
  375px 110px 0 0 rgba(110, 205, 199, 1), 380px 110px 0 0 rgba(110, 205, 199, 1),
  385px 110px 0 0 rgba(110, 205, 199, 1), 390px 110px 0 0 rgba(110, 205, 199, 1),
  395px 110px 0 0 rgba(110, 205, 199, 1), 400px 110px 0 0 rgba(110, 205, 199, 1),
  405px 110px 0 0 rgba(110, 205, 199, 1), 410px 110px 0 0 rgba(110, 205, 199, 1),
  415px 110px 0 0 rgba(110, 205, 199, 1), 420px 110px 0 0 rgba(110, 205, 199, 1),
  425px 110px 0 0 rgba(110, 205, 199, 1), 430px 110px 0 0 rgba(110, 205, 199, 1),
  435px 110px 0 0 rgba(110, 205, 199, 1), 440px 110px 0 0 rgba(110, 205, 199, 1),
  445px 110px 0 0 rgba(110, 205, 199, 1), 450px 110px 0 0 rgba(110, 205, 199, 1),
  455px 110px 0 0 rgba(110, 205, 199, 1), 460px 110px 0 0 rgba(110, 205, 199, 1),
  465px 110px 0 0 rgba(110, 205, 199, 1), 470px 110px 0 0 rgba(110, 205, 199, 1),
  475px 110px 0 0 rgba(110, 205, 199, 1), 480px 110px 0 0 rgba(110, 205, 199, 1),
  485px 110px 0 0 rgba(110, 205, 199, 1), 490px 110px 0 0 rgba(110, 205, 199, 1),
  495px 110px 0 0 rgba(110, 205, 199, 1), 500px 110px 0 0 rgba(110, 205, 199, 1),
  505px 110px 0 0 rgba(110, 205, 199, 1), 510px 110px 0 0 rgba(110, 205, 199, 1),
  515px 110px 0 0 rgba(110, 205, 199, 1), 520px 110px 0 0 rgba(110, 205, 199, 1),
  525px 110px 0 0 rgba(110, 205, 199, 1), 530px 110px 0 0 rgba(110, 205, 199, 1),
  535px 110px 0 0 rgba(110, 205, 199, 1), 540px 110px 0 0 rgba(110, 205, 199, 1),
  545px 110px 0 0 rgba(110, 205, 199, 1), 550px 110px 0 0 rgba(110, 205, 199, 1),
  555px 110px 0 0 rgba(110, 205, 199, 1), 560px 110px 0 0 rgba(110, 205, 199, 1),
  565px 110px 0 0 rgba(110, 205, 199, 1), 570px 110px 0 0 rgba(110, 205, 199, 1),
  575px 110px 0 0 rgba(110, 205, 199, 1), 580px 110px 0 0 rgba(110, 205, 199, 1),
  585px 110px 0 0 rgba(110, 205, 199, 1), 590px 110px 0 0 rgba(110, 205, 199, 1),
  595px 110px 0 0 rgba(110, 205, 199, 1), 600px 110px 0 0 rgba(110, 205, 199, 1),
  605px 110px 0 0 rgba(110, 205, 199, 1), 610px 110px 0 0 rgba(110, 205, 199, 1),
  615px 110px 0 0 rgba(110, 205, 199, 1), 620px 110px 0 0 rgba(110, 205, 199, 1),
  625px 110px 0 0 rgba(110, 205, 199, 1), 630px 110px 0 0 rgba(110, 205, 199, 1),
  635px 110px 0 0 rgba(110, 205, 199, 1), 640px 110px 0 0 rgba(110, 205, 199, 1),
  645px 110px 0 0 rgba(110, 205, 199, 1), 650px 110px 0 0 rgba(110, 205, 199, 1),
  655px 110px 0 0 rgba(110, 205, 199, 1), 660px 110px 0 0 rgba(110, 205, 199, 1),
  665px 110px 0 0 rgba(110, 205, 199, 1), 670px 110px 0 0 rgba(110, 205, 199, 1),
  675px 110px 0 0 rgba(110, 205, 199, 1), 680px 110px 0 0 rgba(110, 205, 199, 1),
  685px 110px 0 0 rgba(203, 109, 181, 1), 690px 110px 0 0 rgba(255, 205, 234, 1),
  695px 110px 0 0 rgba(255, 205, 234, 1), 700px 110px 0 0 rgba(168, 90, 150, 1),
  705px 110px 0 0 rgba(203, 109, 181, 1), 5px 115px 0 0 rgba(203, 109, 181, 1),
  10px 115px 0 0 rgba(252, 231, 243, 1), 15px 115px 0 0 rgba(255, 205, 234, 1),
  20px 115px 0 0 rgba(255, 205, 234, 1), 25px 115px 0 0 rgba(203, 109, 181, 1),
  30px 115px 0 0 rgba(110, 205, 199, 1), 35px 115px 0 0 rgba(110, 205, 199, 1),
  40px 115px 0 0 rgba(110, 205, 199, 1), 45px 115px 0 0 rgba(110, 205, 199, 1),
  50px 115px 0 0 rgba(110, 205, 199, 1), 55px 115px 0 0 rgba(110, 205, 199, 1),
  60px 115px 0 0 rgba(110, 205, 199, 1), 65px 115px 0 0 rgba(110, 205, 199, 1),
  70px 115px 0 0 rgba(110, 205, 199, 1), 75px 115px 0 0 rgba(110, 205, 199, 1),
  80px 115px 0 0 rgba(110, 205, 199, 1), 85px 115px 0 0 rgba(110, 205, 199, 1),
  90px 115px 0 0 rgba(110, 205, 199, 1), 95px 115px 0 0 rgba(110, 205, 199, 1),
  100px 115px 0 0 rgba(110, 205, 199, 1), 105px 115px 0 0 rgba(110, 205, 199, 1),
  110px 115px 0 0 rgba(110, 205, 199, 1), 115px 115px 0 0 rgba(110, 205, 199, 1),
  120px 115px 0 0 rgba(110, 205, 199, 1), 125px 115px 0 0 rgba(110, 205, 199, 1),
  130px 115px 0 0 rgba(110, 205, 199, 1), 135px 115px 0 0 rgba(110, 205, 199, 1),
  140px 115px 0 0 rgba(110, 205, 199, 1), 145px 115px 0 0 rgba(110, 205, 199, 1),
  150px 115px 0 0 rgba(110, 205, 199, 1), 155px 115px 0 0 rgba(110, 205, 199, 1),
  160px 115px 0 0 rgba(110, 205, 199, 1), 165px 115px 0 0 rgba(110, 205, 199, 1),
  170px 115px 0 0 rgba(110, 205, 199, 1), 175px 115px 0 0 rgba(110, 205, 199, 1),
  180px 115px 0 0 rgba(110, 205, 199, 1), 185px 115px 0 0 rgba(110, 205, 199, 1),
  190px 115px 0 0 rgba(110, 205, 199, 1), 195px 115px 0 0 rgba(110, 205, 199, 1),
  200px 115px 0 0 rgba(110, 205, 199, 1), 205px 115px 0 0 rgba(110, 205, 199, 1),
  210px 115px 0 0 rgba(110, 205, 199, 1), 215px 115px 0 0 rgba(110, 205, 199, 1),
  220px 115px 0 0 rgba(110, 205, 199, 1), 225px 115px 0 0 rgba(110, 205, 199, 1),
  230px 115px 0 0 rgba(110, 205, 199, 1), 235px 115px 0 0 rgba(110, 205, 199, 1),
  240px 115px 0 0 rgba(110, 205, 199, 1), 245px 115px 0 0 rgba(110, 205, 199, 1),
  250px 115px 0 0 rgba(110, 205, 199, 1), 255px 115px 0 0 rgba(110, 205, 199, 1),
  260px 115px 0 0 rgba(110, 205, 199, 1), 265px 115px 0 0 rgba(110, 205, 199, 1),
  270px 115px 0 0 rgba(110, 205, 199, 1), 275px 115px 0 0 rgba(110, 205, 199, 1),
  280px 115px 0 0 rgba(110, 205, 199, 1), 285px 115px 0 0 rgba(110, 205, 199, 1),
  290px 115px 0 0 rgba(110, 205, 199, 1), 295px 115px 0 0 rgba(110, 205, 199, 1),
  300px 115px 0 0 rgba(110, 205, 199, 1), 305px 115px 0 0 rgba(110, 205, 199, 1),
  310px 115px 0 0 rgba(110, 205, 199, 1), 315px 115px 0 0 rgba(110, 205, 199, 1),
  320px 115px 0 0 rgba(110, 205, 199, 1), 325px 115px 0 0 rgba(110, 205, 199, 1),
  330px 115px 0 0 rgba(110, 205, 199, 1), 335px 115px 0 0 rgba(110, 205, 199, 1),
  340px 115px 0 0 rgba(110, 205, 199, 1), 345px 115px 0 0 rgba(110, 205, 199, 1),
  350px 115px 0 0 rgba(110, 205, 199, 1), 355px 115px 0 0 rgba(110, 205, 199, 1),
  360px 115px 0 0 rgba(110, 205, 199, 1), 365px 115px 0 0 rgba(110, 205, 199, 1),
  370px 115px 0 0 rgba(110, 205, 199, 1), 375px 115px 0 0 rgba(110, 205, 199, 1),
  380px 115px 0 0 rgba(110, 205, 199, 1), 385px 115px 0 0 rgba(110, 205, 199, 1),
  390px 115px 0 0 rgba(110, 205, 199, 1), 395px 115px 0 0 rgba(110, 205, 199, 1),
  400px 115px 0 0 rgba(110, 205, 199, 1), 405px 115px 0 0 rgba(110, 205, 199, 1),
  410px 115px 0 0 rgba(110, 205, 199, 1), 415px 115px 0 0 rgba(110, 205, 199, 1),
  420px 115px 0 0 rgba(110, 205, 199, 1), 425px 115px 0 0 rgba(110, 205, 199, 1),
  430px 115px 0 0 rgba(110, 205, 199, 1), 435px 115px 0 0 rgba(110, 205, 199, 1),
  440px 115px 0 0 rgba(110, 205, 199, 1), 445px 115px 0 0 rgba(110, 205, 199, 1),
  450px 115px 0 0 rgba(110, 205, 199, 1), 455px 115px 0 0 rgba(110, 205, 199, 1),
  460px 115px 0 0 rgba(110, 205, 199, 1), 465px 115px 0 0 rgba(110, 205, 199, 1),
  470px 115px 0 0 rgba(110, 205, 199, 1), 475px 115px 0 0 rgba(110, 205, 199, 1),
  480px 115px 0 0 rgba(110, 205, 199, 1), 485px 115px 0 0 rgba(110, 205, 199, 1),
  490px 115px 0 0 rgba(110, 205, 199, 1), 495px 115px 0 0 rgba(110, 205, 199, 1),
  500px 115px 0 0 rgba(110, 205, 199, 1), 505px 115px 0 0 rgba(110, 205, 199, 1),
  510px 115px 0 0 rgba(110, 205, 199, 1), 515px 115px 0 0 rgba(110, 205, 199, 1),
  520px 115px 0 0 rgba(110, 205, 199, 1), 525px 115px 0 0 rgba(110, 205, 199, 1),
  530px 115px 0 0 rgba(110, 205, 199, 1), 535px 115px 0 0 rgba(110, 205, 199, 1),
  540px 115px 0 0 rgba(110, 205, 199, 1), 545px 115px 0 0 rgba(110, 205, 199, 1),
  550px 115px 0 0 rgba(110, 205, 199, 1), 555px 115px 0 0 rgba(110, 205, 199, 1),
  560px 115px 0 0 rgba(110, 205, 199, 1), 565px 115px 0 0 rgba(110, 205, 199, 1),
  570px 115px 0 0 rgba(110, 205, 199, 1), 575px 115px 0 0 rgba(110, 205, 199, 1),
  580px 115px 0 0 rgba(110, 205, 199, 1), 585px 115px 0 0 rgba(110, 205, 199, 1),
  590px 115px 0 0 rgba(110, 205, 199, 1), 595px 115px 0 0 rgba(110, 205, 199, 1),
  600px 115px 0 0 rgba(110, 205, 199, 1), 605px 115px 0 0 rgba(110, 205, 199, 1),
  610px 115px 0 0 rgba(110, 205, 199, 1), 615px 115px 0 0 rgba(110, 205, 199, 1),
  620px 115px 0 0 rgba(110, 205, 199, 1), 625px 115px 0 0 rgba(110, 205, 199, 1),
  630px 115px 0 0 rgba(110, 205, 199, 1), 635px 115px 0 0 rgba(110, 205, 199, 1),
  640px 115px 0 0 rgba(110, 205, 199, 1), 645px 115px 0 0 rgba(110, 205, 199, 1),
  650px 115px 0 0 rgba(110, 205, 199, 1), 655px 115px 0 0 rgba(110, 205, 199, 1),
  660px 115px 0 0 rgba(110, 205, 199, 1), 665px 115px 0 0 rgba(110, 205, 199, 1),
  670px 115px 0 0 rgba(110, 205, 199, 1), 675px 115px 0 0 rgba(110, 205, 199, 1),
  680px 115px 0 0 rgba(110, 205, 199, 1), 685px 115px 0 0 rgba(203, 109, 181, 1),
  690px 115px 0 0 rgba(255, 205, 234, 1), 695px 115px 0 0 rgba(255, 205, 234, 1),
  700px 115px 0 0 rgba(168, 90, 150, 1), 705px 115px 0 0 rgba(203, 109, 181, 1),
  5px 120px 0 0 rgba(203, 109, 181, 1), 10px 120px 0 0 rgba(252, 231, 243, 1),
  15px 120px 0 0 rgba(255, 205, 234, 1), 20px 120px 0 0 rgba(255, 205, 234, 1),
  25px 120px 0 0 rgba(203, 109, 181, 1), 30px 120px 0 0 rgba(110, 205, 199, 1),
  35px 120px 0 0 rgba(110, 205, 199, 1), 40px 120px 0 0 rgba(110, 205, 199, 1),
  45px 120px 0 0 rgba(110, 205, 199, 1), 50px 120px 0 0 rgba(110, 205, 199, 1),
  55px 120px 0 0 rgba(110, 205, 199, 1), 60px 120px 0 0 rgba(110, 205, 199, 1),
  65px 120px 0 0 rgba(110, 205, 199, 1), 70px 120px 0 0 rgba(110, 205, 199, 1),
  75px 120px 0 0 rgba(110, 205, 199, 1), 80px 120px 0 0 rgba(110, 205, 199, 1),
  85px 120px 0 0 rgba(110, 205, 199, 1), 90px 120px 0 0 rgba(110, 205, 199, 1),
  95px 120px 0 0 rgba(110, 205, 199, 1), 100px 120px 0 0 rgba(110, 205, 199, 1),
  105px 120px 0 0 rgba(110, 205, 199, 1), 110px 120px 0 0 rgba(110, 205, 199, 1),
  115px 120px 0 0 rgba(110, 205, 199, 1), 120px 120px 0 0 rgba(110, 205, 199, 1),
  125px 120px 0 0 rgba(110, 205, 199, 1), 130px 120px 0 0 rgba(110, 205, 199, 1),
  135px 120px 0 0 rgba(110, 205, 199, 1), 140px 120px 0 0 rgba(110, 205, 199, 1),
  145px 120px 0 0 rgba(110, 205, 199, 1), 150px 120px 0 0 rgba(110, 205, 199, 1),
  155px 120px 0 0 rgba(110, 205, 199, 1), 160px 120px 0 0 rgba(110, 205, 199, 1),
  165px 120px 0 0 rgba(110, 205, 199, 1), 170px 120px 0 0 rgba(110, 205, 199, 1),
  175px 120px 0 0 rgba(110, 205, 199, 1), 180px 120px 0 0 rgba(110, 205, 199, 1),
  185px 120px 0 0 rgba(110, 205, 199, 1), 190px 120px 0 0 rgba(110, 205, 199, 1),
  195px 120px 0 0 rgba(110, 205, 199, 1), 200px 120px 0 0 rgba(110, 205, 199, 1),
  205px 120px 0 0 rgba(110, 205, 199, 1), 210px 120px 0 0 rgba(110, 205, 199, 1),
  215px 120px 0 0 rgba(110, 205, 199, 1), 220px 120px 0 0 rgba(110, 205, 199, 1),
  225px 120px 0 0 rgba(110, 205, 199, 1), 230px 120px 0 0 rgba(110, 205, 199, 1),
  235px 120px 0 0 rgba(110, 205, 199, 1), 240px 120px 0 0 rgba(110, 205, 199, 1),
  245px 120px 0 0 rgba(110, 205, 199, 1), 250px 120px 0 0 rgba(110, 205, 199, 1),
  255px 120px 0 0 rgba(110, 205, 199, 1), 260px 120px 0 0 rgba(110, 205, 199, 1),
  265px 120px 0 0 rgba(110, 205, 199, 1), 270px 120px 0 0 rgba(110, 205, 199, 1),
  275px 120px 0 0 rgba(110, 205, 199, 1), 280px 120px 0 0 rgba(110, 205, 199, 1),
  285px 120px 0 0 rgba(110, 205, 199, 1), 290px 120px 0 0 rgba(110, 205, 199, 1),
  295px 120px 0 0 rgba(110, 205, 199, 1), 300px 120px 0 0 rgba(110, 205, 199, 1),
  305px 120px 0 0 rgba(110, 205, 199, 1), 310px 120px 0 0 rgba(110, 205, 199, 1),
  315px 120px 0 0 rgba(110, 205, 199, 1), 320px 120px 0 0 rgba(110, 205, 199, 1),
  325px 120px 0 0 rgba(110, 205, 199, 1), 330px 120px 0 0 rgba(110, 205, 199, 1),
  335px 120px 0 0 rgba(110, 205, 199, 1), 340px 120px 0 0 rgba(110, 205, 199, 1),
  345px 120px 0 0 rgba(110, 205, 199, 1), 350px 120px 0 0 rgba(110, 205, 199, 1),
  355px 120px 0 0 rgba(110, 205, 199, 1), 360px 120px 0 0 rgba(110, 205, 199, 1),
  365px 120px 0 0 rgba(110, 205, 199, 1), 370px 120px 0 0 rgba(110, 205, 199, 1),
  375px 120px 0 0 rgba(110, 205, 199, 1), 380px 120px 0 0 rgba(110, 205, 199, 1),
  385px 120px 0 0 rgba(110, 205, 199, 1), 390px 120px 0 0 rgba(110, 205, 199, 1),
  395px 120px 0 0 rgba(110, 205, 199, 1), 400px 120px 0 0 rgba(110, 205, 199, 1),
  405px 120px 0 0 rgba(110, 205, 199, 1), 410px 120px 0 0 rgba(110, 205, 199, 1),
  415px 120px 0 0 rgba(110, 205, 199, 1), 420px 120px 0 0 rgba(110, 205, 199, 1),
  425px 120px 0 0 rgba(110, 205, 199, 1), 430px 120px 0 0 rgba(110, 205, 199, 1),
  435px 120px 0 0 rgba(110, 205, 199, 1), 440px 120px 0 0 rgba(110, 205, 199, 1),
  445px 120px 0 0 rgba(110, 205, 199, 1), 450px 120px 0 0 rgba(110, 205, 199, 1),
  455px 120px 0 0 rgba(110, 205, 199, 1), 460px 120px 0 0 rgba(110, 205, 199, 1),
  465px 120px 0 0 rgba(110, 205, 199, 1), 470px 120px 0 0 rgba(110, 205, 199, 1),
  475px 120px 0 0 rgba(110, 205, 199, 1), 480px 120px 0 0 rgba(110, 205, 199, 1),
  485px 120px 0 0 rgba(110, 205, 199, 1), 490px 120px 0 0 rgba(110, 205, 199, 1),
  495px 120px 0 0 rgba(110, 205, 199, 1), 500px 120px 0 0 rgba(110, 205, 199, 1),
  505px 120px 0 0 rgba(110, 205, 199, 1), 510px 120px 0 0 rgba(110, 205, 199, 1),
  515px 120px 0 0 rgba(110, 205, 199, 1), 520px 120px 0 0 rgba(110, 205, 199, 1),
  525px 120px 0 0 rgba(110, 205, 199, 1), 530px 120px 0 0 rgba(110, 205, 199, 1),
  535px 120px 0 0 rgba(110, 205, 199, 1), 540px 120px 0 0 rgba(110, 205, 199, 1),
  545px 120px 0 0 rgba(110, 205, 199, 1), 550px 120px 0 0 rgba(110, 205, 199, 1),
  555px 120px 0 0 rgba(110, 205, 199, 1), 560px 120px 0 0 rgba(110, 205, 199, 1),
  565px 120px 0 0 rgba(110, 205, 199, 1), 570px 120px 0 0 rgba(110, 205, 199, 1),
  575px 120px 0 0 rgba(110, 205, 199, 1), 580px 120px 0 0 rgba(110, 205, 199, 1),
  585px 120px 0 0 rgba(110, 205, 199, 1), 590px 120px 0 0 rgba(110, 205, 199, 1),
  595px 120px 0 0 rgba(110, 205, 199, 1), 600px 120px 0 0 rgba(110, 205, 199, 1),
  605px 120px 0 0 rgba(110, 205, 199, 1), 610px 120px 0 0 rgba(110, 205, 199, 1),
  615px 120px 0 0 rgba(110, 205, 199, 1), 620px 120px 0 0 rgba(110, 205, 199, 1),
  625px 120px 0 0 rgba(110, 205, 199, 1), 630px 120px 0 0 rgba(110, 205, 199, 1),
  635px 120px 0 0 rgba(110, 205, 199, 1), 640px 120px 0 0 rgba(110, 205, 199, 1),
  645px 120px 0 0 rgba(110, 205, 199, 1), 650px 120px 0 0 rgba(110, 205, 199, 1),
  655px 120px 0 0 rgba(110, 205, 199, 1), 660px 120px 0 0 rgba(110, 205, 199, 1),
  665px 120px 0 0 rgba(110, 205, 199, 1), 670px 120px 0 0 rgba(110, 205, 199, 1),
  675px 120px 0 0 rgba(110, 205, 199, 1), 680px 120px 0 0 rgba(110, 205, 199, 1),
  685px 120px 0 0 rgba(203, 109, 181, 1), 690px 120px 0 0 rgba(255, 205, 234, 1),
  695px 120px 0 0 rgba(255, 205, 234, 1), 700px 120px 0 0 rgba(168, 90, 150, 1),
  705px 120px 0 0 rgba(203, 109, 181, 1), 5px 125px 0 0 rgba(203, 109, 181, 1),
  10px 125px 0 0 rgba(252, 231, 243, 1), 15px 125px 0 0 rgba(255, 205, 234, 1),
  20px 125px 0 0 rgba(255, 205, 234, 1), 25px 125px 0 0 rgba(203, 109, 181, 1),
  30px 125px 0 0 rgba(110, 205, 199, 1), 35px 125px 0 0 rgba(110, 205, 199, 1),
  40px 125px 0 0 rgba(110, 205, 199, 1), 45px 125px 0 0 rgba(110, 205, 199, 1),
  50px 125px 0 0 rgba(110, 205, 199, 1), 55px 125px 0 0 rgba(110, 205, 199, 1),
  60px 125px 0 0 rgba(110, 205, 199, 1), 65px 125px 0 0 rgba(110, 205, 199, 1),
  70px 125px 0 0 rgba(110, 205, 199, 1), 75px 125px 0 0 rgba(110, 205, 199, 1),
  80px 125px 0 0 rgba(110, 205, 199, 1), 85px 125px 0 0 rgba(110, 205, 199, 1),
  90px 125px 0 0 rgba(110, 205, 199, 1), 95px 125px 0 0 rgba(110, 205, 199, 1),
  100px 125px 0 0 rgba(110, 205, 199, 1), 105px 125px 0 0 rgba(110, 205, 199, 1),
  110px 125px 0 0 rgba(110, 205, 199, 1), 115px 125px 0 0 rgba(110, 205, 199, 1),
  120px 125px 0 0 rgba(110, 205, 199, 1), 125px 125px 0 0 rgba(110, 205, 199, 1),
  130px 125px 0 0 rgba(110, 205, 199, 1), 135px 125px 0 0 rgba(110, 205, 199, 1),
  140px 125px 0 0 rgba(110, 205, 199, 1), 145px 125px 0 0 rgba(110, 205, 199, 1),
  150px 125px 0 0 rgba(110, 205, 199, 1), 155px 125px 0 0 rgba(110, 205, 199, 1),
  160px 125px 0 0 rgba(110, 205, 199, 1), 165px 125px 0 0 rgba(110, 205, 199, 1),
  170px 125px 0 0 rgba(110, 205, 199, 1), 175px 125px 0 0 rgba(110, 205, 199, 1),
  180px 125px 0 0 rgba(110, 205, 199, 1), 185px 125px 0 0 rgba(110, 205, 199, 1),
  190px 125px 0 0 rgba(110, 205, 199, 1), 195px 125px 0 0 rgba(110, 205, 199, 1),
  200px 125px 0 0 rgba(110, 205, 199, 1), 205px 125px 0 0 rgba(110, 205, 199, 1),
  210px 125px 0 0 rgba(110, 205, 199, 1), 215px 125px 0 0 rgba(110, 205, 199, 1),
  220px 125px 0 0 rgba(110, 205, 199, 1), 225px 125px 0 0 rgba(110, 205, 199, 1),
  230px 125px 0 0 rgba(110, 205, 199, 1), 235px 125px 0 0 rgba(110, 205, 199, 1),
  240px 125px 0 0 rgba(110, 205, 199, 1), 245px 125px 0 0 rgba(110, 205, 199, 1),
  250px 125px 0 0 rgba(110, 205, 199, 1), 255px 125px 0 0 rgba(110, 205, 199, 1),
  260px 125px 0 0 rgba(110, 205, 199, 1), 265px 125px 0 0 rgba(110, 205, 199, 1),
  270px 125px 0 0 rgba(110, 205, 199, 1), 275px 125px 0 0 rgba(110, 205, 199, 1),
  280px 125px 0 0 rgba(110, 205, 199, 1), 285px 125px 0 0 rgba(110, 205, 199, 1),
  290px 125px 0 0 rgba(110, 205, 199, 1), 295px 125px 0 0 rgba(110, 205, 199, 1),
  300px 125px 0 0 rgba(110, 205, 199, 1), 305px 125px 0 0 rgba(110, 205, 199, 1),
  310px 125px 0 0 rgba(110, 205, 199, 1), 315px 125px 0 0 rgba(110, 205, 199, 1),
  320px 125px 0 0 rgba(110, 205, 199, 1), 325px 125px 0 0 rgba(110, 205, 199, 1),
  330px 125px 0 0 rgba(110, 205, 199, 1), 335px 125px 0 0 rgba(110, 205, 199, 1),
  340px 125px 0 0 rgba(110, 205, 199, 1), 345px 125px 0 0 rgba(110, 205, 199, 1),
  350px 125px 0 0 rgba(110, 205, 199, 1), 355px 125px 0 0 rgba(110, 205, 199, 1),
  360px 125px 0 0 rgba(110, 205, 199, 1), 365px 125px 0 0 rgba(110, 205, 199, 1),
  370px 125px 0 0 rgba(110, 205, 199, 1), 375px 125px 0 0 rgba(110, 205, 199, 1),
  380px 125px 0 0 rgba(110, 205, 199, 1), 385px 125px 0 0 rgba(110, 205, 199, 1),
  390px 125px 0 0 rgba(110, 205, 199, 1), 395px 125px 0 0 rgba(110, 205, 199, 1),
  400px 125px 0 0 rgba(110, 205, 199, 1), 405px 125px 0 0 rgba(110, 205, 199, 1),
  410px 125px 0 0 rgba(110, 205, 199, 1), 415px 125px 0 0 rgba(110, 205, 199, 1),
  420px 125px 0 0 rgba(110, 205, 199, 1), 425px 125px 0 0 rgba(110, 205, 199, 1),
  430px 125px 0 0 rgba(110, 205, 199, 1), 435px 125px 0 0 rgba(110, 205, 199, 1),
  440px 125px 0 0 rgba(110, 205, 199, 1), 445px 125px 0 0 rgba(110, 205, 199, 1),
  450px 125px 0 0 rgba(110, 205, 199, 1), 455px 125px 0 0 rgba(110, 205, 199, 1),
  460px 125px 0 0 rgba(110, 205, 199, 1), 465px 125px 0 0 rgba(110, 205, 199, 1),
  470px 125px 0 0 rgba(110, 205, 199, 1), 475px 125px 0 0 rgba(110, 205, 199, 1),
  480px 125px 0 0 rgba(110, 205, 199, 1), 485px 125px 0 0 rgba(110, 205, 199, 1),
  490px 125px 0 0 rgba(110, 205, 199, 1), 495px 125px 0 0 rgba(110, 205, 199, 1),
  500px 125px 0 0 rgba(110, 205, 199, 1), 505px 125px 0 0 rgba(110, 205, 199, 1),
  510px 125px 0 0 rgba(110, 205, 199, 1), 515px 125px 0 0 rgba(110, 205, 199, 1),
  520px 125px 0 0 rgba(110, 205, 199, 1), 525px 125px 0 0 rgba(110, 205, 199, 1),
  530px 125px 0 0 rgba(110, 205, 199, 1), 535px 125px 0 0 rgba(110, 205, 199, 1),
  540px 125px 0 0 rgba(110, 205, 199, 1), 545px 125px 0 0 rgba(110, 205, 199, 1),
  550px 125px 0 0 rgba(110, 205, 199, 1), 555px 125px 0 0 rgba(110, 205, 199, 1),
  560px 125px 0 0 rgba(110, 205, 199, 1), 565px 125px 0 0 rgba(110, 205, 199, 1),
  570px 125px 0 0 rgba(110, 205, 199, 1), 575px 125px 0 0 rgba(110, 205, 199, 1),
  580px 125px 0 0 rgba(110, 205, 199, 1), 585px 125px 0 0 rgba(110, 205, 199, 1),
  590px 125px 0 0 rgba(110, 205, 199, 1), 595px 125px 0 0 rgba(110, 205, 199, 1),
  600px 125px 0 0 rgba(110, 205, 199, 1), 605px 125px 0 0 rgba(110, 205, 199, 1),
  610px 125px 0 0 rgba(110, 205, 199, 1), 615px 125px 0 0 rgba(110, 205, 199, 1),
  620px 125px 0 0 rgba(110, 205, 199, 1), 625px 125px 0 0 rgba(110, 205, 199, 1),
  630px 125px 0 0 rgba(110, 205, 199, 1), 635px 125px 0 0 rgba(110, 205, 199, 1),
  640px 125px 0 0 rgba(110, 205, 199, 1), 645px 125px 0 0 rgba(110, 205, 199, 1),
  650px 125px 0 0 rgba(110, 205, 199, 1), 655px 125px 0 0 rgba(110, 205, 199, 1),
  660px 125px 0 0 rgba(110, 205, 199, 1), 665px 125px 0 0 rgba(110, 205, 199, 1),
  670px 125px 0 0 rgba(110, 205, 199, 1), 675px 125px 0 0 rgba(110, 205, 199, 1),
  680px 125px 0 0 rgba(110, 205, 199, 1), 685px 125px 0 0 rgba(203, 109, 181, 1),
  690px 125px 0 0 rgba(255, 205, 234, 1), 695px 125px 0 0 rgba(255, 205, 234, 1),
  700px 125px 0 0 rgba(168, 90, 150, 1), 705px 125px 0 0 rgba(203, 109, 181, 1),
  5px 130px 0 0 rgba(203, 109, 181, 1), 10px 130px 0 0 rgba(252, 231, 243, 1),
  15px 130px 0 0 rgba(255, 205, 234, 1), 20px 130px 0 0 rgba(255, 205, 234, 1),
  25px 130px 0 0 rgba(203, 109, 181, 1), 30px 130px 0 0 rgba(110, 205, 199, 1),
  35px 130px 0 0 rgba(110, 205, 199, 1), 40px 130px 0 0 rgba(110, 205, 199, 1),
  45px 130px 0 0 rgba(110, 205, 199, 1), 50px 130px 0 0 rgba(110, 205, 199, 1),
  55px 130px 0 0 rgba(110, 205, 199, 1), 60px 130px 0 0 rgba(110, 205, 199, 1),
  65px 130px 0 0 rgba(110, 205, 199, 1), 70px 130px 0 0 rgba(110, 205, 199, 1),
  75px 130px 0 0 rgba(110, 205, 199, 1), 80px 130px 0 0 rgba(110, 205, 199, 1),
  85px 130px 0 0 rgba(110, 205, 199, 1), 90px 130px 0 0 rgba(110, 205, 199, 1),
  95px 130px 0 0 rgba(110, 205, 199, 1), 100px 130px 0 0 rgba(110, 205, 199, 1),
  105px 130px 0 0 rgba(110, 205, 199, 1), 110px 130px 0 0 rgba(110, 205, 199, 1),
  115px 130px 0 0 rgba(110, 205, 199, 1), 120px 130px 0 0 rgba(110, 205, 199, 1),
  125px 130px 0 0 rgba(110, 205, 199, 1), 130px 130px 0 0 rgba(110, 205, 199, 1),
  135px 130px 0 0 rgba(110, 205, 199, 1), 140px 130px 0 0 rgba(110, 205, 199, 1),
  145px 130px 0 0 rgba(110, 205, 199, 1), 150px 130px 0 0 rgba(110, 205, 199, 1),
  155px 130px 0 0 rgba(110, 205, 199, 1), 160px 130px 0 0 rgba(110, 205, 199, 1),
  165px 130px 0 0 rgba(110, 205, 199, 1), 170px 130px 0 0 rgba(110, 205, 199, 1),
  175px 130px 0 0 rgba(110, 205, 199, 1), 180px 130px 0 0 rgba(110, 205, 199, 1),
  185px 130px 0 0 rgba(110, 205, 199, 1), 190px 130px 0 0 rgba(110, 205, 199, 1),
  195px 130px 0 0 rgba(110, 205, 199, 1), 200px 130px 0 0 rgba(110, 205, 199, 1),
  205px 130px 0 0 rgba(110, 205, 199, 1), 210px 130px 0 0 rgba(110, 205, 199, 1),
  215px 130px 0 0 rgba(110, 205, 199, 1), 220px 130px 0 0 rgba(110, 205, 199, 1),
  225px 130px 0 0 rgba(110, 205, 199, 1), 230px 130px 0 0 rgba(110, 205, 199, 1),
  235px 130px 0 0 rgba(110, 205, 199, 1), 240px 130px 0 0 rgba(110, 205, 199, 1),
  245px 130px 0 0 rgba(110, 205, 199, 1), 250px 130px 0 0 rgba(110, 205, 199, 1),
  255px 130px 0 0 rgba(110, 205, 199, 1), 260px 130px 0 0 rgba(110, 205, 199, 1),
  265px 130px 0 0 rgba(110, 205, 199, 1), 270px 130px 0 0 rgba(110, 205, 199, 1),
  275px 130px 0 0 rgba(110, 205, 199, 1), 280px 130px 0 0 rgba(110, 205, 199, 1),
  285px 130px 0 0 rgba(110, 205, 199, 1), 290px 130px 0 0 rgba(110, 205, 199, 1),
  295px 130px 0 0 rgba(110, 205, 199, 1), 300px 130px 0 0 rgba(110, 205, 199, 1),
  305px 130px 0 0 rgba(110, 205, 199, 1), 310px 130px 0 0 rgba(110, 205, 199, 1),
  315px 130px 0 0 rgba(110, 205, 199, 1), 320px 130px 0 0 rgba(110, 205, 199, 1),
  325px 130px 0 0 rgba(110, 205, 199, 1), 330px 130px 0 0 rgba(110, 205, 199, 1),
  335px 130px 0 0 rgba(110, 205, 199, 1), 340px 130px 0 0 rgba(110, 205, 199, 1),
  345px 130px 0 0 rgba(110, 205, 199, 1), 350px 130px 0 0 rgba(110, 205, 199, 1),
  355px 130px 0 0 rgba(110, 205, 199, 1), 360px 130px 0 0 rgba(110, 205, 199, 1),
  365px 130px 0 0 rgba(110, 205, 199, 1), 370px 130px 0 0 rgba(110, 205, 199, 1),
  375px 130px 0 0 rgba(110, 205, 199, 1), 380px 130px 0 0 rgba(110, 205, 199, 1),
  385px 130px 0 0 rgba(110, 205, 199, 1), 390px 130px 0 0 rgba(110, 205, 199, 1),
  395px 130px 0 0 rgba(110, 205, 199, 1), 400px 130px 0 0 rgba(110, 205, 199, 1),
  405px 130px 0 0 rgba(110, 205, 199, 1), 410px 130px 0 0 rgba(110, 205, 199, 1),
  415px 130px 0 0 rgba(110, 205, 199, 1), 420px 130px 0 0 rgba(110, 205, 199, 1),
  425px 130px 0 0 rgba(110, 205, 199, 1), 430px 130px 0 0 rgba(110, 205, 199, 1),
  435px 130px 0 0 rgba(110, 205, 199, 1), 440px 130px 0 0 rgba(110, 205, 199, 1),
  445px 130px 0 0 rgba(110, 205, 199, 1), 450px 130px 0 0 rgba(110, 205, 199, 1),
  455px 130px 0 0 rgba(110, 205, 199, 1), 460px 130px 0 0 rgba(110, 205, 199, 1),
  465px 130px 0 0 rgba(110, 205, 199, 1), 470px 130px 0 0 rgba(110, 205, 199, 1),
  475px 130px 0 0 rgba(110, 205, 199, 1), 480px 130px 0 0 rgba(110, 205, 199, 1),
  485px 130px 0 0 rgba(110, 205, 199, 1), 490px 130px 0 0 rgba(110, 205, 199, 1),
  495px 130px 0 0 rgba(110, 205, 199, 1), 500px 130px 0 0 rgba(110, 205, 199, 1),
  505px 130px 0 0 rgba(110, 205, 199, 1), 510px 130px 0 0 rgba(110, 205, 199, 1),
  515px 130px 0 0 rgba(110, 205, 199, 1), 520px 130px 0 0 rgba(110, 205, 199, 1),
  525px 130px 0 0 rgba(110, 205, 199, 1), 530px 130px 0 0 rgba(110, 205, 199, 1),
  535px 130px 0 0 rgba(110, 205, 199, 1), 540px 130px 0 0 rgba(110, 205, 199, 1),
  545px 130px 0 0 rgba(110, 205, 199, 1), 550px 130px 0 0 rgba(110, 205, 199, 1),
  555px 130px 0 0 rgba(110, 205, 199, 1), 560px 130px 0 0 rgba(110, 205, 199, 1),
  565px 130px 0 0 rgba(110, 205, 199, 1), 570px 130px 0 0 rgba(110, 205, 199, 1),
  575px 130px 0 0 rgba(110, 205, 199, 1), 580px 130px 0 0 rgba(110, 205, 199, 1),
  585px 130px 0 0 rgba(110, 205, 199, 1), 590px 130px 0 0 rgba(110, 205, 199, 1),
  595px 130px 0 0 rgba(110, 205, 199, 1), 600px 130px 0 0 rgba(110, 205, 199, 1),
  605px 130px 0 0 rgba(110, 205, 199, 1), 610px 130px 0 0 rgba(110, 205, 199, 1),
  615px 130px 0 0 rgba(110, 205, 199, 1), 620px 130px 0 0 rgba(110, 205, 199, 1),
  625px 130px 0 0 rgba(110, 205, 199, 1), 630px 130px 0 0 rgba(110, 205, 199, 1),
  635px 130px 0 0 rgba(110, 205, 199, 1), 640px 130px 0 0 rgba(110, 205, 199, 1),
  645px 130px 0 0 rgba(110, 205, 199, 1), 650px 130px 0 0 rgba(110, 205, 199, 1),
  655px 130px 0 0 rgba(110, 205, 199, 1), 660px 130px 0 0 rgba(110, 205, 199, 1),
  665px 130px 0 0 rgba(110, 205, 199, 1), 670px 130px 0 0 rgba(110, 205, 199, 1),
  675px 130px 0 0 rgba(110, 205, 199, 1), 680px 130px 0 0 rgba(110, 205, 199, 1),
  685px 130px 0 0 rgba(203, 109, 181, 1), 690px 130px 0 0 rgba(255, 205, 234, 1),
  695px 130px 0 0 rgba(255, 205, 234, 1), 700px 130px 0 0 rgba(168, 90, 150, 1),
  705px 130px 0 0 rgba(203, 109, 181, 1), 5px 135px 0 0 rgba(203, 109, 181, 1),
  10px 135px 0 0 rgba(252, 231, 243, 1), 15px 135px 0 0 rgba(255, 205, 234, 1),
  20px 135px 0 0 rgba(255, 205, 234, 1), 25px 135px 0 0 rgba(203, 109, 181, 1),
  30px 135px 0 0 rgba(110, 205, 199, 1), 35px 135px 0 0 rgba(110, 205, 199, 1),
  40px 135px 0 0 rgba(110, 205, 199, 1), 45px 135px 0 0 rgba(110, 205, 199, 1),
  50px 135px 0 0 rgba(110, 205, 199, 1), 55px 135px 0 0 rgba(110, 205, 199, 1),
  60px 135px 0 0 rgba(110, 205, 199, 1), 65px 135px 0 0 rgba(110, 205, 199, 1),
  70px 135px 0 0 rgba(110, 205, 199, 1), 75px 135px 0 0 rgba(110, 205, 199, 1),
  80px 135px 0 0 rgba(110, 205, 199, 1), 85px 135px 0 0 rgba(110, 205, 199, 1),
  90px 135px 0 0 rgba(110, 205, 199, 1), 95px 135px 0 0 rgba(110, 205, 199, 1),
  100px 135px 0 0 rgba(110, 205, 199, 1), 105px 135px 0 0 rgba(110, 205, 199, 1),
  110px 135px 0 0 rgba(110, 205, 199, 1), 115px 135px 0 0 rgba(110, 205, 199, 1),
  120px 135px 0 0 rgba(110, 205, 199, 1), 125px 135px 0 0 rgba(110, 205, 199, 1),
  130px 135px 0 0 rgba(110, 205, 199, 1), 135px 135px 0 0 rgba(110, 205, 199, 1),
  140px 135px 0 0 rgba(110, 205, 199, 1), 145px 135px 0 0 rgba(110, 205, 199, 1),
  150px 135px 0 0 rgba(110, 205, 199, 1), 155px 135px 0 0 rgba(110, 205, 199, 1),
  160px 135px 0 0 rgba(110, 205, 199, 1), 165px 135px 0 0 rgba(110, 205, 199, 1),
  170px 135px 0 0 rgba(110, 205, 199, 1), 175px 135px 0 0 rgba(110, 205, 199, 1),
  180px 135px 0 0 rgba(110, 205, 199, 1), 185px 135px 0 0 rgba(110, 205, 199, 1),
  190px 135px 0 0 rgba(110, 205, 199, 1), 195px 135px 0 0 rgba(110, 205, 199, 1),
  200px 135px 0 0 rgba(110, 205, 199, 1), 205px 135px 0 0 rgba(110, 205, 199, 1),
  210px 135px 0 0 rgba(110, 205, 199, 1), 215px 135px 0 0 rgba(110, 205, 199, 1),
  220px 135px 0 0 rgba(110, 205, 199, 1), 225px 135px 0 0 rgba(110, 205, 199, 1),
  230px 135px 0 0 rgba(110, 205, 199, 1), 235px 135px 0 0 rgba(110, 205, 199, 1),
  240px 135px 0 0 rgba(110, 205, 199, 1), 245px 135px 0 0 rgba(110, 205, 199, 1),
  250px 135px 0 0 rgba(110, 205, 199, 1), 255px 135px 0 0 rgba(110, 205, 199, 1),
  260px 135px 0 0 rgba(110, 205, 199, 1), 265px 135px 0 0 rgba(110, 205, 199, 1),
  270px 135px 0 0 rgba(110, 205, 199, 1), 275px 135px 0 0 rgba(110, 205, 199, 1),
  280px 135px 0 0 rgba(110, 205, 199, 1), 285px 135px 0 0 rgba(110, 205, 199, 1),
  290px 135px 0 0 rgba(110, 205, 199, 1), 295px 135px 0 0 rgba(110, 205, 199, 1),
  300px 135px 0 0 rgba(110, 205, 199, 1), 305px 135px 0 0 rgba(110, 205, 199, 1),
  310px 135px 0 0 rgba(110, 205, 199, 1), 315px 135px 0 0 rgba(110, 205, 199, 1),
  320px 135px 0 0 rgba(110, 205, 199, 1), 325px 135px 0 0 rgba(110, 205, 199, 1),
  330px 135px 0 0 rgba(110, 205, 199, 1), 335px 135px 0 0 rgba(110, 205, 199, 1),
  340px 135px 0 0 rgba(110, 205, 199, 1), 345px 135px 0 0 rgba(110, 205, 199, 1),
  350px 135px 0 0 rgba(110, 205, 199, 1), 355px 135px 0 0 rgba(110, 205, 199, 1),
  360px 135px 0 0 rgba(110, 205, 199, 1), 365px 135px 0 0 rgba(110, 205, 199, 1),
  370px 135px 0 0 rgba(110, 205, 199, 1), 375px 135px 0 0 rgba(110, 205, 199, 1),
  380px 135px 0 0 rgba(110, 205, 199, 1), 385px 135px 0 0 rgba(110, 205, 199, 1),
  390px 135px 0 0 rgba(110, 205, 199, 1), 395px 135px 0 0 rgba(110, 205, 199, 1),
  400px 135px 0 0 rgba(110, 205, 199, 1), 405px 135px 0 0 rgba(110, 205, 199, 1),
  410px 135px 0 0 rgba(110, 205, 199, 1), 415px 135px 0 0 rgba(110, 205, 199, 1),
  420px 135px 0 0 rgba(110, 205, 199, 1), 425px 135px 0 0 rgba(110, 205, 199, 1),
  430px 135px 0 0 rgba(110, 205, 199, 1), 435px 135px 0 0 rgba(110, 205, 199, 1),
  440px 135px 0 0 rgba(110, 205, 199, 1), 445px 135px 0 0 rgba(110, 205, 199, 1),
  450px 135px 0 0 rgba(110, 205, 199, 1), 455px 135px 0 0 rgba(110, 205, 199, 1),
  460px 135px 0 0 rgba(110, 205, 199, 1), 465px 135px 0 0 rgba(110, 205, 199, 1),
  470px 135px 0 0 rgba(110, 205, 199, 1), 475px 135px 0 0 rgba(110, 205, 199, 1),
  480px 135px 0 0 rgba(110, 205, 199, 1), 485px 135px 0 0 rgba(110, 205, 199, 1),
  490px 135px 0 0 rgba(110, 205, 199, 1), 495px 135px 0 0 rgba(110, 205, 199, 1),
  500px 135px 0 0 rgba(110, 205, 199, 1), 505px 135px 0 0 rgba(110, 205, 199, 1),
  510px 135px 0 0 rgba(110, 205, 199, 1), 515px 135px 0 0 rgba(110, 205, 199, 1),
  520px 135px 0 0 rgba(110, 205, 199, 1), 525px 135px 0 0 rgba(110, 205, 199, 1),
  530px 135px 0 0 rgba(110, 205, 199, 1), 535px 135px 0 0 rgba(110, 205, 199, 1),
  540px 135px 0 0 rgba(110, 205, 199, 1), 545px 135px 0 0 rgba(110, 205, 199, 1),
  550px 135px 0 0 rgba(110, 205, 199, 1), 555px 135px 0 0 rgba(110, 205, 199, 1),
  560px 135px 0 0 rgba(110, 205, 199, 1), 565px 135px 0 0 rgba(110, 205, 199, 1),
  570px 135px 0 0 rgba(110, 205, 199, 1), 575px 135px 0 0 rgba(110, 205, 199, 1),
  580px 135px 0 0 rgba(110, 205, 199, 1), 585px 135px 0 0 rgba(110, 205, 199, 1),
  590px 135px 0 0 rgba(110, 205, 199, 1), 595px 135px 0 0 rgba(110, 205, 199, 1),
  600px 135px 0 0 rgba(110, 205, 199, 1), 605px 135px 0 0 rgba(110, 205, 199, 1),
  610px 135px 0 0 rgba(110, 205, 199, 1), 615px 135px 0 0 rgba(110, 205, 199, 1),
  620px 135px 0 0 rgba(110, 205, 199, 1), 625px 135px 0 0 rgba(110, 205, 199, 1),
  630px 135px 0 0 rgba(110, 205, 199, 1), 635px 135px 0 0 rgba(110, 205, 199, 1),
  640px 135px 0 0 rgba(110, 205, 199, 1), 645px 135px 0 0 rgba(110, 205, 199, 1),
  650px 135px 0 0 rgba(110, 205, 199, 1), 655px 135px 0 0 rgba(110, 205, 199, 1),
  660px 135px 0 0 rgba(110, 205, 199, 1), 665px 135px 0 0 rgba(110, 205, 199, 1),
  670px 135px 0 0 rgba(110, 205, 199, 1), 675px 135px 0 0 rgba(110, 205, 199, 1),
  680px 135px 0 0 rgba(110, 205, 199, 1), 685px 135px 0 0 rgba(203, 109, 181, 1),
  690px 135px 0 0 rgba(255, 205, 234, 1), 695px 135px 0 0 rgba(255, 205, 234, 1),
  700px 135px 0 0 rgba(168, 90, 150, 1), 705px 135px 0 0 rgba(203, 109, 181, 1),
  5px 140px 0 0 rgba(203, 109, 181, 1), 10px 140px 0 0 rgba(252, 231, 243, 1),
  15px 140px 0 0 rgba(255, 205, 234, 1), 20px 140px 0 0 rgba(255, 205, 234, 1),
  25px 140px 0 0 rgba(203, 109, 181, 1), 30px 140px 0 0 rgba(110, 205, 199, 1),
  35px 140px 0 0 rgba(110, 205, 199, 1), 40px 140px 0 0 rgba(110, 205, 199, 1),
  45px 140px 0 0 rgba(110, 205, 199, 1), 50px 140px 0 0 rgba(110, 205, 199, 1),
  55px 140px 0 0 rgba(110, 205, 199, 1), 60px 140px 0 0 rgba(110, 205, 199, 1),
  65px 140px 0 0 rgba(110, 205, 199, 1), 70px 140px 0 0 rgba(110, 205, 199, 1),
  75px 140px 0 0 rgba(110, 205, 199, 1), 80px 140px 0 0 rgba(110, 205, 199, 1),
  85px 140px 0 0 rgba(110, 205, 199, 1), 90px 140px 0 0 rgba(110, 205, 199, 1),
  95px 140px 0 0 rgba(110, 205, 199, 1), 100px 140px 0 0 rgba(110, 205, 199, 1),
  105px 140px 0 0 rgba(110, 205, 199, 1), 110px 140px 0 0 rgba(110, 205, 199, 1),
  115px 140px 0 0 rgba(110, 205, 199, 1), 120px 140px 0 0 rgba(110, 205, 199, 1),
  125px 140px 0 0 rgba(110, 205, 199, 1), 130px 140px 0 0 rgba(110, 205, 199, 1),
  135px 140px 0 0 rgba(110, 205, 199, 1), 140px 140px 0 0 rgba(110, 205, 199, 1),
  145px 140px 0 0 rgba(110, 205, 199, 1), 150px 140px 0 0 rgba(110, 205, 199, 1),
  155px 140px 0 0 rgba(110, 205, 199, 1), 160px 140px 0 0 rgba(110, 205, 199, 1),
  165px 140px 0 0 rgba(110, 205, 199, 1), 170px 140px 0 0 rgba(110, 205, 199, 1),
  175px 140px 0 0 rgba(110, 205, 199, 1), 180px 140px 0 0 rgba(110, 205, 199, 1),
  185px 140px 0 0 rgba(110, 205, 199, 1), 190px 140px 0 0 rgba(110, 205, 199, 1),
  195px 140px 0 0 rgba(110, 205, 199, 1), 200px 140px 0 0 rgba(110, 205, 199, 1),
  205px 140px 0 0 rgba(110, 205, 199, 1), 210px 140px 0 0 rgba(110, 205, 199, 1),
  215px 140px 0 0 rgba(110, 205, 199, 1), 220px 140px 0 0 rgba(110, 205, 199, 1),
  225px 140px 0 0 rgba(110, 205, 199, 1), 230px 140px 0 0 rgba(110, 205, 199, 1),
  235px 140px 0 0 rgba(110, 205, 199, 1), 240px 140px 0 0 rgba(110, 205, 199, 1),
  245px 140px 0 0 rgba(110, 205, 199, 1), 250px 140px 0 0 rgba(110, 205, 199, 1),
  255px 140px 0 0 rgba(110, 205, 199, 1), 260px 140px 0 0 rgba(110, 205, 199, 1),
  265px 140px 0 0 rgba(110, 205, 199, 1), 270px 140px 0 0 rgba(110, 205, 199, 1),
  275px 140px 0 0 rgba(110, 205, 199, 1), 280px 140px 0 0 rgba(110, 205, 199, 1),
  285px 140px 0 0 rgba(110, 205, 199, 1), 290px 140px 0 0 rgba(110, 205, 199, 1),
  295px 140px 0 0 rgba(110, 205, 199, 1), 300px 140px 0 0 rgba(110, 205, 199, 1),
  305px 140px 0 0 rgba(110, 205, 199, 1), 310px 140px 0 0 rgba(110, 205, 199, 1),
  315px 140px 0 0 rgba(110, 205, 199, 1), 320px 140px 0 0 rgba(110, 205, 199, 1),
  325px 140px 0 0 rgba(110, 205, 199, 1), 330px 140px 0 0 rgba(110, 205, 199, 1),
  335px 140px 0 0 rgba(110, 205, 199, 1), 340px 140px 0 0 rgba(110, 205, 199, 1),
  345px 140px 0 0 rgba(110, 205, 199, 1), 350px 140px 0 0 rgba(110, 205, 199, 1),
  355px 140px 0 0 rgba(110, 205, 199, 1), 360px 140px 0 0 rgba(110, 205, 199, 1),
  365px 140px 0 0 rgba(110, 205, 199, 1), 370px 140px 0 0 rgba(110, 205, 199, 1),
  375px 140px 0 0 rgba(110, 205, 199, 1), 380px 140px 0 0 rgba(110, 205, 199, 1),
  385px 140px 0 0 rgba(110, 205, 199, 1), 390px 140px 0 0 rgba(110, 205, 199, 1),
  395px 140px 0 0 rgba(110, 205, 199, 1), 400px 140px 0 0 rgba(110, 205, 199, 1),
  405px 140px 0 0 rgba(110, 205, 199, 1), 410px 140px 0 0 rgba(110, 205, 199, 1),
  415px 140px 0 0 rgba(110, 205, 199, 1), 420px 140px 0 0 rgba(110, 205, 199, 1),
  425px 140px 0 0 rgba(110, 205, 199, 1), 430px 140px 0 0 rgba(110, 205, 199, 1),
  435px 140px 0 0 rgba(110, 205, 199, 1), 440px 140px 0 0 rgba(110, 205, 199, 1),
  445px 140px 0 0 rgba(110, 205, 199, 1), 450px 140px 0 0 rgba(110, 205, 199, 1),
  455px 140px 0 0 rgba(110, 205, 199, 1), 460px 140px 0 0 rgba(110, 205, 199, 1),
  465px 140px 0 0 rgba(110, 205, 199, 1), 470px 140px 0 0 rgba(110, 205, 199, 1),
  475px 140px 0 0 rgba(110, 205, 199, 1), 480px 140px 0 0 rgba(110, 205, 199, 1),
  485px 140px 0 0 rgba(110, 205, 199, 1), 490px 140px 0 0 rgba(110, 205, 199, 1),
  495px 140px 0 0 rgba(110, 205, 199, 1), 500px 140px 0 0 rgba(110, 205, 199, 1),
  505px 140px 0 0 rgba(110, 205, 199, 1), 510px 140px 0 0 rgba(110, 205, 199, 1),
  515px 140px 0 0 rgba(110, 205, 199, 1), 520px 140px 0 0 rgba(110, 205, 199, 1),
  525px 140px 0 0 rgba(110, 205, 199, 1), 530px 140px 0 0 rgba(110, 205, 199, 1),
  535px 140px 0 0 rgba(110, 205, 199, 1), 540px 140px 0 0 rgba(110, 205, 199, 1),
  545px 140px 0 0 rgba(110, 205, 199, 1), 550px 140px 0 0 rgba(110, 205, 199, 1),
  555px 140px 0 0 rgba(110, 205, 199, 1), 560px 140px 0 0 rgba(110, 205, 199, 1),
  565px 140px 0 0 rgba(110, 205, 199, 1), 570px 140px 0 0 rgba(110, 205, 199, 1),
  575px 140px 0 0 rgba(110, 205, 199, 1), 580px 140px 0 0 rgba(110, 205, 199, 1),
  585px 140px 0 0 rgba(110, 205, 199, 1), 590px 140px 0 0 rgba(110, 205, 199, 1),
  595px 140px 0 0 rgba(110, 205, 199, 1), 600px 140px 0 0 rgba(110, 205, 199, 1),
  605px 140px 0 0 rgba(110, 205, 199, 1), 610px 140px 0 0 rgba(110, 205, 199, 1),
  615px 140px 0 0 rgba(110, 205, 199, 1), 620px 140px 0 0 rgba(110, 205, 199, 1),
  625px 140px 0 0 rgba(110, 205, 199, 1), 630px 140px 0 0 rgba(110, 205, 199, 1),
  635px 140px 0 0 rgba(110, 205, 199, 1), 640px 140px 0 0 rgba(110, 205, 199, 1),
  645px 140px 0 0 rgba(110, 205, 199, 1), 650px 140px 0 0 rgba(110, 205, 199, 1),
  655px 140px 0 0 rgba(110, 205, 199, 1), 660px 140px 0 0 rgba(110, 205, 199, 1),
  665px 140px 0 0 rgba(110, 205, 199, 1), 670px 140px 0 0 rgba(110, 205, 199, 1),
  675px 140px 0 0 rgba(110, 205, 199, 1), 680px 140px 0 0 rgba(110, 205, 199, 1),
  685px 140px 0 0 rgba(203, 109, 181, 1), 690px 140px 0 0 rgba(255, 205, 234, 1),
  695px 140px 0 0 rgba(255, 205, 234, 1), 700px 140px 0 0 rgba(168, 90, 150, 1),
  705px 140px 0 0 rgba(203, 109, 181, 1), 5px 145px 0 0 rgba(203, 109, 181, 1),
  10px 145px 0 0 rgba(252, 231, 243, 1), 15px 145px 0 0 rgba(255, 205, 234, 1),
  20px 145px 0 0 rgba(255, 205, 234, 1), 25px 145px 0 0 rgba(203, 109, 181, 1),
  30px 145px 0 0 rgba(110, 205, 199, 1), 35px 145px 0 0 rgba(110, 205, 199, 1),
  40px 145px 0 0 rgba(110, 205, 199, 1), 45px 145px 0 0 rgba(110, 205, 199, 1),
  50px 145px 0 0 rgba(110, 205, 199, 1), 55px 145px 0 0 rgba(110, 205, 199, 1),
  60px 145px 0 0 rgba(110, 205, 199, 1), 65px 145px 0 0 rgba(110, 205, 199, 1),
  70px 145px 0 0 rgba(110, 205, 199, 1), 75px 145px 0 0 rgba(110, 205, 199, 1),
  80px 145px 0 0 rgba(110, 205, 199, 1), 85px 145px 0 0 rgba(110, 205, 199, 1),
  90px 145px 0 0 rgba(110, 205, 199, 1), 95px 145px 0 0 rgba(110, 205, 199, 1),
  100px 145px 0 0 rgba(110, 205, 199, 1), 105px 145px 0 0 rgba(110, 205, 199, 1),
  110px 145px 0 0 rgba(110, 205, 199, 1), 115px 145px 0 0 rgba(110, 205, 199, 1),
  120px 145px 0 0 rgba(110, 205, 199, 1), 125px 145px 0 0 rgba(110, 205, 199, 1),
  130px 145px 0 0 rgba(110, 205, 199, 1), 135px 145px 0 0 rgba(110, 205, 199, 1),
  140px 145px 0 0 rgba(110, 205, 199, 1), 145px 145px 0 0 rgba(110, 205, 199, 1),
  150px 145px 0 0 rgba(110, 205, 199, 1), 155px 145px 0 0 rgba(110, 205, 199, 1),
  160px 145px 0 0 rgba(110, 205, 199, 1), 165px 145px 0 0 rgba(110, 205, 199, 1),
  170px 145px 0 0 rgba(110, 205, 199, 1), 175px 145px 0 0 rgba(110, 205, 199, 1),
  180px 145px 0 0 rgba(110, 205, 199, 1), 185px 145px 0 0 rgba(110, 205, 199, 1),
  190px 145px 0 0 rgba(110, 205, 199, 1), 195px 145px 0 0 rgba(110, 205, 199, 1),
  200px 145px 0 0 rgba(110, 205, 199, 1), 205px 145px 0 0 rgba(110, 205, 199, 1),
  210px 145px 0 0 rgba(110, 205, 199, 1), 215px 145px 0 0 rgba(110, 205, 199, 1),
  220px 145px 0 0 rgba(110, 205, 199, 1), 225px 145px 0 0 rgba(110, 205, 199, 1),
  230px 145px 0 0 rgba(110, 205, 199, 1), 235px 145px 0 0 rgba(110, 205, 199, 1),
  240px 145px 0 0 rgba(110, 205, 199, 1), 245px 145px 0 0 rgba(110, 205, 199, 1),
  250px 145px 0 0 rgba(110, 205, 199, 1), 255px 145px 0 0 rgba(110, 205, 199, 1),
  260px 145px 0 0 rgba(110, 205, 199, 1), 265px 145px 0 0 rgba(110, 205, 199, 1),
  270px 145px 0 0 rgba(110, 205, 199, 1), 275px 145px 0 0 rgba(110, 205, 199, 1),
  280px 145px 0 0 rgba(110, 205, 199, 1), 285px 145px 0 0 rgba(110, 205, 199, 1),
  290px 145px 0 0 rgba(110, 205, 199, 1), 295px 145px 0 0 rgba(110, 205, 199, 1),
  300px 145px 0 0 rgba(110, 205, 199, 1), 305px 145px 0 0 rgba(110, 205, 199, 1),
  310px 145px 0 0 rgba(110, 205, 199, 1), 315px 145px 0 0 rgba(110, 205, 199, 1),
  320px 145px 0 0 rgba(110, 205, 199, 1), 325px 145px 0 0 rgba(110, 205, 199, 1),
  330px 145px 0 0 rgba(110, 205, 199, 1), 335px 145px 0 0 rgba(110, 205, 199, 1),
  340px 145px 0 0 rgba(110, 205, 199, 1), 345px 145px 0 0 rgba(110, 205, 199, 1),
  350px 145px 0 0 rgba(110, 205, 199, 1), 355px 145px 0 0 rgba(110, 205, 199, 1),
  360px 145px 0 0 rgba(110, 205, 199, 1), 365px 145px 0 0 rgba(110, 205, 199, 1),
  370px 145px 0 0 rgba(110, 205, 199, 1), 375px 145px 0 0 rgba(110, 205, 199, 1),
  380px 145px 0 0 rgba(110, 205, 199, 1), 385px 145px 0 0 rgba(110, 205, 199, 1),
  390px 145px 0 0 rgba(110, 205, 199, 1), 395px 145px 0 0 rgba(110, 205, 199, 1),
  400px 145px 0 0 rgba(110, 205, 199, 1), 405px 145px 0 0 rgba(110, 205, 199, 1),
  410px 145px 0 0 rgba(110, 205, 199, 1), 415px 145px 0 0 rgba(110, 205, 199, 1),
  420px 145px 0 0 rgba(110, 205, 199, 1), 425px 145px 0 0 rgba(110, 205, 199, 1),
  430px 145px 0 0 rgba(110, 205, 199, 1), 435px 145px 0 0 rgba(110, 205, 199, 1),
  440px 145px 0 0 rgba(110, 205, 199, 1), 445px 145px 0 0 rgba(110, 205, 199, 1),
  450px 145px 0 0 rgba(110, 205, 199, 1), 455px 145px 0 0 rgba(110, 205, 199, 1),
  460px 145px 0 0 rgba(110, 205, 199, 1), 465px 145px 0 0 rgba(110, 205, 199, 1),
  470px 145px 0 0 rgba(110, 205, 199, 1), 475px 145px 0 0 rgba(110, 205, 199, 1),
  480px 145px 0 0 rgba(110, 205, 199, 1), 485px 145px 0 0 rgba(110, 205, 199, 1),
  490px 145px 0 0 rgba(110, 205, 199, 1), 495px 145px 0 0 rgba(110, 205, 199, 1),
  500px 145px 0 0 rgba(110, 205, 199, 1), 505px 145px 0 0 rgba(110, 205, 199, 1),
  510px 145px 0 0 rgba(110, 205, 199, 1), 515px 145px 0 0 rgba(110, 205, 199, 1),
  520px 145px 0 0 rgba(110, 205, 199, 1), 525px 145px 0 0 rgba(110, 205, 199, 1),
  530px 145px 0 0 rgba(110, 205, 199, 1), 535px 145px 0 0 rgba(110, 205, 199, 1),
  540px 145px 0 0 rgba(110, 205, 199, 1), 545px 145px 0 0 rgba(110, 205, 199, 1),
  550px 145px 0 0 rgba(110, 205, 199, 1), 555px 145px 0 0 rgba(110, 205, 199, 1),
  560px 145px 0 0 rgba(110, 205, 199, 1), 565px 145px 0 0 rgba(110, 205, 199, 1),
  570px 145px 0 0 rgba(110, 205, 199, 1), 575px 145px 0 0 rgba(110, 205, 199, 1),
  580px 145px 0 0 rgba(110, 205, 199, 1), 585px 145px 0 0 rgba(110, 205, 199, 1),
  590px 145px 0 0 rgba(110, 205, 199, 1), 595px 145px 0 0 rgba(110, 205, 199, 1),
  600px 145px 0 0 rgba(110, 205, 199, 1), 605px 145px 0 0 rgba(110, 205, 199, 1),
  610px 145px 0 0 rgba(110, 205, 199, 1), 615px 145px 0 0 rgba(110, 205, 199, 1),
  620px 145px 0 0 rgba(110, 205, 199, 1), 625px 145px 0 0 rgba(110, 205, 199, 1),
  630px 145px 0 0 rgba(110, 205, 199, 1), 635px 145px 0 0 rgba(110, 205, 199, 1),
  640px 145px 0 0 rgba(110, 205, 199, 1), 645px 145px 0 0 rgba(110, 205, 199, 1),
  650px 145px 0 0 rgba(110, 205, 199, 1), 655px 145px 0 0 rgba(110, 205, 199, 1),
  660px 145px 0 0 rgba(110, 205, 199, 1), 665px 145px 0 0 rgba(110, 205, 199, 1),
  670px 145px 0 0 rgba(110, 205, 199, 1), 675px 145px 0 0 rgba(110, 205, 199, 1),
  680px 145px 0 0 rgba(110, 205, 199, 1), 685px 145px 0 0 rgba(203, 109, 181, 1),
  690px 145px 0 0 rgba(255, 205, 234, 1), 695px 145px 0 0 rgba(255, 205, 234, 1),
  700px 145px 0 0 rgba(168, 90, 150, 1), 705px 145px 0 0 rgba(203, 109, 181, 1),
  5px 150px 0 0 rgba(203, 109, 181, 1), 10px 150px 0 0 rgba(252, 231, 243, 1),
  15px 150px 0 0 rgba(255, 205, 234, 1), 20px 150px 0 0 rgba(255, 205, 234, 1),
  25px 150px 0 0 rgba(203, 109, 181, 1), 30px 150px 0 0 rgba(110, 205, 199, 1),
  35px 150px 0 0 rgba(110, 205, 199, 1), 40px 150px 0 0 rgba(110, 205, 199, 1),
  45px 150px 0 0 rgba(110, 205, 199, 1), 50px 150px 0 0 rgba(110, 205, 199, 1),
  55px 150px 0 0 rgba(255, 255, 255, 1), 60px 150px 0 0 rgba(110, 205, 199, 1),
  65px 150px 0 0 rgba(110, 205, 199, 1), 70px 150px 0 0 rgba(110, 205, 199, 1),
  75px 150px 0 0 rgba(110, 205, 199, 1), 80px 150px 0 0 rgba(110, 205, 199, 1),
  85px 150px 0 0 rgba(110, 205, 199, 1), 90px 150px 0 0 rgba(110, 205, 199, 1),
  95px 150px 0 0 rgba(255, 255, 255, 1), 100px 150px 0 0 rgba(110, 205, 199, 1),
  105px 150px 0 0 rgba(110, 205, 199, 1), 110px 150px 0 0 rgba(110, 205, 199, 1),
  115px 150px 0 0 rgba(110, 205, 199, 1), 120px 150px 0 0 rgba(110, 205, 199, 1),
  125px 150px 0 0 rgba(110, 205, 199, 1), 130px 150px 0 0 rgba(110, 205, 199, 1),
  135px 150px 0 0 rgba(255, 255, 255, 1), 140px 150px 0 0 rgba(110, 205, 199, 1),
  145px 150px 0 0 rgba(110, 205, 199, 1), 150px 150px 0 0 rgba(110, 205, 199, 1),
  155px 150px 0 0 rgba(110, 205, 199, 1), 160px 150px 0 0 rgba(110, 205, 199, 1),
  165px 150px 0 0 rgba(110, 205, 199, 1), 170px 150px 0 0 rgba(110, 205, 199, 1),
  175px 150px 0 0 rgba(255, 255, 255, 1), 180px 150px 0 0 rgba(110, 205, 199, 1),
  185px 150px 0 0 rgba(110, 205, 199, 1), 190px 150px 0 0 rgba(110, 205, 199, 1),
  195px 150px 0 0 rgba(110, 205, 199, 1), 200px 150px 0 0 rgba(110, 205, 199, 1),
  205px 150px 0 0 rgba(110, 205, 199, 1), 210px 150px 0 0 rgba(110, 205, 199, 1),
  215px 150px 0 0 rgba(255, 255, 255, 1), 220px 150px 0 0 rgba(110, 205, 199, 1),
  225px 150px 0 0 rgba(110, 205, 199, 1), 230px 150px 0 0 rgba(110, 205, 199, 1),
  235px 150px 0 0 rgba(110, 205, 199, 1), 240px 150px 0 0 rgba(110, 205, 199, 1),
  245px 150px 0 0 rgba(110, 205, 199, 1), 250px 150px 0 0 rgba(110, 205, 199, 1),
  255px 150px 0 0 rgba(255, 255, 255, 1), 260px 150px 0 0 rgba(110, 205, 199, 1),
  265px 150px 0 0 rgba(110, 205, 199, 1), 270px 150px 0 0 rgba(110, 205, 199, 1),
  275px 150px 0 0 rgba(110, 205, 199, 1), 280px 150px 0 0 rgba(110, 205, 199, 1),
  285px 150px 0 0 rgba(110, 205, 199, 1), 290px 150px 0 0 rgba(110, 205, 199, 1),
  295px 150px 0 0 rgba(255, 255, 255, 1), 300px 150px 0 0 rgba(110, 205, 199, 1),
  305px 150px 0 0 rgba(110, 205, 199, 1), 310px 150px 0 0 rgba(110, 205, 199, 1),
  315px 150px 0 0 rgba(110, 205, 199, 1), 320px 150px 0 0 rgba(110, 205, 199, 1),
  325px 150px 0 0 rgba(110, 205, 199, 1), 330px 150px 0 0 rgba(110, 205, 199, 1),
  335px 150px 0 0 rgba(255, 255, 255, 1), 340px 150px 0 0 rgba(110, 205, 199, 1),
  345px 150px 0 0 rgba(110, 205, 199, 1), 350px 150px 0 0 rgba(110, 205, 199, 1),
  355px 150px 0 0 rgba(110, 205, 199, 1), 360px 150px 0 0 rgba(110, 205, 199, 1),
  365px 150px 0 0 rgba(110, 205, 199, 1), 370px 150px 0 0 rgba(110, 205, 199, 1),
  375px 150px 0 0 rgba(255, 255, 255, 1), 380px 150px 0 0 rgba(110, 205, 199, 1),
  385px 150px 0 0 rgba(110, 205, 199, 1), 390px 150px 0 0 rgba(110, 205, 199, 1),
  395px 150px 0 0 rgba(110, 205, 199, 1), 400px 150px 0 0 rgba(110, 205, 199, 1),
  405px 150px 0 0 rgba(110, 205, 199, 1), 410px 150px 0 0 rgba(110, 205, 199, 1),
  415px 150px 0 0 rgba(255, 255, 255, 1), 420px 150px 0 0 rgba(110, 205, 199, 1),
  425px 150px 0 0 rgba(110, 205, 199, 1), 430px 150px 0 0 rgba(110, 205, 199, 1),
  435px 150px 0 0 rgba(110, 205, 199, 1), 440px 150px 0 0 rgba(110, 205, 199, 1),
  445px 150px 0 0 rgba(110, 205, 199, 1), 450px 150px 0 0 rgba(110, 205, 199, 1),
  455px 150px 0 0 rgba(255, 255, 255, 1), 460px 150px 0 0 rgba(110, 205, 199, 1),
  465px 150px 0 0 rgba(110, 205, 199, 1), 470px 150px 0 0 rgba(110, 205, 199, 1),
  475px 150px 0 0 rgba(110, 205, 199, 1), 480px 150px 0 0 rgba(110, 205, 199, 1),
  485px 150px 0 0 rgba(110, 205, 199, 1), 490px 150px 0 0 rgba(110, 205, 199, 1),
  495px 150px 0 0 rgba(255, 255, 255, 1), 500px 150px 0 0 rgba(110, 205, 199, 1),
  505px 150px 0 0 rgba(110, 205, 199, 1), 510px 150px 0 0 rgba(110, 205, 199, 1),
  515px 150px 0 0 rgba(255, 255, 255, 1), 520px 150px 0 0 rgba(110, 205, 199, 1),
  525px 150px 0 0 rgba(110, 205, 199, 1), 530px 150px 0 0 rgba(110, 205, 199, 1),
  535px 150px 0 0 rgba(255, 255, 255, 1), 540px 150px 0 0 rgba(110, 205, 199, 1),
  545px 150px 0 0 rgba(110, 205, 199, 1), 550px 150px 0 0 rgba(110, 205, 199, 1),
  555px 150px 0 0 rgba(255, 255, 255, 1), 560px 150px 0 0 rgba(110, 205, 199, 1),
  565px 150px 0 0 rgba(110, 205, 199, 1), 570px 150px 0 0 rgba(110, 205, 199, 1),
  575px 150px 0 0 rgba(255, 255, 255, 1), 580px 150px 0 0 rgba(110, 205, 199, 1),
  585px 150px 0 0 rgba(110, 205, 199, 1), 590px 150px 0 0 rgba(110, 205, 199, 1),
  595px 150px 0 0 rgba(255, 255, 255, 1), 600px 150px 0 0 rgba(110, 205, 199, 1),
  605px 150px 0 0 rgba(110, 205, 199, 1), 610px 150px 0 0 rgba(110, 205, 199, 1),
  615px 150px 0 0 rgba(255, 255, 255, 1), 620px 150px 0 0 rgba(110, 205, 199, 1),
  625px 150px 0 0 rgba(110, 205, 199, 1), 630px 150px 0 0 rgba(110, 205, 199, 1),
  635px 150px 0 0 rgba(255, 255, 255, 1), 640px 150px 0 0 rgba(110, 205, 199, 1),
  645px 150px 0 0 rgba(110, 205, 199, 1), 650px 150px 0 0 rgba(110, 205, 199, 1),
  655px 150px 0 0 rgba(255, 255, 255, 1), 660px 150px 0 0 rgba(110, 205, 199, 1),
  665px 150px 0 0 rgba(110, 205, 199, 1), 670px 150px 0 0 rgba(110, 205, 199, 1),
  675px 150px 0 0 rgba(255, 255, 255, 1), 680px 150px 0 0 rgba(110, 205, 199, 1),
  685px 150px 0 0 rgba(203, 109, 181, 1), 690px 150px 0 0 rgba(255, 205, 234, 1),
  695px 150px 0 0 rgba(255, 205, 234, 1), 700px 150px 0 0 rgba(168, 90, 150, 1),
  705px 150px 0 0 rgba(203, 109, 181, 1), 5px 155px 0 0 rgba(203, 109, 181, 1),
  10px 155px 0 0 rgba(252, 231, 243, 1), 15px 155px 0 0 rgba(255, 205, 234, 1),
  20px 155px 0 0 rgba(255, 205, 234, 1), 25px 155px 0 0 rgba(203, 109, 181, 1),
  30px 155px 0 0 rgba(110, 205, 199, 1), 35px 155px 0 0 rgba(110, 205, 199, 1),
  40px 155px 0 0 rgba(110, 205, 199, 1), 45px 155px 0 0 rgba(110, 205, 199, 1),
  50px 155px 0 0 rgba(110, 205, 199, 1), 55px 155px 0 0 rgba(110, 205, 199, 1),
  60px 155px 0 0 rgba(110, 205, 199, 1), 65px 155px 0 0 rgba(110, 205, 199, 1),
  70px 155px 0 0 rgba(110, 205, 199, 1), 75px 155px 0 0 rgba(110, 205, 199, 1),
  80px 155px 0 0 rgba(110, 205, 199, 1), 85px 155px 0 0 rgba(110, 205, 199, 1),
  90px 155px 0 0 rgba(110, 205, 199, 1), 95px 155px 0 0 rgba(110, 205, 199, 1),
  100px 155px 0 0 rgba(110, 205, 199, 1), 105px 155px 0 0 rgba(110, 205, 199, 1),
  110px 155px 0 0 rgba(110, 205, 199, 1), 115px 155px 0 0 rgba(110, 205, 199, 1),
  120px 155px 0 0 rgba(110, 205, 199, 1), 125px 155px 0 0 rgba(110, 205, 199, 1),
  130px 155px 0 0 rgba(110, 205, 199, 1), 135px 155px 0 0 rgba(110, 205, 199, 1),
  140px 155px 0 0 rgba(110, 205, 199, 1), 145px 155px 0 0 rgba(110, 205, 199, 1),
  150px 155px 0 0 rgba(110, 205, 199, 1), 155px 155px 0 0 rgba(110, 205, 199, 1),
  160px 155px 0 0 rgba(110, 205, 199, 1), 165px 155px 0 0 rgba(110, 205, 199, 1),
  170px 155px 0 0 rgba(110, 205, 199, 1), 175px 155px 0 0 rgba(110, 205, 199, 1),
  180px 155px 0 0 rgba(110, 205, 199, 1), 185px 155px 0 0 rgba(110, 205, 199, 1),
  190px 155px 0 0 rgba(110, 205, 199, 1), 195px 155px 0 0 rgba(110, 205, 199, 1),
  200px 155px 0 0 rgba(110, 205, 199, 1), 205px 155px 0 0 rgba(110, 205, 199, 1),
  210px 155px 0 0 rgba(110, 205, 199, 1), 215px 155px 0 0 rgba(110, 205, 199, 1),
  220px 155px 0 0 rgba(110, 205, 199, 1), 225px 155px 0 0 rgba(110, 205, 199, 1),
  230px 155px 0 0 rgba(110, 205, 199, 1), 235px 155px 0 0 rgba(110, 205, 199, 1),
  240px 155px 0 0 rgba(110, 205, 199, 1), 245px 155px 0 0 rgba(110, 205, 199, 1),
  250px 155px 0 0 rgba(110, 205, 199, 1), 255px 155px 0 0 rgba(110, 205, 199, 1),
  260px 155px 0 0 rgba(110, 205, 199, 1), 265px 155px 0 0 rgba(110, 205, 199, 1),
  270px 155px 0 0 rgba(110, 205, 199, 1), 275px 155px 0 0 rgba(110, 205, 199, 1),
  280px 155px 0 0 rgba(110, 205, 199, 1), 285px 155px 0 0 rgba(110, 205, 199, 1),
  290px 155px 0 0 rgba(110, 205, 199, 1), 295px 155px 0 0 rgba(110, 205, 199, 1),
  300px 155px 0 0 rgba(110, 205, 199, 1), 305px 155px 0 0 rgba(110, 205, 199, 1),
  310px 155px 0 0 rgba(110, 205, 199, 1), 315px 155px 0 0 rgba(110, 205, 199, 1),
  320px 155px 0 0 rgba(110, 205, 199, 1), 325px 155px 0 0 rgba(110, 205, 199, 1),
  330px 155px 0 0 rgba(110, 205, 199, 1), 335px 155px 0 0 rgba(110, 205, 199, 1),
  340px 155px 0 0 rgba(110, 205, 199, 1), 345px 155px 0 0 rgba(110, 205, 199, 1),
  350px 155px 0 0 rgba(110, 205, 199, 1), 355px 155px 0 0 rgba(110, 205, 199, 1),
  360px 155px 0 0 rgba(110, 205, 199, 1), 365px 155px 0 0 rgba(110, 205, 199, 1),
  370px 155px 0 0 rgba(110, 205, 199, 1), 375px 155px 0 0 rgba(110, 205, 199, 1),
  380px 155px 0 0 rgba(110, 205, 199, 1), 385px 155px 0 0 rgba(110, 205, 199, 1),
  390px 155px 0 0 rgba(110, 205, 199, 1), 395px 155px 0 0 rgba(110, 205, 199, 1),
  400px 155px 0 0 rgba(110, 205, 199, 1), 405px 155px 0 0 rgba(110, 205, 199, 1),
  410px 155px 0 0 rgba(110, 205, 199, 1), 415px 155px 0 0 rgba(110, 205, 199, 1),
  420px 155px 0 0 rgba(110, 205, 199, 1), 425px 155px 0 0 rgba(110, 205, 199, 1),
  430px 155px 0 0 rgba(110, 205, 199, 1), 435px 155px 0 0 rgba(110, 205, 199, 1),
  440px 155px 0 0 rgba(110, 205, 199, 1), 445px 155px 0 0 rgba(110, 205, 199, 1),
  450px 155px 0 0 rgba(110, 205, 199, 1), 455px 155px 0 0 rgba(110, 205, 199, 1),
  460px 155px 0 0 rgba(110, 205, 199, 1), 465px 155px 0 0 rgba(110, 205, 199, 1),
  470px 155px 0 0 rgba(110, 205, 199, 1), 475px 155px 0 0 rgba(110, 205, 199, 1),
  480px 155px 0 0 rgba(110, 205, 199, 1), 485px 155px 0 0 rgba(110, 205, 199, 1),
  490px 155px 0 0 rgba(110, 205, 199, 1), 495px 155px 0 0 rgba(110, 205, 199, 1),
  500px 155px 0 0 rgba(110, 205, 199, 1), 505px 155px 0 0 rgba(110, 205, 199, 1),
  510px 155px 0 0 rgba(110, 205, 199, 1), 515px 155px 0 0 rgba(110, 205, 199, 1),
  520px 155px 0 0 rgba(110, 205, 199, 1), 525px 155px 0 0 rgba(110, 205, 199, 1),
  530px 155px 0 0 rgba(110, 205, 199, 1), 535px 155px 0 0 rgba(110, 205, 199, 1),
  540px 155px 0 0 rgba(110, 205, 199, 1), 545px 155px 0 0 rgba(110, 205, 199, 1),
  550px 155px 0 0 rgba(110, 205, 199, 1), 555px 155px 0 0 rgba(110, 205, 199, 1),
  560px 155px 0 0 rgba(110, 205, 199, 1), 565px 155px 0 0 rgba(110, 205, 199, 1),
  570px 155px 0 0 rgba(110, 205, 199, 1), 575px 155px 0 0 rgba(110, 205, 199, 1),
  580px 155px 0 0 rgba(110, 205, 199, 1), 585px 155px 0 0 rgba(110, 205, 199, 1),
  590px 155px 0 0 rgba(110, 205, 199, 1), 595px 155px 0 0 rgba(110, 205, 199, 1),
  600px 155px 0 0 rgba(110, 205, 199, 1), 605px 155px 0 0 rgba(110, 205, 199, 1),
  610px 155px 0 0 rgba(110, 205, 199, 1), 615px 155px 0 0 rgba(110, 205, 199, 1),
  620px 155px 0 0 rgba(110, 205, 199, 1), 625px 155px 0 0 rgba(110, 205, 199, 1),
  630px 155px 0 0 rgba(110, 205, 199, 1), 635px 155px 0 0 rgba(110, 205, 199, 1),
  640px 155px 0 0 rgba(110, 205, 199, 1), 645px 155px 0 0 rgba(110, 205, 199, 1),
  650px 155px 0 0 rgba(110, 205, 199, 1), 655px 155px 0 0 rgba(110, 205, 199, 1),
  660px 155px 0 0 rgba(110, 205, 199, 1), 665px 155px 0 0 rgba(110, 205, 199, 1),
  670px 155px 0 0 rgba(110, 205, 199, 1), 675px 155px 0 0 rgba(110, 205, 199, 1),
  680px 155px 0 0 rgba(110, 205, 199, 1), 685px 155px 0 0 rgba(203, 109, 181, 1),
  690px 155px 0 0 rgba(255, 205, 234, 1), 695px 155px 0 0 rgba(255, 205, 234, 1),
  700px 155px 0 0 rgba(168, 90, 150, 1), 705px 155px 0 0 rgba(203, 109, 181, 1),
  5px 160px 0 0 rgba(203, 109, 181, 1), 10px 160px 0 0 rgba(252, 231, 243, 1),
  15px 160px 0 0 rgba(255, 205, 234, 1), 20px 160px 0 0 rgba(255, 205, 234, 1),
  25px 160px 0 0 rgba(203, 109, 181, 1), 30px 160px 0 0 rgba(110, 205, 199, 1),
  35px 160px 0 0 rgba(110, 205, 199, 1), 40px 160px 0 0 rgba(110, 205, 199, 1),
  45px 160px 0 0 rgba(255, 255, 255, 1), 50px 160px 0 0 rgba(110, 205, 199, 1),
  55px 160px 0 0 rgba(110, 205, 199, 1), 60px 160px 0 0 rgba(110, 205, 199, 1),
  65px 160px 0 0 rgba(255, 255, 255, 1), 70px 160px 0 0 rgba(110, 205, 199, 1),
  75px 160px 0 0 rgba(110, 205, 199, 1), 80px 160px 0 0 rgba(110, 205, 199, 1),
  85px 160px 0 0 rgba(255, 255, 255, 1), 90px 160px 0 0 rgba(110, 205, 199, 1),
  95px 160px 0 0 rgba(110, 205, 199, 1), 100px 160px 0 0 rgba(110, 205, 199, 1),
  105px 160px 0 0 rgba(255, 255, 255, 1), 110px 160px 0 0 rgba(110, 205, 199, 1),
  115px 160px 0 0 rgba(110, 205, 199, 1), 120px 160px 0 0 rgba(110, 205, 199, 1),
  125px 160px 0 0 rgba(255, 255, 255, 1), 130px 160px 0 0 rgba(110, 205, 199, 1),
  135px 160px 0 0 rgba(110, 205, 199, 1), 140px 160px 0 0 rgba(110, 205, 199, 1),
  145px 160px 0 0 rgba(255, 255, 255, 1), 150px 160px 0 0 rgba(110, 205, 199, 1),
  155px 160px 0 0 rgba(110, 205, 199, 1), 160px 160px 0 0 rgba(110, 205, 199, 1),
  165px 160px 0 0 rgba(255, 255, 255, 1), 170px 160px 0 0 rgba(110, 205, 199, 1),
  175px 160px 0 0 rgba(110, 205, 199, 1), 180px 160px 0 0 rgba(110, 205, 199, 1),
  185px 160px 0 0 rgba(255, 255, 255, 1), 190px 160px 0 0 rgba(110, 205, 199, 1),
  195px 160px 0 0 rgba(110, 205, 199, 1), 200px 160px 0 0 rgba(110, 205, 199, 1),
  205px 160px 0 0 rgba(255, 255, 255, 1), 210px 160px 0 0 rgba(110, 205, 199, 1),
  215px 160px 0 0 rgba(110, 205, 199, 1), 220px 160px 0 0 rgba(110, 205, 199, 1),
  225px 160px 0 0 rgba(255, 255, 255, 1), 230px 160px 0 0 rgba(110, 205, 199, 1),
  235px 160px 0 0 rgba(110, 205, 199, 1), 240px 160px 0 0 rgba(110, 205, 199, 1),
  245px 160px 0 0 rgba(255, 255, 255, 1), 250px 160px 0 0 rgba(110, 205, 199, 1),
  255px 160px 0 0 rgba(110, 205, 199, 1), 260px 160px 0 0 rgba(110, 205, 199, 1),
  265px 160px 0 0 rgba(255, 255, 255, 1), 270px 160px 0 0 rgba(110, 205, 199, 1),
  275px 160px 0 0 rgba(110, 205, 199, 1), 280px 160px 0 0 rgba(110, 205, 199, 1),
  285px 160px 0 0 rgba(255, 255, 255, 1), 290px 160px 0 0 rgba(110, 205, 199, 1),
  295px 160px 0 0 rgba(110, 205, 199, 1), 300px 160px 0 0 rgba(110, 205, 199, 1),
  305px 160px 0 0 rgba(255, 255, 255, 1), 310px 160px 0 0 rgba(110, 205, 199, 1),
  315px 160px 0 0 rgba(110, 205, 199, 1), 320px 160px 0 0 rgba(110, 205, 199, 1),
  325px 160px 0 0 rgba(255, 255, 255, 1), 330px 160px 0 0 rgba(110, 205, 199, 1),
  335px 160px 0 0 rgba(110, 205, 199, 1), 340px 160px 0 0 rgba(110, 205, 199, 1),
  345px 160px 0 0 rgba(255, 255, 255, 1), 350px 160px 0 0 rgba(110, 205, 199, 1),
  355px 160px 0 0 rgba(110, 205, 199, 1), 360px 160px 0 0 rgba(110, 205, 199, 1),
  365px 160px 0 0 rgba(255, 255, 255, 1), 370px 160px 0 0 rgba(110, 205, 199, 1),
  375px 160px 0 0 rgba(110, 205, 199, 1), 380px 160px 0 0 rgba(110, 205, 199, 1),
  385px 160px 0 0 rgba(255, 255, 255, 1), 390px 160px 0 0 rgba(110, 205, 199, 1),
  395px 160px 0 0 rgba(110, 205, 199, 1), 400px 160px 0 0 rgba(110, 205, 199, 1),
  405px 160px 0 0 rgba(255, 255, 255, 1), 410px 160px 0 0 rgba(110, 205, 199, 1),
  415px 160px 0 0 rgba(110, 205, 199, 1), 420px 160px 0 0 rgba(110, 205, 199, 1),
  425px 160px 0 0 rgba(255, 255, 255, 1), 430px 160px 0 0 rgba(110, 205, 199, 1),
  435px 160px 0 0 rgba(110, 205, 199, 1), 440px 160px 0 0 rgba(110, 205, 199, 1),
  445px 160px 0 0 rgba(255, 255, 255, 1), 450px 160px 0 0 rgba(110, 205, 199, 1),
  455px 160px 0 0 rgba(110, 205, 199, 1), 460px 160px 0 0 rgba(110, 205, 199, 1),
  465px 160px 0 0 rgba(255, 255, 255, 1), 470px 160px 0 0 rgba(110, 205, 199, 1),
  475px 160px 0 0 rgba(110, 205, 199, 1), 480px 160px 0 0 rgba(110, 205, 199, 1),
  485px 160px 0 0 rgba(255, 255, 255, 1), 490px 160px 0 0 rgba(110, 205, 199, 1),
  495px 160px 0 0 rgba(110, 205, 199, 1), 500px 160px 0 0 rgba(110, 205, 199, 1),
  505px 160px 0 0 rgba(255, 255, 255, 1), 510px 160px 0 0 rgba(110, 205, 199, 1),
  515px 160px 0 0 rgba(110, 205, 199, 1), 520px 160px 0 0 rgba(110, 205, 199, 1),
  525px 160px 0 0 rgba(255, 255, 255, 1), 530px 160px 0 0 rgba(110, 205, 199, 1),
  535px 160px 0 0 rgba(110, 205, 199, 1), 540px 160px 0 0 rgba(110, 205, 199, 1),
  545px 160px 0 0 rgba(255, 255, 255, 1), 550px 160px 0 0 rgba(110, 205, 199, 1),
  555px 160px 0 0 rgba(110, 205, 199, 1), 560px 160px 0 0 rgba(110, 205, 199, 1),
  565px 160px 0 0 rgba(255, 255, 255, 1), 570px 160px 0 0 rgba(110, 205, 199, 1),
  575px 160px 0 0 rgba(110, 205, 199, 1), 580px 160px 0 0 rgba(110, 205, 199, 1),
  585px 160px 0 0 rgba(255, 255, 255, 1), 590px 160px 0 0 rgba(110, 205, 199, 1),
  595px 160px 0 0 rgba(110, 205, 199, 1), 600px 160px 0 0 rgba(110, 205, 199, 1),
  605px 160px 0 0 rgba(255, 255, 255, 1), 610px 160px 0 0 rgba(110, 205, 199, 1),
  615px 160px 0 0 rgba(110, 205, 199, 1), 620px 160px 0 0 rgba(110, 205, 199, 1),
  625px 160px 0 0 rgba(255, 255, 255, 1), 630px 160px 0 0 rgba(110, 205, 199, 1),
  635px 160px 0 0 rgba(110, 205, 199, 1), 640px 160px 0 0 rgba(110, 205, 199, 1),
  645px 160px 0 0 rgba(255, 255, 255, 1), 650px 160px 0 0 rgba(110, 205, 199, 1),
  655px 160px 0 0 rgba(110, 205, 199, 1), 660px 160px 0 0 rgba(110, 205, 199, 1),
  665px 160px 0 0 rgba(255, 255, 255, 1), 670px 160px 0 0 rgba(110, 205, 199, 1),
  675px 160px 0 0 rgba(110, 205, 199, 1), 680px 160px 0 0 rgba(110, 205, 199, 1),
  685px 160px 0 0 rgba(203, 109, 181, 1), 690px 160px 0 0 rgba(255, 205, 234, 1),
  695px 160px 0 0 rgba(255, 205, 234, 1), 700px 160px 0 0 rgba(168, 90, 150, 1),
  705px 160px 0 0 rgba(203, 109, 181, 1), 5px 165px 0 0 rgba(203, 109, 181, 1),
  10px 165px 0 0 rgba(252, 231, 243, 1), 15px 165px 0 0 rgba(255, 205, 234, 1),
  20px 165px 0 0 rgba(255, 205, 234, 1), 25px 165px 0 0 rgba(203, 109, 181, 1),
  30px 165px 0 0 rgba(110, 205, 199, 1), 35px 165px 0 0 rgba(255, 255, 255, 1),
  40px 165px 0 0 rgba(110, 205, 199, 1), 45px 165px 0 0 rgba(110, 205, 199, 1),
  50px 165px 0 0 rgba(110, 205, 199, 1), 55px 165px 0 0 rgba(255, 255, 255, 1),
  60px 165px 0 0 rgba(110, 205, 199, 1), 65px 165px 0 0 rgba(110, 205, 199, 1),
  70px 165px 0 0 rgba(110, 205, 199, 1), 75px 165px 0 0 rgba(255, 255, 255, 1),
  80px 165px 0 0 rgba(110, 205, 199, 1), 85px 165px 0 0 rgba(110, 205, 199, 1),
  90px 165px 0 0 rgba(110, 205, 199, 1), 95px 165px 0 0 rgba(255, 255, 255, 1),
  100px 165px 0 0 rgba(110, 205, 199, 1), 105px 165px 0 0 rgba(110, 205, 199, 1),
  110px 165px 0 0 rgba(110, 205, 199, 1), 115px 165px 0 0 rgba(255, 255, 255, 1),
  120px 165px 0 0 rgba(110, 205, 199, 1), 125px 165px 0 0 rgba(110, 205, 199, 1),
  130px 165px 0 0 rgba(110, 205, 199, 1), 135px 165px 0 0 rgba(255, 255, 255, 1),
  140px 165px 0 0 rgba(110, 205, 199, 1), 145px 165px 0 0 rgba(110, 205, 199, 1),
  150px 165px 0 0 rgba(110, 205, 199, 1), 155px 165px 0 0 rgba(255, 255, 255, 1),
  160px 165px 0 0 rgba(110, 205, 199, 1), 165px 165px 0 0 rgba(110, 205, 199, 1),
  170px 165px 0 0 rgba(110, 205, 199, 1), 175px 165px 0 0 rgba(255, 255, 255, 1),
  180px 165px 0 0 rgba(110, 205, 199, 1), 185px 165px 0 0 rgba(110, 205, 199, 1),
  190px 165px 0 0 rgba(110, 205, 199, 1), 195px 165px 0 0 rgba(255, 255, 255, 1),
  200px 165px 0 0 rgba(110, 205, 199, 1), 205px 165px 0 0 rgba(110, 205, 199, 1),
  210px 165px 0 0 rgba(110, 205, 199, 1), 215px 165px 0 0 rgba(255, 255, 255, 1),
  220px 165px 0 0 rgba(110, 205, 199, 1), 225px 165px 0 0 rgba(110, 205, 199, 1),
  230px 165px 0 0 rgba(110, 205, 199, 1), 235px 165px 0 0 rgba(255, 255, 255, 1),
  240px 165px 0 0 rgba(110, 205, 199, 1), 245px 165px 0 0 rgba(110, 205, 199, 1),
  250px 165px 0 0 rgba(110, 205, 199, 1), 255px 165px 0 0 rgba(255, 255, 255, 1),
  260px 165px 0 0 rgba(110, 205, 199, 1), 265px 165px 0 0 rgba(110, 205, 199, 1),
  270px 165px 0 0 rgba(110, 205, 199, 1), 275px 165px 0 0 rgba(255, 255, 255, 1),
  280px 165px 0 0 rgba(110, 205, 199, 1), 285px 165px 0 0 rgba(110, 205, 199, 1),
  290px 165px 0 0 rgba(110, 205, 199, 1), 295px 165px 0 0 rgba(255, 255, 255, 1),
  300px 165px 0 0 rgba(110, 205, 199, 1), 305px 165px 0 0 rgba(110, 205, 199, 1),
  310px 165px 0 0 rgba(110, 205, 199, 1), 315px 165px 0 0 rgba(255, 255, 255, 1),
  320px 165px 0 0 rgba(110, 205, 199, 1), 325px 165px 0 0 rgba(110, 205, 199, 1),
  330px 165px 0 0 rgba(110, 205, 199, 1), 335px 165px 0 0 rgba(255, 255, 255, 1),
  340px 165px 0 0 rgba(110, 205, 199, 1), 345px 165px 0 0 rgba(110, 205, 199, 1),
  350px 165px 0 0 rgba(110, 205, 199, 1), 355px 165px 0 0 rgba(255, 255, 255, 1),
  360px 165px 0 0 rgba(110, 205, 199, 1), 365px 165px 0 0 rgba(110, 205, 199, 1),
  370px 165px 0 0 rgba(110, 205, 199, 1), 375px 165px 0 0 rgba(255, 255, 255, 1),
  380px 165px 0 0 rgba(110, 205, 199, 1), 385px 165px 0 0 rgba(110, 205, 199, 1),
  390px 165px 0 0 rgba(110, 205, 199, 1), 395px 165px 0 0 rgba(255, 255, 255, 1),
  400px 165px 0 0 rgba(110, 205, 199, 1), 405px 165px 0 0 rgba(110, 205, 199, 1),
  410px 165px 0 0 rgba(110, 205, 199, 1), 415px 165px 0 0 rgba(255, 255, 255, 1),
  420px 165px 0 0 rgba(110, 205, 199, 1), 425px 165px 0 0 rgba(110, 205, 199, 1),
  430px 165px 0 0 rgba(110, 205, 199, 1), 435px 165px 0 0 rgba(255, 255, 255, 1),
  440px 165px 0 0 rgba(110, 205, 199, 1), 445px 165px 0 0 rgba(110, 205, 199, 1),
  450px 165px 0 0 rgba(110, 205, 199, 1), 455px 165px 0 0 rgba(255, 255, 255, 1),
  460px 165px 0 0 rgba(110, 205, 199, 1), 465px 165px 0 0 rgba(110, 205, 199, 1),
  470px 165px 0 0 rgba(110, 205, 199, 1), 475px 165px 0 0 rgba(255, 255, 255, 1),
  480px 165px 0 0 rgba(110, 205, 199, 1), 485px 165px 0 0 rgba(110, 205, 199, 1),
  490px 165px 0 0 rgba(110, 205, 199, 1), 495px 165px 0 0 rgba(255, 255, 255, 1),
  500px 165px 0 0 rgba(110, 205, 199, 1), 505px 165px 0 0 rgba(110, 205, 199, 1),
  510px 165px 0 0 rgba(110, 205, 199, 1), 515px 165px 0 0 rgba(255, 255, 255, 1),
  520px 165px 0 0 rgba(110, 205, 199, 1), 525px 165px 0 0 rgba(110, 205, 199, 1),
  530px 165px 0 0 rgba(110, 205, 199, 1), 535px 165px 0 0 rgba(255, 255, 255, 1),
  540px 165px 0 0 rgba(110, 205, 199, 1), 545px 165px 0 0 rgba(110, 205, 199, 1),
  550px 165px 0 0 rgba(110, 205, 199, 1), 555px 165px 0 0 rgba(255, 255, 255, 1),
  560px 165px 0 0 rgba(110, 205, 199, 1), 565px 165px 0 0 rgba(110, 205, 199, 1),
  570px 165px 0 0 rgba(110, 205, 199, 1), 575px 165px 0 0 rgba(255, 255, 255, 1),
  580px 165px 0 0 rgba(110, 205, 199, 1), 585px 165px 0 0 rgba(110, 205, 199, 1),
  590px 165px 0 0 rgba(110, 205, 199, 1), 595px 165px 0 0 rgba(255, 255, 255, 1),
  600px 165px 0 0 rgba(110, 205, 199, 1), 605px 165px 0 0 rgba(110, 205, 199, 1),
  610px 165px 0 0 rgba(110, 205, 199, 1), 615px 165px 0 0 rgba(255, 255, 255, 1),
  620px 165px 0 0 rgba(110, 205, 199, 1), 625px 165px 0 0 rgba(110, 205, 199, 1),
  630px 165px 0 0 rgba(110, 205, 199, 1), 635px 165px 0 0 rgba(255, 255, 255, 1),
  640px 165px 0 0 rgba(110, 205, 199, 1), 645px 165px 0 0 rgba(110, 205, 199, 1),
  650px 165px 0 0 rgba(110, 205, 199, 1), 655px 165px 0 0 rgba(255, 255, 255, 1),
  660px 165px 0 0 rgba(110, 205, 199, 1), 665px 165px 0 0 rgba(110, 205, 199, 1),
  670px 165px 0 0 rgba(110, 205, 199, 1), 675px 165px 0 0 rgba(255, 255, 255, 1),
  680px 165px 0 0 rgba(110, 205, 199, 1), 685px 165px 0 0 rgba(203, 109, 181, 1),
  690px 165px 0 0 rgba(255, 205, 234, 1), 695px 165px 0 0 rgba(255, 205, 234, 1),
  700px 165px 0 0 rgba(168, 90, 150, 1), 705px 165px 0 0 rgba(203, 109, 181, 1),
  5px 170px 0 0 rgba(203, 109, 181, 1), 10px 170px 0 0 rgba(252, 231, 243, 1),
  15px 170px 0 0 rgba(255, 205, 234, 1), 20px 170px 0 0 rgba(255, 205, 234, 1),
  25px 170px 0 0 rgba(203, 109, 181, 1), 30px 170px 0 0 rgba(110, 205, 199, 1),
  35px 170px 0 0 rgba(110, 205, 199, 1), 40px 170px 0 0 rgba(110, 205, 199, 1),
  45px 170px 0 0 rgba(110, 205, 199, 1), 50px 170px 0 0 rgba(110, 205, 199, 1),
  55px 170px 0 0 rgba(110, 205, 199, 1), 60px 170px 0 0 rgba(110, 205, 199, 1),
  65px 170px 0 0 rgba(110, 205, 199, 1), 70px 170px 0 0 rgba(110, 205, 199, 1),
  75px 170px 0 0 rgba(110, 205, 199, 1), 80px 170px 0 0 rgba(110, 205, 199, 1),
  85px 170px 0 0 rgba(110, 205, 199, 1), 90px 170px 0 0 rgba(110, 205, 199, 1),
  95px 170px 0 0 rgba(110, 205, 199, 1), 100px 170px 0 0 rgba(110, 205, 199, 1),
  105px 170px 0 0 rgba(110, 205, 199, 1), 110px 170px 0 0 rgba(110, 205, 199, 1),
  115px 170px 0 0 rgba(110, 205, 199, 1), 120px 170px 0 0 rgba(110, 205, 199, 1),
  125px 170px 0 0 rgba(110, 205, 199, 1), 130px 170px 0 0 rgba(110, 205, 199, 1),
  135px 170px 0 0 rgba(110, 205, 199, 1), 140px 170px 0 0 rgba(110, 205, 199, 1),
  145px 170px 0 0 rgba(110, 205, 199, 1), 150px 170px 0 0 rgba(110, 205, 199, 1),
  155px 170px 0 0 rgba(110, 205, 199, 1), 160px 170px 0 0 rgba(110, 205, 199, 1),
  165px 170px 0 0 rgba(110, 205, 199, 1), 170px 170px 0 0 rgba(110, 205, 199, 1),
  175px 170px 0 0 rgba(110, 205, 199, 1), 180px 170px 0 0 rgba(110, 205, 199, 1),
  185px 170px 0 0 rgba(110, 205, 199, 1), 190px 170px 0 0 rgba(110, 205, 199, 1),
  195px 170px 0 0 rgba(110, 205, 199, 1), 200px 170px 0 0 rgba(110, 205, 199, 1),
  205px 170px 0 0 rgba(110, 205, 199, 1), 210px 170px 0 0 rgba(110, 205, 199, 1),
  215px 170px 0 0 rgba(110, 205, 199, 1), 220px 170px 0 0 rgba(110, 205, 199, 1),
  225px 170px 0 0 rgba(110, 205, 199, 1), 230px 170px 0 0 rgba(110, 205, 199, 1),
  235px 170px 0 0 rgba(110, 205, 199, 1), 240px 170px 0 0 rgba(110, 205, 199, 1),
  245px 170px 0 0 rgba(110, 205, 199, 1), 250px 170px 0 0 rgba(110, 205, 199, 1),
  255px 170px 0 0 rgba(110, 205, 199, 1), 260px 170px 0 0 rgba(110, 205, 199, 1),
  265px 170px 0 0 rgba(110, 205, 199, 1), 270px 170px 0 0 rgba(110, 205, 199, 1),
  275px 170px 0 0 rgba(110, 205, 199, 1), 280px 170px 0 0 rgba(110, 205, 199, 1),
  285px 170px 0 0 rgba(110, 205, 199, 1), 290px 170px 0 0 rgba(110, 205, 199, 1),
  295px 170px 0 0 rgba(110, 205, 199, 1), 300px 170px 0 0 rgba(110, 205, 199, 1),
  305px 170px 0 0 rgba(110, 205, 199, 1), 310px 170px 0 0 rgba(110, 205, 199, 1),
  315px 170px 0 0 rgba(110, 205, 199, 1), 320px 170px 0 0 rgba(110, 205, 199, 1),
  325px 170px 0 0 rgba(110, 205, 199, 1), 330px 170px 0 0 rgba(110, 205, 199, 1),
  335px 170px 0 0 rgba(110, 205, 199, 1), 340px 170px 0 0 rgba(110, 205, 199, 1),
  345px 170px 0 0 rgba(110, 205, 199, 1), 350px 170px 0 0 rgba(110, 205, 199, 1),
  355px 170px 0 0 rgba(110, 205, 199, 1), 360px 170px 0 0 rgba(110, 205, 199, 1),
  365px 170px 0 0 rgba(110, 205, 199, 1), 370px 170px 0 0 rgba(110, 205, 199, 1),
  375px 170px 0 0 rgba(110, 205, 199, 1), 380px 170px 0 0 rgba(110, 205, 199, 1),
  385px 170px 0 0 rgba(110, 205, 199, 1), 390px 170px 0 0 rgba(110, 205, 199, 1),
  395px 170px 0 0 rgba(110, 205, 199, 1), 400px 170px 0 0 rgba(110, 205, 199, 1),
  405px 170px 0 0 rgba(110, 205, 199, 1), 410px 170px 0 0 rgba(110, 205, 199, 1),
  415px 170px 0 0 rgba(110, 205, 199, 1), 420px 170px 0 0 rgba(110, 205, 199, 1),
  425px 170px 0 0 rgba(110, 205, 199, 1), 430px 170px 0 0 rgba(110, 205, 199, 1),
  435px 170px 0 0 rgba(110, 205, 199, 1), 440px 170px 0 0 rgba(110, 205, 199, 1),
  445px 170px 0 0 rgba(110, 205, 199, 1), 450px 170px 0 0 rgba(110, 205, 199, 1),
  455px 170px 0 0 rgba(110, 205, 199, 1), 460px 170px 0 0 rgba(110, 205, 199, 1),
  465px 170px 0 0 rgba(110, 205, 199, 1), 470px 170px 0 0 rgba(110, 205, 199, 1),
  475px 170px 0 0 rgba(110, 205, 199, 1), 480px 170px 0 0 rgba(110, 205, 199, 1),
  485px 170px 0 0 rgba(110, 205, 199, 1), 490px 170px 0 0 rgba(110, 205, 199, 1),
  495px 170px 0 0 rgba(110, 205, 199, 1), 500px 170px 0 0 rgba(110, 205, 199, 1),
  505px 170px 0 0 rgba(110, 205, 199, 1), 510px 170px 0 0 rgba(110, 205, 199, 1),
  515px 170px 0 0 rgba(110, 205, 199, 1), 520px 170px 0 0 rgba(110, 205, 199, 1),
  525px 170px 0 0 rgba(110, 205, 199, 1), 530px 170px 0 0 rgba(110, 205, 199, 1),
  535px 170px 0 0 rgba(110, 205, 199, 1), 540px 170px 0 0 rgba(110, 205, 199, 1),
  545px 170px 0 0 rgba(110, 205, 199, 1), 550px 170px 0 0 rgba(110, 205, 199, 1),
  555px 170px 0 0 rgba(110, 205, 199, 1), 560px 170px 0 0 rgba(110, 205, 199, 1),
  565px 170px 0 0 rgba(110, 205, 199, 1), 570px 170px 0 0 rgba(110, 205, 199, 1),
  575px 170px 0 0 rgba(110, 205, 199, 1), 580px 170px 0 0 rgba(110, 205, 199, 1),
  585px 170px 0 0 rgba(110, 205, 199, 1), 590px 170px 0 0 rgba(110, 205, 199, 1),
  595px 170px 0 0 rgba(110, 205, 199, 1), 600px 170px 0 0 rgba(110, 205, 199, 1),
  605px 170px 0 0 rgba(110, 205, 199, 1), 610px 170px 0 0 rgba(110, 205, 199, 1),
  615px 170px 0 0 rgba(110, 205, 199, 1), 620px 170px 0 0 rgba(110, 205, 199, 1),
  625px 170px 0 0 rgba(110, 205, 199, 1), 630px 170px 0 0 rgba(110, 205, 199, 1),
  635px 170px 0 0 rgba(110, 205, 199, 1), 640px 170px 0 0 rgba(110, 205, 199, 1),
  645px 170px 0 0 rgba(110, 205, 199, 1), 650px 170px 0 0 rgba(110, 205, 199, 1),
  655px 170px 0 0 rgba(110, 205, 199, 1), 660px 170px 0 0 rgba(110, 205, 199, 1),
  665px 170px 0 0 rgba(110, 205, 199, 1), 670px 170px 0 0 rgba(110, 205, 199, 1),
  675px 170px 0 0 rgba(110, 205, 199, 1), 680px 170px 0 0 rgba(110, 205, 199, 1),
  685px 170px 0 0 rgba(203, 109, 181, 1), 690px 170px 0 0 rgba(255, 205, 234, 1),
  695px 170px 0 0 rgba(255, 205, 234, 1), 700px 170px 0 0 rgba(168, 90, 150, 1),
  705px 170px 0 0 rgba(203, 109, 181, 1), 5px 175px 0 0 rgba(203, 109, 181, 1),
  10px 175px 0 0 rgba(252, 231, 243, 1), 15px 175px 0 0 rgba(255, 205, 234, 1),
  20px 175px 0 0 rgba(255, 205, 234, 1), 25px 175px 0 0 rgba(203, 109, 181, 1),
  30px 175px 0 0 rgba(110, 205, 199, 1), 35px 175px 0 0 rgba(255, 255, 255, 1),
  40px 175px 0 0 rgba(110, 205, 199, 1), 45px 175px 0 0 rgba(255, 255, 255, 1),
  50px 175px 0 0 rgba(110, 205, 199, 1), 55px 175px 0 0 rgba(255, 255, 255, 1),
  60px 175px 0 0 rgba(110, 205, 199, 1), 65px 175px 0 0 rgba(255, 255, 255, 1),
  70px 175px 0 0 rgba(110, 205, 199, 1), 75px 175px 0 0 rgba(255, 255, 255, 1),
  80px 175px 0 0 rgba(110, 205, 199, 1), 85px 175px 0 0 rgba(255, 255, 255, 1),
  90px 175px 0 0 rgba(110, 205, 199, 1), 95px 175px 0 0 rgba(255, 255, 255, 1),
  100px 175px 0 0 rgba(110, 205, 199, 1), 105px 175px 0 0 rgba(255, 255, 255, 1),
  110px 175px 0 0 rgba(110, 205, 199, 1), 115px 175px 0 0 rgba(255, 255, 255, 1),
  120px 175px 0 0 rgba(110, 205, 199, 1), 125px 175px 0 0 rgba(255, 255, 255, 1),
  130px 175px 0 0 rgba(110, 205, 199, 1), 135px 175px 0 0 rgba(255, 255, 255, 1),
  140px 175px 0 0 rgba(110, 205, 199, 1), 145px 175px 0 0 rgba(255, 255, 255, 1),
  150px 175px 0 0 rgba(110, 205, 199, 1), 155px 175px 0 0 rgba(255, 255, 255, 1),
  160px 175px 0 0 rgba(110, 205, 199, 1), 165px 175px 0 0 rgba(255, 255, 255, 1),
  170px 175px 0 0 rgba(110, 205, 199, 1), 175px 175px 0 0 rgba(255, 255, 255, 1),
  180px 175px 0 0 rgba(110, 205, 199, 1), 185px 175px 0 0 rgba(255, 255, 255, 1),
  190px 175px 0 0 rgba(110, 205, 199, 1), 195px 175px 0 0 rgba(255, 255, 255, 1),
  200px 175px 0 0 rgba(110, 205, 199, 1), 205px 175px 0 0 rgba(255, 255, 255, 1),
  210px 175px 0 0 rgba(110, 205, 199, 1), 215px 175px 0 0 rgba(255, 255, 255, 1),
  220px 175px 0 0 rgba(110, 205, 199, 1), 225px 175px 0 0 rgba(255, 255, 255, 1),
  230px 175px 0 0 rgba(110, 205, 199, 1), 235px 175px 0 0 rgba(255, 255, 255, 1),
  240px 175px 0 0 rgba(110, 205, 199, 1), 245px 175px 0 0 rgba(255, 255, 255, 1),
  250px 175px 0 0 rgba(110, 205, 199, 1), 255px 175px 0 0 rgba(255, 255, 255, 1),
  260px 175px 0 0 rgba(110, 205, 199, 1), 265px 175px 0 0 rgba(255, 255, 255, 1),
  270px 175px 0 0 rgba(110, 205, 199, 1), 275px 175px 0 0 rgba(255, 255, 255, 1),
  280px 175px 0 0 rgba(110, 205, 199, 1), 285px 175px 0 0 rgba(255, 255, 255, 1),
  290px 175px 0 0 rgba(110, 205, 199, 1), 295px 175px 0 0 rgba(255, 255, 255, 1),
  300px 175px 0 0 rgba(110, 205, 199, 1), 305px 175px 0 0 rgba(255, 255, 255, 1),
  310px 175px 0 0 rgba(110, 205, 199, 1), 315px 175px 0 0 rgba(255, 255, 255, 1),
  320px 175px 0 0 rgba(110, 205, 199, 1), 325px 175px 0 0 rgba(255, 255, 255, 1),
  330px 175px 0 0 rgba(110, 205, 199, 1), 335px 175px 0 0 rgba(255, 255, 255, 1),
  340px 175px 0 0 rgba(110, 205, 199, 1), 345px 175px 0 0 rgba(255, 255, 255, 1),
  350px 175px 0 0 rgba(110, 205, 199, 1), 355px 175px 0 0 rgba(255, 255, 255, 1),
  360px 175px 0 0 rgba(110, 205, 199, 1), 365px 175px 0 0 rgba(255, 255, 255, 1),
  370px 175px 0 0 rgba(110, 205, 199, 1), 375px 175px 0 0 rgba(255, 255, 255, 1),
  380px 175px 0 0 rgba(110, 205, 199, 1), 385px 175px 0 0 rgba(255, 255, 255, 1),
  390px 175px 0 0 rgba(110, 205, 199, 1), 395px 175px 0 0 rgba(255, 255, 255, 1),
  400px 175px 0 0 rgba(110, 205, 199, 1), 405px 175px 0 0 rgba(255, 255, 255, 1),
  410px 175px 0 0 rgba(110, 205, 199, 1), 415px 175px 0 0 rgba(255, 255, 255, 1),
  420px 175px 0 0 rgba(110, 205, 199, 1), 425px 175px 0 0 rgba(255, 255, 255, 1),
  430px 175px 0 0 rgba(110, 205, 199, 1), 435px 175px 0 0 rgba(255, 255, 255, 1),
  440px 175px 0 0 rgba(110, 205, 199, 1), 445px 175px 0 0 rgba(255, 255, 255, 1),
  450px 175px 0 0 rgba(110, 205, 199, 1), 455px 175px 0 0 rgba(255, 255, 255, 1),
  460px 175px 0 0 rgba(110, 205, 199, 1), 465px 175px 0 0 rgba(255, 255, 255, 1),
  470px 175px 0 0 rgba(110, 205, 199, 1), 475px 175px 0 0 rgba(255, 255, 255, 1),
  480px 175px 0 0 rgba(110, 205, 199, 1), 485px 175px 0 0 rgba(255, 255, 255, 1),
  490px 175px 0 0 rgba(110, 205, 199, 1), 495px 175px 0 0 rgba(255, 255, 255, 1),
  500px 175px 0 0 rgba(110, 205, 199, 1), 505px 175px 0 0 rgba(255, 255, 255, 1),
  510px 175px 0 0 rgba(110, 205, 199, 1), 515px 175px 0 0 rgba(255, 255, 255, 1),
  520px 175px 0 0 rgba(110, 205, 199, 1), 525px 175px 0 0 rgba(255, 255, 255, 1),
  530px 175px 0 0 rgba(110, 205, 199, 1), 535px 175px 0 0 rgba(255, 255, 255, 1),
  540px 175px 0 0 rgba(110, 205, 199, 1), 545px 175px 0 0 rgba(255, 255, 255, 1),
  550px 175px 0 0 rgba(110, 205, 199, 1), 555px 175px 0 0 rgba(255, 255, 255, 1),
  560px 175px 0 0 rgba(110, 205, 199, 1), 565px 175px 0 0 rgba(255, 255, 255, 1),
  570px 175px 0 0 rgba(110, 205, 199, 1), 575px 175px 0 0 rgba(255, 255, 255, 1),
  580px 175px 0 0 rgba(110, 205, 199, 1), 585px 175px 0 0 rgba(255, 255, 255, 1),
  590px 175px 0 0 rgba(110, 205, 199, 1), 595px 175px 0 0 rgba(255, 255, 255, 1),
  600px 175px 0 0 rgba(110, 205, 199, 1), 605px 175px 0 0 rgba(255, 255, 255, 1),
  610px 175px 0 0 rgba(110, 205, 199, 1), 615px 175px 0 0 rgba(255, 255, 255, 1),
  620px 175px 0 0 rgba(110, 205, 199, 1), 625px 175px 0 0 rgba(255, 255, 255, 1),
  630px 175px 0 0 rgba(110, 205, 199, 1), 635px 175px 0 0 rgba(255, 255, 255, 1),
  640px 175px 0 0 rgba(110, 205, 199, 1), 645px 175px 0 0 rgba(255, 255, 255, 1),
  650px 175px 0 0 rgba(110, 205, 199, 1), 655px 175px 0 0 rgba(255, 255, 255, 1),
  660px 175px 0 0 rgba(110, 205, 199, 1), 665px 175px 0 0 rgba(255, 255, 255, 1),
  670px 175px 0 0 rgba(110, 205, 199, 1), 675px 175px 0 0 rgba(255, 255, 255, 1),
  680px 175px 0 0 rgba(110, 205, 199, 1), 685px 175px 0 0 rgba(203, 109, 181, 1),
  690px 175px 0 0 rgba(255, 205, 234, 1), 695px 175px 0 0 rgba(255, 205, 234, 1),
  700px 175px 0 0 rgba(168, 90, 150, 1), 705px 175px 0 0 rgba(203, 109, 181, 1),
  5px 180px 0 0 rgba(203, 109, 181, 1), 10px 180px 0 0 rgba(252, 231, 243, 1),
  15px 180px 0 0 rgba(255, 205, 234, 1), 20px 180px 0 0 rgba(255, 205, 234, 1),
  25px 180px 0 0 rgba(203, 109, 181, 1), 30px 180px 0 0 rgba(255, 255, 255, 1),
  35px 180px 0 0 rgba(110, 205, 199, 1), 40px 180px 0 0 rgba(110, 205, 199, 1),
  45px 180px 0 0 rgba(110, 205, 199, 1), 50px 180px 0 0 rgba(255, 255, 255, 1),
  55px 180px 0 0 rgba(110, 205, 199, 1), 60px 180px 0 0 rgba(110, 205, 199, 1),
  65px 180px 0 0 rgba(110, 205, 199, 1), 70px 180px 0 0 rgba(255, 255, 255, 1),
  75px 180px 0 0 rgba(110, 205, 199, 1), 80px 180px 0 0 rgba(110, 205, 199, 1),
  85px 180px 0 0 rgba(110, 205, 199, 1), 90px 180px 0 0 rgba(255, 255, 255, 1),
  95px 180px 0 0 rgba(110, 205, 199, 1), 100px 180px 0 0 rgba(110, 205, 199, 1),
  105px 180px 0 0 rgba(110, 205, 199, 1), 110px 180px 0 0 rgba(255, 255, 255, 1),
  115px 180px 0 0 rgba(110, 205, 199, 1), 120px 180px 0 0 rgba(110, 205, 199, 1),
  125px 180px 0 0 rgba(110, 205, 199, 1), 130px 180px 0 0 rgba(255, 255, 255, 1),
  135px 180px 0 0 rgba(110, 205, 199, 1), 140px 180px 0 0 rgba(110, 205, 199, 1),
  145px 180px 0 0 rgba(110, 205, 199, 1), 150px 180px 0 0 rgba(255, 255, 255, 1),
  155px 180px 0 0 rgba(110, 205, 199, 1), 160px 180px 0 0 rgba(110, 205, 199, 1),
  165px 180px 0 0 rgba(110, 205, 199, 1), 170px 180px 0 0 rgba(255, 255, 255, 1),
  175px 180px 0 0 rgba(110, 205, 199, 1), 180px 180px 0 0 rgba(110, 205, 199, 1),
  185px 180px 0 0 rgba(110, 205, 199, 1), 190px 180px 0 0 rgba(255, 255, 255, 1),
  195px 180px 0 0 rgba(110, 205, 199, 1), 200px 180px 0 0 rgba(110, 205, 199, 1),
  205px 180px 0 0 rgba(110, 205, 199, 1), 210px 180px 0 0 rgba(255, 255, 255, 1),
  215px 180px 0 0 rgba(110, 205, 199, 1), 220px 180px 0 0 rgba(110, 205, 199, 1),
  225px 180px 0 0 rgba(110, 205, 199, 1), 230px 180px 0 0 rgba(255, 255, 255, 1),
  235px 180px 0 0 rgba(110, 205, 199, 1), 240px 180px 0 0 rgba(110, 205, 199, 1),
  245px 180px 0 0 rgba(110, 205, 199, 1), 250px 180px 0 0 rgba(255, 255, 255, 1),
  255px 180px 0 0 rgba(110, 205, 199, 1), 260px 180px 0 0 rgba(110, 205, 199, 1),
  265px 180px 0 0 rgba(110, 205, 199, 1), 270px 180px 0 0 rgba(255, 255, 255, 1),
  275px 180px 0 0 rgba(110, 205, 199, 1), 280px 180px 0 0 rgba(110, 205, 199, 1),
  285px 180px 0 0 rgba(110, 205, 199, 1), 290px 180px 0 0 rgba(255, 255, 255, 1),
  295px 180px 0 0 rgba(110, 205, 199, 1), 300px 180px 0 0 rgba(110, 205, 199, 1),
  305px 180px 0 0 rgba(110, 205, 199, 1), 310px 180px 0 0 rgba(255, 255, 255, 1),
  315px 180px 0 0 rgba(110, 205, 199, 1), 320px 180px 0 0 rgba(110, 205, 199, 1),
  325px 180px 0 0 rgba(110, 205, 199, 1), 330px 180px 0 0 rgba(255, 255, 255, 1),
  335px 180px 0 0 rgba(110, 205, 199, 1), 340px 180px 0 0 rgba(110, 205, 199, 1),
  345px 180px 0 0 rgba(110, 205, 199, 1), 350px 180px 0 0 rgba(255, 255, 255, 1),
  355px 180px 0 0 rgba(110, 205, 199, 1), 360px 180px 0 0 rgba(110, 205, 199, 1),
  365px 180px 0 0 rgba(110, 205, 199, 1), 370px 180px 0 0 rgba(255, 255, 255, 1),
  375px 180px 0 0 rgba(110, 205, 199, 1), 380px 180px 0 0 rgba(110, 205, 199, 1),
  385px 180px 0 0 rgba(110, 205, 199, 1), 390px 180px 0 0 rgba(255, 255, 255, 1),
  395px 180px 0 0 rgba(110, 205, 199, 1), 400px 180px 0 0 rgba(110, 205, 199, 1),
  405px 180px 0 0 rgba(110, 205, 199, 1), 410px 180px 0 0 rgba(255, 255, 255, 1),
  415px 180px 0 0 rgba(110, 205, 199, 1), 420px 180px 0 0 rgba(110, 205, 199, 1),
  425px 180px 0 0 rgba(110, 205, 199, 1), 430px 180px 0 0 rgba(255, 255, 255, 1),
  435px 180px 0 0 rgba(110, 205, 199, 1), 440px 180px 0 0 rgba(110, 205, 199, 1),
  445px 180px 0 0 rgba(110, 205, 199, 1), 450px 180px 0 0 rgba(255, 255, 255, 1),
  455px 180px 0 0 rgba(110, 205, 199, 1), 460px 180px 0 0 rgba(110, 205, 199, 1),
  465px 180px 0 0 rgba(110, 205, 199, 1), 470px 180px 0 0 rgba(255, 255, 255, 1),
  475px 180px 0 0 rgba(110, 205, 199, 1), 480px 180px 0 0 rgba(110, 205, 199, 1),
  485px 180px 0 0 rgba(110, 205, 199, 1), 490px 180px 0 0 rgba(255, 255, 255, 1),
  495px 180px 0 0 rgba(110, 205, 199, 1), 500px 180px 0 0 rgba(110, 205, 199, 1),
  505px 180px 0 0 rgba(110, 205, 199, 1), 510px 180px 0 0 rgba(255, 255, 255, 1),
  515px 180px 0 0 rgba(110, 205, 199, 1), 520px 180px 0 0 rgba(110, 205, 199, 1),
  525px 180px 0 0 rgba(110, 205, 199, 1), 530px 180px 0 0 rgba(255, 255, 255, 1),
  535px 180px 0 0 rgba(110, 205, 199, 1), 540px 180px 0 0 rgba(110, 205, 199, 1),
  545px 180px 0 0 rgba(110, 205, 199, 1), 550px 180px 0 0 rgba(255, 255, 255, 1),
  555px 180px 0 0 rgba(110, 205, 199, 1), 560px 180px 0 0 rgba(110, 205, 199, 1),
  565px 180px 0 0 rgba(110, 205, 199, 1), 570px 180px 0 0 rgba(255, 255, 255, 1),
  575px 180px 0 0 rgba(110, 205, 199, 1), 580px 180px 0 0 rgba(110, 205, 199, 1),
  585px 180px 0 0 rgba(110, 205, 199, 1), 590px 180px 0 0 rgba(255, 255, 255, 1),
  595px 180px 0 0 rgba(110, 205, 199, 1), 600px 180px 0 0 rgba(110, 205, 199, 1),
  605px 180px 0 0 rgba(110, 205, 199, 1), 610px 180px 0 0 rgba(255, 255, 255, 1),
  615px 180px 0 0 rgba(110, 205, 199, 1), 620px 180px 0 0 rgba(110, 205, 199, 1),
  625px 180px 0 0 rgba(110, 205, 199, 1), 630px 180px 0 0 rgba(255, 255, 255, 1),
  635px 180px 0 0 rgba(110, 205, 199, 1), 640px 180px 0 0 rgba(110, 205, 199, 1),
  645px 180px 0 0 rgba(110, 205, 199, 1), 650px 180px 0 0 rgba(255, 255, 255, 1),
  655px 180px 0 0 rgba(110, 205, 199, 1), 660px 180px 0 0 rgba(110, 205, 199, 1),
  665px 180px 0 0 rgba(110, 205, 199, 1), 670px 180px 0 0 rgba(255, 255, 255, 1),
  675px 180px 0 0 rgba(110, 205, 199, 1), 680px 180px 0 0 rgba(110, 205, 199, 1),
  685px 180px 0 0 rgba(203, 109, 181, 1), 690px 180px 0 0 rgba(255, 205, 234, 1),
  695px 180px 0 0 rgba(255, 205, 234, 1), 700px 180px 0 0 rgba(168, 90, 150, 1),
  705px 180px 0 0 rgba(203, 109, 181, 1), 5px 185px 0 0 rgba(203, 109, 181, 1),
  10px 185px 0 0 rgba(252, 231, 243, 1), 15px 185px 0 0 rgba(255, 205, 234, 1),
  20px 185px 0 0 rgba(255, 205, 234, 1), 25px 185px 0 0 rgba(203, 109, 181, 1),
  30px 185px 0 0 rgba(110, 205, 199, 1), 35px 185px 0 0 rgba(255, 255, 255, 1),
  40px 185px 0 0 rgba(110, 205, 199, 1), 45px 185px 0 0 rgba(255, 255, 255, 1),
  50px 185px 0 0 rgba(110, 205, 199, 1), 55px 185px 0 0 rgba(255, 255, 255, 1),
  60px 185px 0 0 rgba(110, 205, 199, 1), 65px 185px 0 0 rgba(255, 255, 255, 1),
  70px 185px 0 0 rgba(110, 205, 199, 1), 75px 185px 0 0 rgba(255, 255, 255, 1),
  80px 185px 0 0 rgba(110, 205, 199, 1), 85px 185px 0 0 rgba(255, 255, 255, 1),
  90px 185px 0 0 rgba(110, 205, 199, 1), 95px 185px 0 0 rgba(255, 255, 255, 1),
  100px 185px 0 0 rgba(110, 205, 199, 1), 105px 185px 0 0 rgba(255, 255, 255, 1),
  110px 185px 0 0 rgba(110, 205, 199, 1), 115px 185px 0 0 rgba(255, 255, 255, 1),
  120px 185px 0 0 rgba(110, 205, 199, 1), 125px 185px 0 0 rgba(255, 255, 255, 1),
  130px 185px 0 0 rgba(110, 205, 199, 1), 135px 185px 0 0 rgba(255, 255, 255, 1),
  140px 185px 0 0 rgba(110, 205, 199, 1), 145px 185px 0 0 rgba(255, 255, 255, 1),
  150px 185px 0 0 rgba(110, 205, 199, 1), 155px 185px 0 0 rgba(255, 255, 255, 1),
  160px 185px 0 0 rgba(110, 205, 199, 1), 165px 185px 0 0 rgba(255, 255, 255, 1),
  170px 185px 0 0 rgba(110, 205, 199, 1), 175px 185px 0 0 rgba(255, 255, 255, 1),
  180px 185px 0 0 rgba(110, 205, 199, 1), 185px 185px 0 0 rgba(255, 255, 255, 1),
  190px 185px 0 0 rgba(110, 205, 199, 1), 195px 185px 0 0 rgba(255, 255, 255, 1),
  200px 185px 0 0 rgba(110, 205, 199, 1), 205px 185px 0 0 rgba(255, 255, 255, 1),
  210px 185px 0 0 rgba(110, 205, 199, 1), 215px 185px 0 0 rgba(255, 255, 255, 1),
  220px 185px 0 0 rgba(110, 205, 199, 1), 225px 185px 0 0 rgba(255, 255, 255, 1),
  230px 185px 0 0 rgba(110, 205, 199, 1), 235px 185px 0 0 rgba(255, 255, 255, 1),
  240px 185px 0 0 rgba(110, 205, 199, 1), 245px 185px 0 0 rgba(255, 255, 255, 1),
  250px 185px 0 0 rgba(110, 205, 199, 1), 255px 185px 0 0 rgba(255, 255, 255, 1),
  260px 185px 0 0 rgba(110, 205, 199, 1), 265px 185px 0 0 rgba(255, 255, 255, 1),
  270px 185px 0 0 rgba(110, 205, 199, 1), 275px 185px 0 0 rgba(255, 255, 255, 1),
  280px 185px 0 0 rgba(110, 205, 199, 1), 285px 185px 0 0 rgba(255, 255, 255, 1),
  290px 185px 0 0 rgba(110, 205, 199, 1), 295px 185px 0 0 rgba(255, 255, 255, 1),
  300px 185px 0 0 rgba(110, 205, 199, 1), 305px 185px 0 0 rgba(255, 255, 255, 1),
  310px 185px 0 0 rgba(110, 205, 199, 1), 315px 185px 0 0 rgba(255, 255, 255, 1),
  320px 185px 0 0 rgba(110, 205, 199, 1), 325px 185px 0 0 rgba(255, 255, 255, 1),
  330px 185px 0 0 rgba(110, 205, 199, 1), 335px 185px 0 0 rgba(255, 255, 255, 1),
  340px 185px 0 0 rgba(110, 205, 199, 1), 345px 185px 0 0 rgba(255, 255, 255, 1),
  350px 185px 0 0 rgba(110, 205, 199, 1), 355px 185px 0 0 rgba(255, 255, 255, 1),
  360px 185px 0 0 rgba(110, 205, 199, 1), 365px 185px 0 0 rgba(255, 255, 255, 1),
  370px 185px 0 0 rgba(110, 205, 199, 1), 375px 185px 0 0 rgba(255, 255, 255, 1),
  380px 185px 0 0 rgba(110, 205, 199, 1), 385px 185px 0 0 rgba(255, 255, 255, 1),
  390px 185px 0 0 rgba(110, 205, 199, 1), 395px 185px 0 0 rgba(255, 255, 255, 1),
  400px 185px 0 0 rgba(110, 205, 199, 1), 405px 185px 0 0 rgba(255, 255, 255, 1),
  410px 185px 0 0 rgba(110, 205, 199, 1), 415px 185px 0 0 rgba(255, 255, 255, 1),
  420px 185px 0 0 rgba(110, 205, 199, 1), 425px 185px 0 0 rgba(255, 255, 255, 1),
  430px 185px 0 0 rgba(110, 205, 199, 1), 435px 185px 0 0 rgba(255, 255, 255, 1),
  440px 185px 0 0 rgba(110, 205, 199, 1), 445px 185px 0 0 rgba(255, 255, 255, 1),
  450px 185px 0 0 rgba(110, 205, 199, 1), 455px 185px 0 0 rgba(255, 255, 255, 1),
  460px 185px 0 0 rgba(110, 205, 199, 1), 465px 185px 0 0 rgba(255, 255, 255, 1),
  470px 185px 0 0 rgba(110, 205, 199, 1), 475px 185px 0 0 rgba(255, 255, 255, 1),
  480px 185px 0 0 rgba(110, 205, 199, 1), 485px 185px 0 0 rgba(255, 255, 255, 1),
  490px 185px 0 0 rgba(110, 205, 199, 1), 495px 185px 0 0 rgba(255, 255, 255, 1),
  500px 185px 0 0 rgba(110, 205, 199, 1), 505px 185px 0 0 rgba(255, 255, 255, 1),
  510px 185px 0 0 rgba(110, 205, 199, 1), 515px 185px 0 0 rgba(255, 255, 255, 1),
  520px 185px 0 0 rgba(110, 205, 199, 1), 525px 185px 0 0 rgba(255, 255, 255, 1),
  530px 185px 0 0 rgba(110, 205, 199, 1), 535px 185px 0 0 rgba(255, 255, 255, 1),
  540px 185px 0 0 rgba(110, 205, 199, 1), 545px 185px 0 0 rgba(255, 255, 255, 1),
  550px 185px 0 0 rgba(110, 205, 199, 1), 555px 185px 0 0 rgba(255, 255, 255, 1),
  560px 185px 0 0 rgba(110, 205, 199, 1), 565px 185px 0 0 rgba(255, 255, 255, 1),
  570px 185px 0 0 rgba(110, 205, 199, 1), 575px 185px 0 0 rgba(255, 255, 255, 1),
  580px 185px 0 0 rgba(110, 205, 199, 1), 585px 185px 0 0 rgba(255, 255, 255, 1),
  590px 185px 0 0 rgba(110, 205, 199, 1), 595px 185px 0 0 rgba(255, 255, 255, 1),
  600px 185px 0 0 rgba(110, 205, 199, 1), 605px 185px 0 0 rgba(255, 255, 255, 1),
  610px 185px 0 0 rgba(110, 205, 199, 1), 615px 185px 0 0 rgba(255, 255, 255, 1),
  620px 185px 0 0 rgba(110, 205, 199, 1), 625px 185px 0 0 rgba(255, 255, 255, 1),
  630px 185px 0 0 rgba(110, 205, 199, 1), 635px 185px 0 0 rgba(255, 255, 255, 1),
  640px 185px 0 0 rgba(110, 205, 199, 1), 645px 185px 0 0 rgba(255, 255, 255, 1),
  650px 185px 0 0 rgba(110, 205, 199, 1), 655px 185px 0 0 rgba(255, 255, 255, 1),
  660px 185px 0 0 rgba(110, 205, 199, 1), 665px 185px 0 0 rgba(255, 255, 255, 1),
  670px 185px 0 0 rgba(110, 205, 199, 1), 675px 185px 0 0 rgba(255, 255, 255, 1),
  680px 185px 0 0 rgba(110, 205, 199, 1), 685px 185px 0 0 rgba(203, 109, 181, 1),
  690px 185px 0 0 rgba(255, 205, 234, 1), 695px 185px 0 0 rgba(255, 205, 234, 1),
  700px 185px 0 0 rgba(168, 90, 150, 1), 705px 185px 0 0 rgba(203, 109, 181, 1),
  5px 190px 0 0 rgba(203, 109, 181, 1), 10px 190px 0 0 rgba(252, 231, 243, 1),
  15px 190px 0 0 rgba(255, 205, 234, 1), 20px 190px 0 0 rgba(255, 205, 234, 1),
  25px 190px 0 0 rgba(203, 109, 181, 1), 30px 190px 0 0 rgba(110, 205, 199, 1),
  35px 190px 0 0 rgba(110, 205, 199, 1), 40px 190px 0 0 rgba(255, 255, 255, 1),
  45px 190px 0 0 rgba(110, 205, 199, 1), 50px 190px 0 0 rgba(110, 205, 199, 1),
  55px 190px 0 0 rgba(110, 205, 199, 1), 60px 190px 0 0 rgba(255, 255, 255, 1),
  65px 190px 0 0 rgba(110, 205, 199, 1), 70px 190px 0 0 rgba(110, 205, 199, 1),
  75px 190px 0 0 rgba(110, 205, 199, 1), 80px 190px 0 0 rgba(255, 255, 255, 1),
  85px 190px 0 0 rgba(110, 205, 199, 1), 90px 190px 0 0 rgba(110, 205, 199, 1),
  95px 190px 0 0 rgba(110, 205, 199, 1), 100px 190px 0 0 rgba(255, 255, 255, 1),
  105px 190px 0 0 rgba(110, 205, 199, 1), 110px 190px 0 0 rgba(110, 205, 199, 1),
  115px 190px 0 0 rgba(110, 205, 199, 1), 120px 190px 0 0 rgba(255, 255, 255, 1),
  125px 190px 0 0 rgba(110, 205, 199, 1), 130px 190px 0 0 rgba(110, 205, 199, 1),
  135px 190px 0 0 rgba(110, 205, 199, 1), 140px 190px 0 0 rgba(255, 255, 255, 1),
  145px 190px 0 0 rgba(110, 205, 199, 1), 150px 190px 0 0 rgba(110, 205, 199, 1),
  155px 190px 0 0 rgba(110, 205, 199, 1), 160px 190px 0 0 rgba(255, 255, 255, 1),
  165px 190px 0 0 rgba(110, 205, 199, 1), 170px 190px 0 0 rgba(110, 205, 199, 1),
  175px 190px 0 0 rgba(110, 205, 199, 1), 180px 190px 0 0 rgba(255, 255, 255, 1),
  185px 190px 0 0 rgba(110, 205, 199, 1), 190px 190px 0 0 rgba(110, 205, 199, 1),
  195px 190px 0 0 rgba(110, 205, 199, 1), 200px 190px 0 0 rgba(255, 255, 255, 1),
  205px 190px 0 0 rgba(110, 205, 199, 1), 210px 190px 0 0 rgba(110, 205, 199, 1),
  215px 190px 0 0 rgba(110, 205, 199, 1), 220px 190px 0 0 rgba(255, 255, 255, 1),
  225px 190px 0 0 rgba(110, 205, 199, 1), 230px 190px 0 0 rgba(110, 205, 199, 1),
  235px 190px 0 0 rgba(110, 205, 199, 1), 240px 190px 0 0 rgba(255, 255, 255, 1),
  245px 190px 0 0 rgba(110, 205, 199, 1), 250px 190px 0 0 rgba(110, 205, 199, 1),
  255px 190px 0 0 rgba(110, 205, 199, 1), 260px 190px 0 0 rgba(255, 255, 255, 1),
  265px 190px 0 0 rgba(110, 205, 199, 1), 270px 190px 0 0 rgba(110, 205, 199, 1),
  275px 190px 0 0 rgba(110, 205, 199, 1), 280px 190px 0 0 rgba(255, 255, 255, 1),
  285px 190px 0 0 rgba(110, 205, 199, 1), 290px 190px 0 0 rgba(110, 205, 199, 1),
  295px 190px 0 0 rgba(110, 205, 199, 1), 300px 190px 0 0 rgba(255, 255, 255, 1),
  305px 190px 0 0 rgba(110, 205, 199, 1), 310px 190px 0 0 rgba(110, 205, 199, 1),
  315px 190px 0 0 rgba(110, 205, 199, 1), 320px 190px 0 0 rgba(255, 255, 255, 1),
  325px 190px 0 0 rgba(110, 205, 199, 1), 330px 190px 0 0 rgba(110, 205, 199, 1),
  335px 190px 0 0 rgba(110, 205, 199, 1), 340px 190px 0 0 rgba(255, 255, 255, 1),
  345px 190px 0 0 rgba(110, 205, 199, 1), 350px 190px 0 0 rgba(110, 205, 199, 1),
  355px 190px 0 0 rgba(110, 205, 199, 1), 360px 190px 0 0 rgba(255, 255, 255, 1),
  365px 190px 0 0 rgba(110, 205, 199, 1), 370px 190px 0 0 rgba(110, 205, 199, 1),
  375px 190px 0 0 rgba(110, 205, 199, 1), 380px 190px 0 0 rgba(255, 255, 255, 1),
  385px 190px 0 0 rgba(110, 205, 199, 1), 390px 190px 0 0 rgba(110, 205, 199, 1),
  395px 190px 0 0 rgba(110, 205, 199, 1), 400px 190px 0 0 rgba(255, 255, 255, 1),
  405px 190px 0 0 rgba(110, 205, 199, 1), 410px 190px 0 0 rgba(110, 205, 199, 1),
  415px 190px 0 0 rgba(110, 205, 199, 1), 420px 190px 0 0 rgba(255, 255, 255, 1),
  425px 190px 0 0 rgba(110, 205, 199, 1), 430px 190px 0 0 rgba(110, 205, 199, 1),
  435px 190px 0 0 rgba(110, 205, 199, 1), 440px 190px 0 0 rgba(255, 255, 255, 1),
  445px 190px 0 0 rgba(110, 205, 199, 1), 450px 190px 0 0 rgba(110, 205, 199, 1),
  455px 190px 0 0 rgba(110, 205, 199, 1), 460px 190px 0 0 rgba(255, 255, 255, 1),
  465px 190px 0 0 rgba(110, 205, 199, 1), 470px 190px 0 0 rgba(110, 205, 199, 1),
  475px 190px 0 0 rgba(110, 205, 199, 1), 480px 190px 0 0 rgba(255, 255, 255, 1),
  485px 190px 0 0 rgba(110, 205, 199, 1), 490px 190px 0 0 rgba(110, 205, 199, 1),
  495px 190px 0 0 rgba(110, 205, 199, 1), 500px 190px 0 0 rgba(255, 255, 255, 1),
  505px 190px 0 0 rgba(110, 205, 199, 1), 510px 190px 0 0 rgba(110, 205, 199, 1),
  515px 190px 0 0 rgba(110, 205, 199, 1), 520px 190px 0 0 rgba(255, 255, 255, 1),
  525px 190px 0 0 rgba(110, 205, 199, 1), 530px 190px 0 0 rgba(110, 205, 199, 1),
  535px 190px 0 0 rgba(110, 205, 199, 1), 540px 190px 0 0 rgba(255, 255, 255, 1),
  545px 190px 0 0 rgba(110, 205, 199, 1), 550px 190px 0 0 rgba(110, 205, 199, 1),
  555px 190px 0 0 rgba(110, 205, 199, 1), 560px 190px 0 0 rgba(255, 255, 255, 1),
  565px 190px 0 0 rgba(110, 205, 199, 1), 570px 190px 0 0 rgba(110, 205, 199, 1),
  575px 190px 0 0 rgba(110, 205, 199, 1), 580px 190px 0 0 rgba(255, 255, 255, 1),
  585px 190px 0 0 rgba(110, 205, 199, 1), 590px 190px 0 0 rgba(110, 205, 199, 1),
  595px 190px 0 0 rgba(110, 205, 199, 1), 600px 190px 0 0 rgba(255, 255, 255, 1),
  605px 190px 0 0 rgba(110, 205, 199, 1), 610px 190px 0 0 rgba(110, 205, 199, 1),
  615px 190px 0 0 rgba(110, 205, 199, 1), 620px 190px 0 0 rgba(255, 255, 255, 1),
  625px 190px 0 0 rgba(110, 205, 199, 1), 630px 190px 0 0 rgba(110, 205, 199, 1),
  635px 190px 0 0 rgba(110, 205, 199, 1), 640px 190px 0 0 rgba(255, 255, 255, 1),
  645px 190px 0 0 rgba(110, 205, 199, 1), 650px 190px 0 0 rgba(110, 205, 199, 1),
  655px 190px 0 0 rgba(110, 205, 199, 1), 660px 190px 0 0 rgba(255, 255, 255, 1),
  665px 190px 0 0 rgba(110, 205, 199, 1), 670px 190px 0 0 rgba(110, 205, 199, 1),
  675px 190px 0 0 rgba(110, 205, 199, 1), 680px 190px 0 0 rgba(255, 255, 255, 1),
  685px 190px 0 0 rgba(203, 109, 181, 1), 690px 190px 0 0 rgba(255, 205, 234, 1),
  695px 190px 0 0 rgba(255, 205, 234, 1), 700px 190px 0 0 rgba(168, 90, 150, 1),
  705px 190px 0 0 rgba(203, 109, 181, 1), 5px 195px 0 0 rgba(203, 109, 181, 1),
  10px 195px 0 0 rgba(252, 231, 243, 1), 15px 195px 0 0 rgba(255, 205, 234, 1),
  20px 195px 0 0 rgba(255, 205, 234, 1), 25px 195px 0 0 rgba(203, 109, 181, 1),
  30px 195px 0 0 rgba(110, 205, 199, 1), 35px 195px 0 0 rgba(255, 255, 255, 1),
  40px 195px 0 0 rgba(110, 205, 199, 1), 45px 195px 0 0 rgba(255, 255, 255, 1),
  50px 195px 0 0 rgba(110, 205, 199, 1), 55px 195px 0 0 rgba(255, 255, 255, 1),
  60px 195px 0 0 rgba(110, 205, 199, 1), 65px 195px 0 0 rgba(255, 255, 255, 1),
  70px 195px 0 0 rgba(110, 205, 199, 1), 75px 195px 0 0 rgba(255, 255, 255, 1),
  80px 195px 0 0 rgba(110, 205, 199, 1), 85px 195px 0 0 rgba(255, 255, 255, 1),
  90px 195px 0 0 rgba(110, 205, 199, 1), 95px 195px 0 0 rgba(255, 255, 255, 1),
  100px 195px 0 0 rgba(110, 205, 199, 1), 105px 195px 0 0 rgba(255, 255, 255, 1),
  110px 195px 0 0 rgba(110, 205, 199, 1), 115px 195px 0 0 rgba(255, 255, 255, 1),
  120px 195px 0 0 rgba(110, 205, 199, 1), 125px 195px 0 0 rgba(255, 255, 255, 1),
  130px 195px 0 0 rgba(110, 205, 199, 1), 135px 195px 0 0 rgba(255, 255, 255, 1),
  140px 195px 0 0 rgba(110, 205, 199, 1), 145px 195px 0 0 rgba(255, 255, 255, 1),
  150px 195px 0 0 rgba(110, 205, 199, 1), 155px 195px 0 0 rgba(255, 255, 255, 1),
  160px 195px 0 0 rgba(110, 205, 199, 1), 165px 195px 0 0 rgba(255, 255, 255, 1),
  170px 195px 0 0 rgba(110, 205, 199, 1), 175px 195px 0 0 rgba(255, 255, 255, 1),
  180px 195px 0 0 rgba(110, 205, 199, 1), 185px 195px 0 0 rgba(255, 255, 255, 1),
  190px 195px 0 0 rgba(110, 205, 199, 1), 195px 195px 0 0 rgba(255, 255, 255, 1),
  200px 195px 0 0 rgba(110, 205, 199, 1), 205px 195px 0 0 rgba(255, 255, 255, 1),
  210px 195px 0 0 rgba(110, 205, 199, 1), 215px 195px 0 0 rgba(255, 255, 255, 1),
  220px 195px 0 0 rgba(110, 205, 199, 1), 225px 195px 0 0 rgba(255, 255, 255, 1),
  230px 195px 0 0 rgba(110, 205, 199, 1), 235px 195px 0 0 rgba(255, 255, 255, 1),
  240px 195px 0 0 rgba(110, 205, 199, 1), 245px 195px 0 0 rgba(255, 255, 255, 1),
  250px 195px 0 0 rgba(110, 205, 199, 1), 255px 195px 0 0 rgba(255, 255, 255, 1),
  260px 195px 0 0 rgba(110, 205, 199, 1), 265px 195px 0 0 rgba(255, 255, 255, 1),
  270px 195px 0 0 rgba(110, 205, 199, 1), 275px 195px 0 0 rgba(255, 255, 255, 1),
  280px 195px 0 0 rgba(110, 205, 199, 1), 285px 195px 0 0 rgba(255, 255, 255, 1),
  290px 195px 0 0 rgba(110, 205, 199, 1), 295px 195px 0 0 rgba(255, 255, 255, 1),
  300px 195px 0 0 rgba(110, 205, 199, 1), 305px 195px 0 0 rgba(255, 255, 255, 1),
  310px 195px 0 0 rgba(110, 205, 199, 1), 315px 195px 0 0 rgba(255, 255, 255, 1),
  320px 195px 0 0 rgba(110, 205, 199, 1), 325px 195px 0 0 rgba(255, 255, 255, 1),
  330px 195px 0 0 rgba(110, 205, 199, 1), 335px 195px 0 0 rgba(255, 255, 255, 1),
  340px 195px 0 0 rgba(110, 205, 199, 1), 345px 195px 0 0 rgba(255, 255, 255, 1),
  350px 195px 0 0 rgba(110, 205, 199, 1), 355px 195px 0 0 rgba(255, 255, 255, 1),
  360px 195px 0 0 rgba(110, 205, 199, 1), 365px 195px 0 0 rgba(255, 255, 255, 1),
  370px 195px 0 0 rgba(110, 205, 199, 1), 375px 195px 0 0 rgba(255, 255, 255, 1),
  380px 195px 0 0 rgba(110, 205, 199, 1), 385px 195px 0 0 rgba(255, 255, 255, 1),
  390px 195px 0 0 rgba(110, 205, 199, 1), 395px 195px 0 0 rgba(255, 255, 255, 1),
  400px 195px 0 0 rgba(110, 205, 199, 1), 405px 195px 0 0 rgba(255, 255, 255, 1),
  410px 195px 0 0 rgba(110, 205, 199, 1), 415px 195px 0 0 rgba(255, 255, 255, 1),
  420px 195px 0 0 rgba(110, 205, 199, 1), 425px 195px 0 0 rgba(255, 255, 255, 1),
  430px 195px 0 0 rgba(110, 205, 199, 1), 435px 195px 0 0 rgba(255, 255, 255, 1),
  440px 195px 0 0 rgba(110, 205, 199, 1), 445px 195px 0 0 rgba(255, 255, 255, 1),
  450px 195px 0 0 rgba(110, 205, 199, 1), 455px 195px 0 0 rgba(255, 255, 255, 1),
  460px 195px 0 0 rgba(110, 205, 199, 1), 465px 195px 0 0 rgba(255, 255, 255, 1),
  470px 195px 0 0 rgba(110, 205, 199, 1), 475px 195px 0 0 rgba(255, 255, 255, 1),
  480px 195px 0 0 rgba(110, 205, 199, 1), 485px 195px 0 0 rgba(255, 255, 255, 1),
  490px 195px 0 0 rgba(110, 205, 199, 1), 495px 195px 0 0 rgba(255, 255, 255, 1),
  500px 195px 0 0 rgba(110, 205, 199, 1), 505px 195px 0 0 rgba(255, 255, 255, 1),
  510px 195px 0 0 rgba(110, 205, 199, 1), 515px 195px 0 0 rgba(255, 255, 255, 1),
  520px 195px 0 0 rgba(110, 205, 199, 1), 525px 195px 0 0 rgba(255, 255, 255, 1),
  530px 195px 0 0 rgba(110, 205, 199, 1), 535px 195px 0 0 rgba(255, 255, 255, 1),
  540px 195px 0 0 rgba(110, 205, 199, 1), 545px 195px 0 0 rgba(255, 255, 255, 1),
  550px 195px 0 0 rgba(110, 205, 199, 1), 555px 195px 0 0 rgba(255, 255, 255, 1),
  560px 195px 0 0 rgba(110, 205, 199, 1), 565px 195px 0 0 rgba(255, 255, 255, 1),
  570px 195px 0 0 rgba(110, 205, 199, 1), 575px 195px 0 0 rgba(255, 255, 255, 1),
  580px 195px 0 0 rgba(110, 205, 199, 1), 585px 195px 0 0 rgba(255, 255, 255, 1),
  590px 195px 0 0 rgba(110, 205, 199, 1), 595px 195px 0 0 rgba(255, 255, 255, 1),
  600px 195px 0 0 rgba(110, 205, 199, 1), 605px 195px 0 0 rgba(255, 255, 255, 1),
  610px 195px 0 0 rgba(110, 205, 199, 1), 615px 195px 0 0 rgba(255, 255, 255, 1),
  620px 195px 0 0 rgba(110, 205, 199, 1), 625px 195px 0 0 rgba(255, 255, 255, 1),
  630px 195px 0 0 rgba(110, 205, 199, 1), 635px 195px 0 0 rgba(255, 255, 255, 1),
  640px 195px 0 0 rgba(110, 205, 199, 1), 645px 195px 0 0 rgba(255, 255, 255, 1),
  650px 195px 0 0 rgba(110, 205, 199, 1), 655px 195px 0 0 rgba(255, 255, 255, 1),
  660px 195px 0 0 rgba(110, 205, 199, 1), 665px 195px 0 0 rgba(255, 255, 255, 1),
  670px 195px 0 0 rgba(110, 205, 199, 1), 675px 195px 0 0 rgba(255, 255, 255, 1),
  680px 195px 0 0 rgba(110, 205, 199, 1), 685px 195px 0 0 rgba(203, 109, 181, 1),
  690px 195px 0 0 rgba(255, 205, 234, 1), 695px 195px 0 0 rgba(255, 205, 234, 1),
  700px 195px 0 0 rgba(168, 90, 150, 1), 705px 195px 0 0 rgba(203, 109, 181, 1),
  5px 200px 0 0 rgba(203, 109, 181, 1), 10px 200px 0 0 rgba(252, 231, 243, 1),
  15px 200px 0 0 rgba(255, 205, 234, 1), 20px 200px 0 0 rgba(255, 205, 234, 1),
  25px 200px 0 0 rgba(203, 109, 181, 1), 30px 200px 0 0 rgba(255, 255, 255, 1),
  35px 200px 0 0 rgba(110, 205, 199, 1), 40px 200px 0 0 rgba(255, 255, 255, 1),
  45px 200px 0 0 rgba(110, 205, 199, 1), 50px 200px 0 0 rgba(255, 255, 255, 1),
  55px 200px 0 0 rgba(110, 205, 199, 1), 60px 200px 0 0 rgba(255, 255, 255, 1),
  65px 200px 0 0 rgba(110, 205, 199, 1), 70px 200px 0 0 rgba(255, 255, 255, 1),
  75px 200px 0 0 rgba(110, 205, 199, 1), 80px 200px 0 0 rgba(255, 255, 255, 1),
  85px 200px 0 0 rgba(110, 205, 199, 1), 90px 200px 0 0 rgba(255, 255, 255, 1),
  95px 200px 0 0 rgba(110, 205, 199, 1), 100px 200px 0 0 rgba(255, 255, 255, 1),
  105px 200px 0 0 rgba(110, 205, 199, 1), 110px 200px 0 0 rgba(255, 255, 255, 1),
  115px 200px 0 0 rgba(110, 205, 199, 1), 120px 200px 0 0 rgba(255, 255, 255, 1),
  125px 200px 0 0 rgba(110, 205, 199, 1), 130px 200px 0 0 rgba(255, 255, 255, 1),
  135px 200px 0 0 rgba(110, 205, 199, 1), 140px 200px 0 0 rgba(255, 255, 255, 1),
  145px 200px 0 0 rgba(110, 205, 199, 1), 150px 200px 0 0 rgba(255, 255, 255, 1),
  155px 200px 0 0 rgba(110, 205, 199, 1), 160px 200px 0 0 rgba(255, 255, 255, 1),
  165px 200px 0 0 rgba(110, 205, 199, 1), 170px 200px 0 0 rgba(255, 255, 255, 1),
  175px 200px 0 0 rgba(110, 205, 199, 1), 180px 200px 0 0 rgba(255, 255, 255, 1),
  185px 200px 0 0 rgba(110, 205, 199, 1), 190px 200px 0 0 rgba(255, 255, 255, 1),
  195px 200px 0 0 rgba(110, 205, 199, 1), 200px 200px 0 0 rgba(255, 255, 255, 1),
  205px 200px 0 0 rgba(110, 205, 199, 1), 210px 200px 0 0 rgba(255, 255, 255, 1),
  215px 200px 0 0 rgba(110, 205, 199, 1), 220px 200px 0 0 rgba(255, 255, 255, 1),
  225px 200px 0 0 rgba(110, 205, 199, 1), 230px 200px 0 0 rgba(255, 255, 255, 1),
  235px 200px 0 0 rgba(110, 205, 199, 1), 240px 200px 0 0 rgba(255, 255, 255, 1),
  245px 200px 0 0 rgba(110, 205, 199, 1), 250px 200px 0 0 rgba(255, 255, 255, 1),
  255px 200px 0 0 rgba(110, 205, 199, 1), 260px 200px 0 0 rgba(255, 255, 255, 1),
  265px 200px 0 0 rgba(110, 205, 199, 1), 270px 200px 0 0 rgba(255, 255, 255, 1),
  275px 200px 0 0 rgba(110, 205, 199, 1), 280px 200px 0 0 rgba(255, 255, 255, 1),
  285px 200px 0 0 rgba(110, 205, 199, 1), 290px 200px 0 0 rgba(255, 255, 255, 1),
  295px 200px 0 0 rgba(110, 205, 199, 1), 300px 200px 0 0 rgba(255, 255, 255, 1),
  305px 200px 0 0 rgba(110, 205, 199, 1), 310px 200px 0 0 rgba(255, 255, 255, 1),
  315px 200px 0 0 rgba(110, 205, 199, 1), 320px 200px 0 0 rgba(255, 255, 255, 1),
  325px 200px 0 0 rgba(110, 205, 199, 1), 330px 200px 0 0 rgba(255, 255, 255, 1),
  335px 200px 0 0 rgba(110, 205, 199, 1), 340px 200px 0 0 rgba(255, 255, 255, 1),
  345px 200px 0 0 rgba(110, 205, 199, 1), 350px 200px 0 0 rgba(255, 255, 255, 1),
  355px 200px 0 0 rgba(110, 205, 199, 1), 360px 200px 0 0 rgba(255, 255, 255, 1),
  365px 200px 0 0 rgba(110, 205, 199, 1), 370px 200px 0 0 rgba(255, 255, 255, 1),
  375px 200px 0 0 rgba(110, 205, 199, 1), 380px 200px 0 0 rgba(255, 255, 255, 1),
  385px 200px 0 0 rgba(110, 205, 199, 1), 390px 200px 0 0 rgba(255, 255, 255, 1),
  395px 200px 0 0 rgba(110, 205, 199, 1), 400px 200px 0 0 rgba(255, 255, 255, 1),
  405px 200px 0 0 rgba(110, 205, 199, 1), 410px 200px 0 0 rgba(255, 255, 255, 1),
  415px 200px 0 0 rgba(110, 205, 199, 1), 420px 200px 0 0 rgba(255, 255, 255, 1),
  425px 200px 0 0 rgba(110, 205, 199, 1), 430px 200px 0 0 rgba(255, 255, 255, 1),
  435px 200px 0 0 rgba(110, 205, 199, 1), 440px 200px 0 0 rgba(255, 255, 255, 1),
  445px 200px 0 0 rgba(110, 205, 199, 1), 450px 200px 0 0 rgba(255, 255, 255, 1),
  455px 200px 0 0 rgba(110, 205, 199, 1), 460px 200px 0 0 rgba(255, 255, 255, 1),
  465px 200px 0 0 rgba(110, 205, 199, 1), 470px 200px 0 0 rgba(255, 255, 255, 1),
  475px 200px 0 0 rgba(110, 205, 199, 1), 480px 200px 0 0 rgba(255, 255, 255, 1),
  485px 200px 0 0 rgba(110, 205, 199, 1), 490px 200px 0 0 rgba(255, 255, 255, 1),
  495px 200px 0 0 rgba(110, 205, 199, 1), 500px 200px 0 0 rgba(255, 255, 255, 1),
  505px 200px 0 0 rgba(110, 205, 199, 1), 510px 200px 0 0 rgba(255, 255, 255, 1),
  515px 200px 0 0 rgba(110, 205, 199, 1), 520px 200px 0 0 rgba(255, 255, 255, 1),
  525px 200px 0 0 rgba(110, 205, 199, 1), 530px 200px 0 0 rgba(255, 255, 255, 1),
  535px 200px 0 0 rgba(110, 205, 199, 1), 540px 200px 0 0 rgba(255, 255, 255, 1),
  545px 200px 0 0 rgba(110, 205, 199, 1), 550px 200px 0 0 rgba(255, 255, 255, 1),
  555px 200px 0 0 rgba(110, 205, 199, 1), 560px 200px 0 0 rgba(255, 255, 255, 1),
  565px 200px 0 0 rgba(110, 205, 199, 1), 570px 200px 0 0 rgba(255, 255, 255, 1),
  575px 200px 0 0 rgba(110, 205, 199, 1), 580px 200px 0 0 rgba(255, 255, 255, 1),
  585px 200px 0 0 rgba(110, 205, 199, 1), 590px 200px 0 0 rgba(255, 255, 255, 1),
  595px 200px 0 0 rgba(110, 205, 199, 1), 600px 200px 0 0 rgba(255, 255, 255, 1),
  605px 200px 0 0 rgba(110, 205, 199, 1), 610px 200px 0 0 rgba(255, 255, 255, 1),
  615px 200px 0 0 rgba(110, 205, 199, 1), 620px 200px 0 0 rgba(255, 255, 255, 1),
  625px 200px 0 0 rgba(110, 205, 199, 1), 630px 200px 0 0 rgba(255, 255, 255, 1),
  635px 200px 0 0 rgba(110, 205, 199, 1), 640px 200px 0 0 rgba(255, 255, 255, 1),
  645px 200px 0 0 rgba(110, 205, 199, 1), 650px 200px 0 0 rgba(255, 255, 255, 1),
  655px 200px 0 0 rgba(110, 205, 199, 1), 660px 200px 0 0 rgba(255, 255, 255, 1),
  665px 200px 0 0 rgba(110, 205, 199, 1), 670px 200px 0 0 rgba(255, 255, 255, 1),
  675px 200px 0 0 rgba(110, 205, 199, 1), 680px 200px 0 0 rgba(255, 255, 255, 1),
  685px 200px 0 0 rgba(203, 109, 181, 1), 690px 200px 0 0 rgba(255, 205, 234, 1),
  695px 200px 0 0 rgba(255, 205, 234, 1), 700px 200px 0 0 rgba(168, 90, 150, 1),
  705px 200px 0 0 rgba(203, 109, 181, 1), 5px 205px 0 0 rgba(203, 109, 181, 1),
  10px 205px 0 0 rgba(252, 231, 243, 1), 15px 205px 0 0 rgba(255, 205, 234, 1),
  20px 205px 0 0 rgba(255, 205, 234, 1), 25px 205px 0 0 rgba(203, 109, 181, 1),
  30px 205px 0 0 rgba(110, 205, 199, 1), 35px 205px 0 0 rgba(255, 255, 255, 1),
  40px 205px 0 0 rgba(110, 205, 199, 1), 45px 205px 0 0 rgba(255, 255, 255, 1),
  50px 205px 0 0 rgba(110, 205, 199, 1), 55px 205px 0 0 rgba(255, 255, 255, 1),
  60px 205px 0 0 rgba(110, 205, 199, 1), 65px 205px 0 0 rgba(255, 255, 255, 1),
  70px 205px 0 0 rgba(110, 205, 199, 1), 75px 205px 0 0 rgba(255, 255, 255, 1),
  80px 205px 0 0 rgba(110, 205, 199, 1), 85px 205px 0 0 rgba(255, 255, 255, 1),
  90px 205px 0 0 rgba(110, 205, 199, 1), 95px 205px 0 0 rgba(255, 255, 255, 1),
  100px 205px 0 0 rgba(110, 205, 199, 1), 105px 205px 0 0 rgba(255, 255, 255, 1),
  110px 205px 0 0 rgba(110, 205, 199, 1), 115px 205px 0 0 rgba(255, 255, 255, 1),
  120px 205px 0 0 rgba(110, 205, 199, 1), 125px 205px 0 0 rgba(255, 255, 255, 1),
  130px 205px 0 0 rgba(110, 205, 199, 1), 135px 205px 0 0 rgba(255, 255, 255, 1),
  140px 205px 0 0 rgba(110, 205, 199, 1), 145px 205px 0 0 rgba(255, 255, 255, 1),
  150px 205px 0 0 rgba(110, 205, 199, 1), 155px 205px 0 0 rgba(255, 255, 255, 1),
  160px 205px 0 0 rgba(110, 205, 199, 1), 165px 205px 0 0 rgba(255, 255, 255, 1),
  170px 205px 0 0 rgba(110, 205, 199, 1), 175px 205px 0 0 rgba(255, 255, 255, 1),
  180px 205px 0 0 rgba(110, 205, 199, 1), 185px 205px 0 0 rgba(255, 255, 255, 1),
  190px 205px 0 0 rgba(110, 205, 199, 1), 195px 205px 0 0 rgba(255, 255, 255, 1),
  200px 205px 0 0 rgba(110, 205, 199, 1), 205px 205px 0 0 rgba(255, 255, 255, 1),
  210px 205px 0 0 rgba(110, 205, 199, 1), 215px 205px 0 0 rgba(255, 255, 255, 1),
  220px 205px 0 0 rgba(110, 205, 199, 1), 225px 205px 0 0 rgba(255, 255, 255, 1),
  230px 205px 0 0 rgba(110, 205, 199, 1), 235px 205px 0 0 rgba(255, 255, 255, 1),
  240px 205px 0 0 rgba(110, 205, 199, 1), 245px 205px 0 0 rgba(255, 255, 255, 1),
  250px 205px 0 0 rgba(110, 205, 199, 1), 255px 205px 0 0 rgba(255, 255, 255, 1),
  260px 205px 0 0 rgba(110, 205, 199, 1), 265px 205px 0 0 rgba(255, 255, 255, 1),
  270px 205px 0 0 rgba(110, 205, 199, 1), 275px 205px 0 0 rgba(255, 255, 255, 1),
  280px 205px 0 0 rgba(110, 205, 199, 1), 285px 205px 0 0 rgba(255, 255, 255, 1),
  290px 205px 0 0 rgba(110, 205, 199, 1), 295px 205px 0 0 rgba(255, 255, 255, 1),
  300px 205px 0 0 rgba(110, 205, 199, 1), 305px 205px 0 0 rgba(255, 255, 255, 1),
  310px 205px 0 0 rgba(110, 205, 199, 1), 315px 205px 0 0 rgba(255, 255, 255, 1),
  320px 205px 0 0 rgba(110, 205, 199, 1), 325px 205px 0 0 rgba(255, 255, 255, 1),
  330px 205px 0 0 rgba(110, 205, 199, 1), 335px 205px 0 0 rgba(255, 255, 255, 1),
  340px 205px 0 0 rgba(110, 205, 199, 1), 345px 205px 0 0 rgba(255, 255, 255, 1),
  350px 205px 0 0 rgba(110, 205, 199, 1), 355px 205px 0 0 rgba(255, 255, 255, 1),
  360px 205px 0 0 rgba(110, 205, 199, 1), 365px 205px 0 0 rgba(255, 255, 255, 1),
  370px 205px 0 0 rgba(110, 205, 199, 1), 375px 205px 0 0 rgba(255, 255, 255, 1),
  380px 205px 0 0 rgba(110, 205, 199, 1), 385px 205px 0 0 rgba(255, 255, 255, 1),
  390px 205px 0 0 rgba(110, 205, 199, 1), 395px 205px 0 0 rgba(255, 255, 255, 1),
  400px 205px 0 0 rgba(110, 205, 199, 1), 405px 205px 0 0 rgba(255, 255, 255, 1),
  410px 205px 0 0 rgba(110, 205, 199, 1), 415px 205px 0 0 rgba(255, 255, 255, 1),
  420px 205px 0 0 rgba(110, 205, 199, 1), 425px 205px 0 0 rgba(255, 255, 255, 1),
  430px 205px 0 0 rgba(110, 205, 199, 1), 435px 205px 0 0 rgba(255, 255, 255, 1),
  440px 205px 0 0 rgba(110, 205, 199, 1), 445px 205px 0 0 rgba(255, 255, 255, 1),
  450px 205px 0 0 rgba(110, 205, 199, 1), 455px 205px 0 0 rgba(255, 255, 255, 1),
  460px 205px 0 0 rgba(110, 205, 199, 1), 465px 205px 0 0 rgba(255, 255, 255, 1),
  470px 205px 0 0 rgba(110, 205, 199, 1), 475px 205px 0 0 rgba(255, 255, 255, 1),
  480px 205px 0 0 rgba(110, 205, 199, 1), 485px 205px 0 0 rgba(255, 255, 255, 1),
  490px 205px 0 0 rgba(110, 205, 199, 1), 495px 205px 0 0 rgba(255, 255, 255, 1),
  500px 205px 0 0 rgba(110, 205, 199, 1), 505px 205px 0 0 rgba(255, 255, 255, 1),
  510px 205px 0 0 rgba(110, 205, 199, 1), 515px 205px 0 0 rgba(255, 255, 255, 1),
  520px 205px 0 0 rgba(110, 205, 199, 1), 525px 205px 0 0 rgba(255, 255, 255, 1),
  530px 205px 0 0 rgba(110, 205, 199, 1), 535px 205px 0 0 rgba(255, 255, 255, 1),
  540px 205px 0 0 rgba(110, 205, 199, 1), 545px 205px 0 0 rgba(255, 255, 255, 1),
  550px 205px 0 0 rgba(110, 205, 199, 1), 555px 205px 0 0 rgba(255, 255, 255, 1),
  560px 205px 0 0 rgba(110, 205, 199, 1), 565px 205px 0 0 rgba(255, 255, 255, 1),
  570px 205px 0 0 rgba(110, 205, 199, 1), 575px 205px 0 0 rgba(255, 255, 255, 1),
  580px 205px 0 0 rgba(110, 205, 199, 1), 585px 205px 0 0 rgba(255, 255, 255, 1),
  590px 205px 0 0 rgba(110, 205, 199, 1), 595px 205px 0 0 rgba(255, 255, 255, 1),
  600px 205px 0 0 rgba(110, 205, 199, 1), 605px 205px 0 0 rgba(255, 255, 255, 1),
  610px 205px 0 0 rgba(110, 205, 199, 1), 615px 205px 0 0 rgba(255, 255, 255, 1),
  620px 205px 0 0 rgba(110, 205, 199, 1), 625px 205px 0 0 rgba(255, 255, 255, 1),
  630px 205px 0 0 rgba(110, 205, 199, 1), 635px 205px 0 0 rgba(255, 255, 255, 1),
  640px 205px 0 0 rgba(110, 205, 199, 1), 645px 205px 0 0 rgba(255, 255, 255, 1),
  650px 205px 0 0 rgba(110, 205, 199, 1), 655px 205px 0 0 rgba(255, 255, 255, 1),
  660px 205px 0 0 rgba(110, 205, 199, 1), 665px 205px 0 0 rgba(255, 255, 255, 1),
  670px 205px 0 0 rgba(110, 205, 199, 1), 675px 205px 0 0 rgba(255, 255, 255, 1),
  680px 205px 0 0 rgba(110, 205, 199, 1), 685px 205px 0 0 rgba(203, 109, 181, 1),
  690px 205px 0 0 rgba(255, 205, 234, 1), 695px 205px 0 0 rgba(255, 205, 234, 1),
  700px 205px 0 0 rgba(168, 90, 150, 1), 705px 205px 0 0 rgba(203, 109, 181, 1),
  5px 210px 0 0 rgba(203, 109, 181, 1), 10px 210px 0 0 rgba(252, 231, 243, 1),
  15px 210px 0 0 rgba(255, 205, 234, 1), 20px 210px 0 0 rgba(255, 205, 234, 1),
  25px 210px 0 0 rgba(203, 109, 181, 1), 30px 210px 0 0 rgba(255, 255, 255, 1),
  35px 210px 0 0 rgba(110, 205, 199, 1), 40px 210px 0 0 rgba(255, 255, 255, 1),
  45px 210px 0 0 rgba(110, 205, 199, 1), 50px 210px 0 0 rgba(255, 255, 255, 1),
  55px 210px 0 0 rgba(110, 205, 199, 1), 60px 210px 0 0 rgba(255, 255, 255, 1),
  65px 210px 0 0 rgba(110, 205, 199, 1), 70px 210px 0 0 rgba(255, 255, 255, 1),
  75px 210px 0 0 rgba(110, 205, 199, 1), 80px 210px 0 0 rgba(255, 255, 255, 1),
  85px 210px 0 0 rgba(110, 205, 199, 1), 90px 210px 0 0 rgba(255, 255, 255, 1),
  95px 210px 0 0 rgba(110, 205, 199, 1), 100px 210px 0 0 rgba(255, 255, 255, 1),
  105px 210px 0 0 rgba(110, 205, 199, 1), 110px 210px 0 0 rgba(255, 255, 255, 1),
  115px 210px 0 0 rgba(110, 205, 199, 1), 120px 210px 0 0 rgba(255, 255, 255, 1),
  125px 210px 0 0 rgba(110, 205, 199, 1), 130px 210px 0 0 rgba(255, 255, 255, 1),
  135px 210px 0 0 rgba(110, 205, 199, 1), 140px 210px 0 0 rgba(255, 255, 255, 1),
  145px 210px 0 0 rgba(110, 205, 199, 1), 150px 210px 0 0 rgba(255, 255, 255, 1),
  155px 210px 0 0 rgba(110, 205, 199, 1), 160px 210px 0 0 rgba(255, 255, 255, 1),
  165px 210px 0 0 rgba(110, 205, 199, 1), 170px 210px 0 0 rgba(255, 255, 255, 1),
  175px 210px 0 0 rgba(110, 205, 199, 1), 180px 210px 0 0 rgba(255, 255, 255, 1),
  185px 210px 0 0 rgba(110, 205, 199, 1), 190px 210px 0 0 rgba(255, 255, 255, 1),
  195px 210px 0 0 rgba(110, 205, 199, 1), 200px 210px 0 0 rgba(255, 255, 255, 1),
  205px 210px 0 0 rgba(110, 205, 199, 1), 210px 210px 0 0 rgba(255, 255, 255, 1),
  215px 210px 0 0 rgba(110, 205, 199, 1), 220px 210px 0 0 rgba(255, 255, 255, 1),
  225px 210px 0 0 rgba(110, 205, 199, 1), 230px 210px 0 0 rgba(255, 255, 255, 1),
  235px 210px 0 0 rgba(110, 205, 199, 1), 240px 210px 0 0 rgba(255, 255, 255, 1),
  245px 210px 0 0 rgba(110, 205, 199, 1), 250px 210px 0 0 rgba(255, 255, 255, 1),
  255px 210px 0 0 rgba(110, 205, 199, 1), 260px 210px 0 0 rgba(255, 255, 255, 1),
  265px 210px 0 0 rgba(110, 205, 199, 1), 270px 210px 0 0 rgba(255, 255, 255, 1),
  275px 210px 0 0 rgba(110, 205, 199, 1), 280px 210px 0 0 rgba(255, 255, 255, 1),
  285px 210px 0 0 rgba(110, 205, 199, 1), 290px 210px 0 0 rgba(255, 255, 255, 1),
  295px 210px 0 0 rgba(110, 205, 199, 1), 300px 210px 0 0 rgba(255, 255, 255, 1),
  305px 210px 0 0 rgba(110, 205, 199, 1), 310px 210px 0 0 rgba(255, 255, 255, 1),
  315px 210px 0 0 rgba(110, 205, 199, 1), 320px 210px 0 0 rgba(255, 255, 255, 1),
  325px 210px 0 0 rgba(110, 205, 199, 1), 330px 210px 0 0 rgba(255, 255, 255, 1),
  335px 210px 0 0 rgba(110, 205, 199, 1), 340px 210px 0 0 rgba(255, 255, 255, 1),
  345px 210px 0 0 rgba(110, 205, 199, 1), 350px 210px 0 0 rgba(255, 255, 255, 1),
  355px 210px 0 0 rgba(110, 205, 199, 1), 360px 210px 0 0 rgba(255, 255, 255, 1),
  365px 210px 0 0 rgba(110, 205, 199, 1), 370px 210px 0 0 rgba(255, 255, 255, 1),
  375px 210px 0 0 rgba(110, 205, 199, 1), 380px 210px 0 0 rgba(255, 255, 255, 1),
  385px 210px 0 0 rgba(110, 205, 199, 1), 390px 210px 0 0 rgba(255, 255, 255, 1),
  395px 210px 0 0 rgba(110, 205, 199, 1), 400px 210px 0 0 rgba(255, 255, 255, 1),
  405px 210px 0 0 rgba(110, 205, 199, 1), 410px 210px 0 0 rgba(255, 255, 255, 1),
  415px 210px 0 0 rgba(110, 205, 199, 1), 420px 210px 0 0 rgba(255, 255, 255, 1),
  425px 210px 0 0 rgba(110, 205, 199, 1), 430px 210px 0 0 rgba(255, 255, 255, 1),
  435px 210px 0 0 rgba(110, 205, 199, 1), 440px 210px 0 0 rgba(255, 255, 255, 1),
  445px 210px 0 0 rgba(110, 205, 199, 1), 450px 210px 0 0 rgba(255, 255, 255, 1),
  455px 210px 0 0 rgba(110, 205, 199, 1), 460px 210px 0 0 rgba(255, 255, 255, 1),
  465px 210px 0 0 rgba(110, 205, 199, 1), 470px 210px 0 0 rgba(255, 255, 255, 1),
  475px 210px 0 0 rgba(110, 205, 199, 1), 480px 210px 0 0 rgba(255, 255, 255, 1),
  485px 210px 0 0 rgba(110, 205, 199, 1), 490px 210px 0 0 rgba(255, 255, 255, 1),
  495px 210px 0 0 rgba(110, 205, 199, 1), 500px 210px 0 0 rgba(255, 255, 255, 1),
  505px 210px 0 0 rgba(110, 205, 199, 1), 510px 210px 0 0 rgba(255, 255, 255, 1),
  515px 210px 0 0 rgba(110, 205, 199, 1), 520px 210px 0 0 rgba(255, 255, 255, 1),
  525px 210px 0 0 rgba(110, 205, 199, 1), 530px 210px 0 0 rgba(255, 255, 255, 1),
  535px 210px 0 0 rgba(110, 205, 199, 1), 540px 210px 0 0 rgba(255, 255, 255, 1),
  545px 210px 0 0 rgba(110, 205, 199, 1), 550px 210px 0 0 rgba(255, 255, 255, 1),
  555px 210px 0 0 rgba(110, 205, 199, 1), 560px 210px 0 0 rgba(255, 255, 255, 1),
  565px 210px 0 0 rgba(110, 205, 199, 1), 570px 210px 0 0 rgba(255, 255, 255, 1),
  575px 210px 0 0 rgba(110, 205, 199, 1), 580px 210px 0 0 rgba(255, 255, 255, 1),
  585px 210px 0 0 rgba(110, 205, 199, 1), 590px 210px 0 0 rgba(255, 255, 255, 1),
  595px 210px 0 0 rgba(110, 205, 199, 1), 600px 210px 0 0 rgba(255, 255, 255, 1),
  605px 210px 0 0 rgba(110, 205, 199, 1), 610px 210px 0 0 rgba(255, 255, 255, 1),
  615px 210px 0 0 rgba(110, 205, 199, 1), 620px 210px 0 0 rgba(255, 255, 255, 1),
  625px 210px 0 0 rgba(110, 205, 199, 1), 630px 210px 0 0 rgba(255, 255, 255, 1),
  635px 210px 0 0 rgba(110, 205, 199, 1), 640px 210px 0 0 rgba(255, 255, 255, 1),
  645px 210px 0 0 rgba(110, 205, 199, 1), 650px 210px 0 0 rgba(255, 255, 255, 1),
  655px 210px 0 0 rgba(110, 205, 199, 1), 660px 210px 0 0 rgba(255, 255, 255, 1),
  665px 210px 0 0 rgba(110, 205, 199, 1), 670px 210px 0 0 rgba(255, 255, 255, 1),
  675px 210px 0 0 rgba(110, 205, 199, 1), 680px 210px 0 0 rgba(255, 255, 255, 1),
  685px 210px 0 0 rgba(203, 109, 181, 1), 690px 210px 0 0 rgba(255, 205, 234, 1),
  695px 210px 0 0 rgba(255, 205, 234, 1), 700px 210px 0 0 rgba(168, 90, 150, 1),
  705px 210px 0 0 rgba(203, 109, 181, 1), 5px 215px 0 0 rgba(203, 109, 181, 1),
  10px 215px 0 0 rgba(252, 231, 243, 1), 15px 215px 0 0 rgba(255, 205, 234, 1),
  20px 215px 0 0 rgba(255, 205, 234, 1), 25px 215px 0 0 rgba(203, 109, 181, 1),
  30px 215px 0 0 rgba(110, 205, 199, 1), 35px 215px 0 0 rgba(255, 255, 255, 1),
  40px 215px 0 0 rgba(110, 205, 199, 1), 45px 215px 0 0 rgba(255, 255, 255, 1),
  50px 215px 0 0 rgba(110, 205, 199, 1), 55px 215px 0 0 rgba(255, 255, 255, 1),
  60px 215px 0 0 rgba(110, 205, 199, 1), 65px 215px 0 0 rgba(255, 255, 255, 1),
  70px 215px 0 0 rgba(110, 205, 199, 1), 75px 215px 0 0 rgba(255, 255, 255, 1),
  80px 215px 0 0 rgba(110, 205, 199, 1), 85px 215px 0 0 rgba(255, 255, 255, 1),
  90px 215px 0 0 rgba(110, 205, 199, 1), 95px 215px 0 0 rgba(255, 255, 255, 1),
  100px 215px 0 0 rgba(110, 205, 199, 1), 105px 215px 0 0 rgba(255, 255, 255, 1),
  110px 215px 0 0 rgba(110, 205, 199, 1), 115px 215px 0 0 rgba(255, 255, 255, 1),
  120px 215px 0 0 rgba(110, 205, 199, 1), 125px 215px 0 0 rgba(255, 255, 255, 1),
  130px 215px 0 0 rgba(110, 205, 199, 1), 135px 215px 0 0 rgba(255, 255, 255, 1),
  140px 215px 0 0 rgba(110, 205, 199, 1), 145px 215px 0 0 rgba(255, 255, 255, 1),
  150px 215px 0 0 rgba(110, 205, 199, 1), 155px 215px 0 0 rgba(255, 255, 255, 1),
  160px 215px 0 0 rgba(110, 205, 199, 1), 165px 215px 0 0 rgba(255, 255, 255, 1),
  170px 215px 0 0 rgba(110, 205, 199, 1), 175px 215px 0 0 rgba(255, 255, 255, 1),
  180px 215px 0 0 rgba(110, 205, 199, 1), 185px 215px 0 0 rgba(255, 255, 255, 1),
  190px 215px 0 0 rgba(110, 205, 199, 1), 195px 215px 0 0 rgba(255, 255, 255, 1),
  200px 215px 0 0 rgba(110, 205, 199, 1), 205px 215px 0 0 rgba(255, 255, 255, 1),
  210px 215px 0 0 rgba(110, 205, 199, 1), 215px 215px 0 0 rgba(255, 255, 255, 1),
  220px 215px 0 0 rgba(110, 205, 199, 1), 225px 215px 0 0 rgba(255, 255, 255, 1),
  230px 215px 0 0 rgba(110, 205, 199, 1), 235px 215px 0 0 rgba(255, 255, 255, 1),
  240px 215px 0 0 rgba(110, 205, 199, 1), 245px 215px 0 0 rgba(255, 255, 255, 1),
  250px 215px 0 0 rgba(110, 205, 199, 1), 255px 215px 0 0 rgba(255, 255, 255, 1),
  260px 215px 0 0 rgba(110, 205, 199, 1), 265px 215px 0 0 rgba(255, 255, 255, 1),
  270px 215px 0 0 rgba(110, 205, 199, 1), 275px 215px 0 0 rgba(255, 255, 255, 1),
  280px 215px 0 0 rgba(110, 205, 199, 1), 285px 215px 0 0 rgba(255, 255, 255, 1),
  290px 215px 0 0 rgba(110, 205, 199, 1), 295px 215px 0 0 rgba(255, 255, 255, 1),
  300px 215px 0 0 rgba(110, 205, 199, 1), 305px 215px 0 0 rgba(255, 255, 255, 1),
  310px 215px 0 0 rgba(110, 205, 199, 1), 315px 215px 0 0 rgba(255, 255, 255, 1),
  320px 215px 0 0 rgba(110, 205, 199, 1), 325px 215px 0 0 rgba(255, 255, 255, 1),
  330px 215px 0 0 rgba(110, 205, 199, 1), 335px 215px 0 0 rgba(255, 255, 255, 1),
  340px 215px 0 0 rgba(110, 205, 199, 1), 345px 215px 0 0 rgba(255, 255, 255, 1),
  350px 215px 0 0 rgba(110, 205, 199, 1), 355px 215px 0 0 rgba(255, 255, 255, 1),
  360px 215px 0 0 rgba(110, 205, 199, 1), 365px 215px 0 0 rgba(255, 255, 255, 1),
  370px 215px 0 0 rgba(110, 205, 199, 1), 375px 215px 0 0 rgba(255, 255, 255, 1),
  380px 215px 0 0 rgba(110, 205, 199, 1), 385px 215px 0 0 rgba(255, 255, 255, 1),
  390px 215px 0 0 rgba(110, 205, 199, 1), 395px 215px 0 0 rgba(255, 255, 255, 1),
  400px 215px 0 0 rgba(110, 205, 199, 1), 405px 215px 0 0 rgba(255, 255, 255, 1),
  410px 215px 0 0 rgba(110, 205, 199, 1), 415px 215px 0 0 rgba(255, 255, 255, 1),
  420px 215px 0 0 rgba(110, 205, 199, 1), 425px 215px 0 0 rgba(255, 255, 255, 1),
  430px 215px 0 0 rgba(110, 205, 199, 1), 435px 215px 0 0 rgba(255, 255, 255, 1),
  440px 215px 0 0 rgba(110, 205, 199, 1), 445px 215px 0 0 rgba(255, 255, 255, 1),
  450px 215px 0 0 rgba(110, 205, 199, 1), 455px 215px 0 0 rgba(255, 255, 255, 1),
  460px 215px 0 0 rgba(110, 205, 199, 1), 465px 215px 0 0 rgba(255, 255, 255, 1),
  470px 215px 0 0 rgba(110, 205, 199, 1), 475px 215px 0 0 rgba(255, 255, 255, 1),
  480px 215px 0 0 rgba(110, 205, 199, 1), 485px 215px 0 0 rgba(255, 255, 255, 1),
  490px 215px 0 0 rgba(110, 205, 199, 1), 495px 215px 0 0 rgba(255, 255, 255, 1),
  500px 215px 0 0 rgba(110, 205, 199, 1), 505px 215px 0 0 rgba(255, 255, 255, 1),
  510px 215px 0 0 rgba(110, 205, 199, 1), 515px 215px 0 0 rgba(255, 255, 255, 1),
  520px 215px 0 0 rgba(110, 205, 199, 1), 525px 215px 0 0 rgba(255, 255, 255, 1),
  530px 215px 0 0 rgba(110, 205, 199, 1), 535px 215px 0 0 rgba(255, 255, 255, 1),
  540px 215px 0 0 rgba(110, 205, 199, 1), 545px 215px 0 0 rgba(255, 255, 255, 1),
  550px 215px 0 0 rgba(110, 205, 199, 1), 555px 215px 0 0 rgba(255, 255, 255, 1),
  560px 215px 0 0 rgba(110, 205, 199, 1), 565px 215px 0 0 rgba(255, 255, 255, 1),
  570px 215px 0 0 rgba(110, 205, 199, 1), 575px 215px 0 0 rgba(255, 255, 255, 1),
  580px 215px 0 0 rgba(110, 205, 199, 1), 585px 215px 0 0 rgba(255, 255, 255, 1),
  590px 215px 0 0 rgba(110, 205, 199, 1), 595px 215px 0 0 rgba(255, 255, 255, 1),
  600px 215px 0 0 rgba(110, 205, 199, 1), 605px 215px 0 0 rgba(255, 255, 255, 1),
  610px 215px 0 0 rgba(110, 205, 199, 1), 615px 215px 0 0 rgba(255, 255, 255, 1),
  620px 215px 0 0 rgba(110, 205, 199, 1), 625px 215px 0 0 rgba(255, 255, 255, 1),
  630px 215px 0 0 rgba(110, 205, 199, 1), 635px 215px 0 0 rgba(255, 255, 255, 1),
  640px 215px 0 0 rgba(110, 205, 199, 1), 645px 215px 0 0 rgba(255, 255, 255, 1),
  650px 215px 0 0 rgba(110, 205, 199, 1), 655px 215px 0 0 rgba(255, 255, 255, 1),
  660px 215px 0 0 rgba(110, 205, 199, 1), 665px 215px 0 0 rgba(255, 255, 255, 1),
  670px 215px 0 0 rgba(110, 205, 199, 1), 675px 215px 0 0 rgba(255, 255, 255, 1),
  680px 215px 0 0 rgba(110, 205, 199, 1), 685px 215px 0 0 rgba(203, 109, 181, 1),
  690px 215px 0 0 rgba(255, 205, 234, 1), 695px 215px 0 0 rgba(255, 205, 234, 1),
  700px 215px 0 0 rgba(168, 90, 150, 1), 705px 215px 0 0 rgba(203, 109, 181, 1),
  5px 220px 0 0 rgba(203, 109, 181, 1), 10px 220px 0 0 rgba(252, 231, 243, 1),
  15px 220px 0 0 rgba(255, 205, 234, 1), 20px 220px 0 0 rgba(255, 205, 234, 1),
  25px 220px 0 0 rgba(203, 109, 181, 1), 30px 220px 0 0 rgba(255, 255, 255, 1),
  35px 220px 0 0 rgba(255, 255, 255, 1), 40px 220px 0 0 rgba(255, 255, 255, 1),
  45px 220px 0 0 rgba(110, 205, 199, 1), 50px 220px 0 0 rgba(255, 255, 255, 1),
  55px 220px 0 0 rgba(255, 255, 255, 1), 60px 220px 0 0 rgba(255, 255, 255, 1),
  65px 220px 0 0 rgba(110, 205, 199, 1), 70px 220px 0 0 rgba(255, 255, 255, 1),
  75px 220px 0 0 rgba(255, 255, 255, 1), 80px 220px 0 0 rgba(255, 255, 255, 1),
  85px 220px 0 0 rgba(110, 205, 199, 1), 90px 220px 0 0 rgba(255, 255, 255, 1),
  95px 220px 0 0 rgba(255, 255, 255, 1), 100px 220px 0 0 rgba(255, 255, 255, 1),
  105px 220px 0 0 rgba(110, 205, 199, 1), 110px 220px 0 0 rgba(255, 255, 255, 1),
  115px 220px 0 0 rgba(255, 255, 255, 1), 120px 220px 0 0 rgba(255, 255, 255, 1),
  125px 220px 0 0 rgba(110, 205, 199, 1), 130px 220px 0 0 rgba(255, 255, 255, 1),
  135px 220px 0 0 rgba(255, 255, 255, 1), 140px 220px 0 0 rgba(255, 255, 255, 1),
  145px 220px 0 0 rgba(110, 205, 199, 1), 150px 220px 0 0 rgba(255, 255, 255, 1),
  155px 220px 0 0 rgba(255, 255, 255, 1), 160px 220px 0 0 rgba(255, 255, 255, 1),
  165px 220px 0 0 rgba(110, 205, 199, 1), 170px 220px 0 0 rgba(255, 255, 255, 1),
  175px 220px 0 0 rgba(255, 255, 255, 1), 180px 220px 0 0 rgba(255, 255, 255, 1),
  185px 220px 0 0 rgba(110, 205, 199, 1), 190px 220px 0 0 rgba(255, 255, 255, 1),
  195px 220px 0 0 rgba(255, 255, 255, 1), 200px 220px 0 0 rgba(255, 255, 255, 1),
  205px 220px 0 0 rgba(110, 205, 199, 1), 210px 220px 0 0 rgba(255, 255, 255, 1),
  215px 220px 0 0 rgba(255, 255, 255, 1), 220px 220px 0 0 rgba(255, 255, 255, 1),
  225px 220px 0 0 rgba(110, 205, 199, 1), 230px 220px 0 0 rgba(255, 255, 255, 1),
  235px 220px 0 0 rgba(255, 255, 255, 1), 240px 220px 0 0 rgba(255, 255, 255, 1),
  245px 220px 0 0 rgba(110, 205, 199, 1), 250px 220px 0 0 rgba(255, 255, 255, 1),
  255px 220px 0 0 rgba(255, 255, 255, 1), 260px 220px 0 0 rgba(255, 255, 255, 1),
  265px 220px 0 0 rgba(110, 205, 199, 1), 270px 220px 0 0 rgba(255, 255, 255, 1),
  275px 220px 0 0 rgba(255, 255, 255, 1), 280px 220px 0 0 rgba(255, 255, 255, 1),
  285px 220px 0 0 rgba(110, 205, 199, 1), 290px 220px 0 0 rgba(255, 255, 255, 1),
  295px 220px 0 0 rgba(255, 255, 255, 1), 300px 220px 0 0 rgba(255, 255, 255, 1),
  305px 220px 0 0 rgba(110, 205, 199, 1), 310px 220px 0 0 rgba(255, 255, 255, 1),
  315px 220px 0 0 rgba(255, 255, 255, 1), 320px 220px 0 0 rgba(255, 255, 255, 1),
  325px 220px 0 0 rgba(110, 205, 199, 1), 330px 220px 0 0 rgba(255, 255, 255, 1),
  335px 220px 0 0 rgba(255, 255, 255, 1), 340px 220px 0 0 rgba(255, 255, 255, 1),
  345px 220px 0 0 rgba(110, 205, 199, 1), 350px 220px 0 0 rgba(255, 255, 255, 1),
  355px 220px 0 0 rgba(255, 255, 255, 1), 360px 220px 0 0 rgba(255, 255, 255, 1),
  365px 220px 0 0 rgba(110, 205, 199, 1), 370px 220px 0 0 rgba(255, 255, 255, 1),
  375px 220px 0 0 rgba(255, 255, 255, 1), 380px 220px 0 0 rgba(255, 255, 255, 1),
  385px 220px 0 0 rgba(110, 205, 199, 1), 390px 220px 0 0 rgba(255, 255, 255, 1),
  395px 220px 0 0 rgba(255, 255, 255, 1), 400px 220px 0 0 rgba(255, 255, 255, 1),
  405px 220px 0 0 rgba(110, 205, 199, 1), 410px 220px 0 0 rgba(255, 255, 255, 1),
  415px 220px 0 0 rgba(255, 255, 255, 1), 420px 220px 0 0 rgba(255, 255, 255, 1),
  425px 220px 0 0 rgba(110, 205, 199, 1), 430px 220px 0 0 rgba(255, 255, 255, 1),
  435px 220px 0 0 rgba(255, 255, 255, 1), 440px 220px 0 0 rgba(255, 255, 255, 1),
  445px 220px 0 0 rgba(110, 205, 199, 1), 450px 220px 0 0 rgba(255, 255, 255, 1),
  455px 220px 0 0 rgba(255, 255, 255, 1), 460px 220px 0 0 rgba(255, 255, 255, 1),
  465px 220px 0 0 rgba(110, 205, 199, 1), 470px 220px 0 0 rgba(255, 255, 255, 1),
  475px 220px 0 0 rgba(255, 255, 255, 1), 480px 220px 0 0 rgba(255, 255, 255, 1),
  485px 220px 0 0 rgba(110, 205, 199, 1), 490px 220px 0 0 rgba(255, 255, 255, 1),
  495px 220px 0 0 rgba(255, 255, 255, 1), 500px 220px 0 0 rgba(255, 255, 255, 1),
  505px 220px 0 0 rgba(110, 205, 199, 1), 510px 220px 0 0 rgba(255, 255, 255, 1),
  515px 220px 0 0 rgba(255, 255, 255, 1), 520px 220px 0 0 rgba(255, 255, 255, 1),
  525px 220px 0 0 rgba(110, 205, 199, 1), 530px 220px 0 0 rgba(255, 255, 255, 1),
  535px 220px 0 0 rgba(255, 255, 255, 1), 540px 220px 0 0 rgba(255, 255, 255, 1),
  545px 220px 0 0 rgba(110, 205, 199, 1), 550px 220px 0 0 rgba(255, 255, 255, 1),
  555px 220px 0 0 rgba(255, 255, 255, 1), 560px 220px 0 0 rgba(255, 255, 255, 1),
  565px 220px 0 0 rgba(110, 205, 199, 1), 570px 220px 0 0 rgba(255, 255, 255, 1),
  575px 220px 0 0 rgba(255, 255, 255, 1), 580px 220px 0 0 rgba(255, 255, 255, 1),
  585px 220px 0 0 rgba(110, 205, 199, 1), 590px 220px 0 0 rgba(255, 255, 255, 1),
  595px 220px 0 0 rgba(255, 255, 255, 1), 600px 220px 0 0 rgba(255, 255, 255, 1),
  605px 220px 0 0 rgba(110, 205, 199, 1), 610px 220px 0 0 rgba(255, 255, 255, 1),
  615px 220px 0 0 rgba(255, 255, 255, 1), 620px 220px 0 0 rgba(255, 255, 255, 1),
  625px 220px 0 0 rgba(110, 205, 199, 1), 630px 220px 0 0 rgba(255, 255, 255, 1),
  635px 220px 0 0 rgba(255, 255, 255, 1), 640px 220px 0 0 rgba(255, 255, 255, 1),
  645px 220px 0 0 rgba(110, 205, 199, 1), 650px 220px 0 0 rgba(255, 255, 255, 1),
  655px 220px 0 0 rgba(255, 255, 255, 1), 660px 220px 0 0 rgba(255, 255, 255, 1),
  665px 220px 0 0 rgba(110, 205, 199, 1), 670px 220px 0 0 rgba(255, 255, 255, 1),
  675px 220px 0 0 rgba(255, 255, 255, 1), 680px 220px 0 0 rgba(255, 255, 255, 1),
  685px 220px 0 0 rgba(203, 109, 181, 1), 690px 220px 0 0 rgba(255, 205, 234, 1),
  695px 220px 0 0 rgba(255, 205, 234, 1), 700px 220px 0 0 rgba(168, 90, 150, 1),
  705px 220px 0 0 rgba(203, 109, 181, 1), 5px 225px 0 0 rgba(203, 109, 181, 1),
  10px 225px 0 0 rgba(252, 231, 243, 1), 15px 225px 0 0 rgba(255, 205, 234, 1),
  20px 225px 0 0 rgba(255, 205, 234, 1), 25px 225px 0 0 rgba(203, 109, 181, 1),
  30px 225px 0 0 rgba(110, 205, 199, 1), 35px 225px 0 0 rgba(255, 255, 255, 1),
  40px 225px 0 0 rgba(110, 205, 199, 1), 45px 225px 0 0 rgba(255, 255, 255, 1),
  50px 225px 0 0 rgba(110, 205, 199, 1), 55px 225px 0 0 rgba(255, 255, 255, 1),
  60px 225px 0 0 rgba(110, 205, 199, 1), 65px 225px 0 0 rgba(255, 255, 255, 1),
  70px 225px 0 0 rgba(110, 205, 199, 1), 75px 225px 0 0 rgba(255, 255, 255, 1),
  80px 225px 0 0 rgba(110, 205, 199, 1), 85px 225px 0 0 rgba(255, 255, 255, 1),
  90px 225px 0 0 rgba(110, 205, 199, 1), 95px 225px 0 0 rgba(255, 255, 255, 1),
  100px 225px 0 0 rgba(110, 205, 199, 1), 105px 225px 0 0 rgba(255, 255, 255, 1),
  110px 225px 0 0 rgba(110, 205, 199, 1), 115px 225px 0 0 rgba(255, 255, 255, 1),
  120px 225px 0 0 rgba(110, 205, 199, 1), 125px 225px 0 0 rgba(255, 255, 255, 1),
  130px 225px 0 0 rgba(110, 205, 199, 1), 135px 225px 0 0 rgba(255, 255, 255, 1),
  140px 225px 0 0 rgba(110, 205, 199, 1), 145px 225px 0 0 rgba(255, 255, 255, 1),
  150px 225px 0 0 rgba(110, 205, 199, 1), 155px 225px 0 0 rgba(255, 255, 255, 1),
  160px 225px 0 0 rgba(110, 205, 199, 1), 165px 225px 0 0 rgba(255, 255, 255, 1),
  170px 225px 0 0 rgba(110, 205, 199, 1), 175px 225px 0 0 rgba(255, 255, 255, 1),
  180px 225px 0 0 rgba(110, 205, 199, 1), 185px 225px 0 0 rgba(255, 255, 255, 1),
  190px 225px 0 0 rgba(110, 205, 199, 1), 195px 225px 0 0 rgba(255, 255, 255, 1),
  200px 225px 0 0 rgba(110, 205, 199, 1), 205px 225px 0 0 rgba(255, 255, 255, 1),
  210px 225px 0 0 rgba(110, 205, 199, 1), 215px 225px 0 0 rgba(255, 255, 255, 1),
  220px 225px 0 0 rgba(110, 205, 199, 1), 225px 225px 0 0 rgba(255, 255, 255, 1),
  230px 225px 0 0 rgba(110, 205, 199, 1), 235px 225px 0 0 rgba(255, 255, 255, 1),
  240px 225px 0 0 rgba(110, 205, 199, 1), 245px 225px 0 0 rgba(255, 255, 255, 1),
  250px 225px 0 0 rgba(110, 205, 199, 1), 255px 225px 0 0 rgba(255, 255, 255, 1),
  260px 225px 0 0 rgba(110, 205, 199, 1), 265px 225px 0 0 rgba(255, 255, 255, 1),
  270px 225px 0 0 rgba(110, 205, 199, 1), 275px 225px 0 0 rgba(255, 255, 255, 1),
  280px 225px 0 0 rgba(110, 205, 199, 1), 285px 225px 0 0 rgba(255, 255, 255, 1),
  290px 225px 0 0 rgba(110, 205, 199, 1), 295px 225px 0 0 rgba(255, 255, 255, 1),
  300px 225px 0 0 rgba(110, 205, 199, 1), 305px 225px 0 0 rgba(255, 255, 255, 1),
  310px 225px 0 0 rgba(110, 205, 199, 1), 315px 225px 0 0 rgba(255, 255, 255, 1),
  320px 225px 0 0 rgba(110, 205, 199, 1), 325px 225px 0 0 rgba(255, 255, 255, 1),
  330px 225px 0 0 rgba(110, 205, 199, 1), 335px 225px 0 0 rgba(255, 255, 255, 1),
  340px 225px 0 0 rgba(110, 205, 199, 1), 345px 225px 0 0 rgba(255, 255, 255, 1),
  350px 225px 0 0 rgba(110, 205, 199, 1), 355px 225px 0 0 rgba(255, 255, 255, 1),
  360px 225px 0 0 rgba(110, 205, 199, 1), 365px 225px 0 0 rgba(255, 255, 255, 1),
  370px 225px 0 0 rgba(110, 205, 199, 1), 375px 225px 0 0 rgba(255, 255, 255, 1),
  380px 225px 0 0 rgba(110, 205, 199, 1), 385px 225px 0 0 rgba(255, 255, 255, 1),
  390px 225px 0 0 rgba(110, 205, 199, 1), 395px 225px 0 0 rgba(255, 255, 255, 1),
  400px 225px 0 0 rgba(110, 205, 199, 1), 405px 225px 0 0 rgba(255, 255, 255, 1),
  410px 225px 0 0 rgba(110, 205, 199, 1), 415px 225px 0 0 rgba(255, 255, 255, 1),
  420px 225px 0 0 rgba(110, 205, 199, 1), 425px 225px 0 0 rgba(255, 255, 255, 1),
  430px 225px 0 0 rgba(110, 205, 199, 1), 435px 225px 0 0 rgba(255, 255, 255, 1),
  440px 225px 0 0 rgba(110, 205, 199, 1), 445px 225px 0 0 rgba(255, 255, 255, 1),
  450px 225px 0 0 rgba(110, 205, 199, 1), 455px 225px 0 0 rgba(255, 255, 255, 1),
  460px 225px 0 0 rgba(110, 205, 199, 1), 465px 225px 0 0 rgba(255, 255, 255, 1),
  470px 225px 0 0 rgba(110, 205, 199, 1), 475px 225px 0 0 rgba(255, 255, 255, 1),
  480px 225px 0 0 rgba(110, 205, 199, 1), 485px 225px 0 0 rgba(255, 255, 255, 1),
  490px 225px 0 0 rgba(110, 205, 199, 1), 495px 225px 0 0 rgba(255, 255, 255, 1),
  500px 225px 0 0 rgba(110, 205, 199, 1), 505px 225px 0 0 rgba(255, 255, 255, 1),
  510px 225px 0 0 rgba(110, 205, 199, 1), 515px 225px 0 0 rgba(255, 255, 255, 1),
  520px 225px 0 0 rgba(110, 205, 199, 1), 525px 225px 0 0 rgba(255, 255, 255, 1),
  530px 225px 0 0 rgba(110, 205, 199, 1), 535px 225px 0 0 rgba(255, 255, 255, 1),
  540px 225px 0 0 rgba(110, 205, 199, 1), 545px 225px 0 0 rgba(255, 255, 255, 1),
  550px 225px 0 0 rgba(110, 205, 199, 1), 555px 225px 0 0 rgba(255, 255, 255, 1),
  560px 225px 0 0 rgba(110, 205, 199, 1), 565px 225px 0 0 rgba(255, 255, 255, 1),
  570px 225px 0 0 rgba(110, 205, 199, 1), 575px 225px 0 0 rgba(255, 255, 255, 1),
  580px 225px 0 0 rgba(110, 205, 199, 1), 585px 225px 0 0 rgba(255, 255, 255, 1),
  590px 225px 0 0 rgba(110, 205, 199, 1), 595px 225px 0 0 rgba(255, 255, 255, 1),
  600px 225px 0 0 rgba(110, 205, 199, 1), 605px 225px 0 0 rgba(255, 255, 255, 1),
  610px 225px 0 0 rgba(110, 205, 199, 1), 615px 225px 0 0 rgba(255, 255, 255, 1),
  620px 225px 0 0 rgba(110, 205, 199, 1), 625px 225px 0 0 rgba(255, 255, 255, 1),
  630px 225px 0 0 rgba(110, 205, 199, 1), 635px 225px 0 0 rgba(255, 255, 255, 1),
  640px 225px 0 0 rgba(110, 205, 199, 1), 645px 225px 0 0 rgba(255, 255, 255, 1),
  650px 225px 0 0 rgba(110, 205, 199, 1), 655px 225px 0 0 rgba(255, 255, 255, 1),
  660px 225px 0 0 rgba(110, 205, 199, 1), 665px 225px 0 0 rgba(255, 255, 255, 1),
  670px 225px 0 0 rgba(110, 205, 199, 1), 675px 225px 0 0 rgba(255, 255, 255, 1),
  680px 225px 0 0 rgba(110, 205, 199, 1), 685px 225px 0 0 rgba(203, 109, 181, 1),
  690px 225px 0 0 rgba(255, 205, 234, 1), 695px 225px 0 0 rgba(255, 205, 234, 1),
  700px 225px 0 0 rgba(168, 90, 150, 1), 705px 225px 0 0 rgba(203, 109, 181, 1),
  5px 230px 0 0 rgba(203, 109, 181, 1), 10px 230px 0 0 rgba(252, 231, 243, 1),
  15px 230px 0 0 rgba(255, 205, 234, 1), 20px 230px 0 0 rgba(255, 205, 234, 1),
  25px 230px 0 0 rgba(203, 109, 181, 1), 30px 230px 0 0 rgba(255, 255, 255, 1),
  35px 230px 0 0 rgba(255, 255, 255, 1), 40px 230px 0 0 rgba(255, 255, 255, 1),
  45px 230px 0 0 rgba(255, 255, 255, 1), 50px 230px 0 0 rgba(255, 255, 255, 1),
  55px 230px 0 0 rgba(255, 255, 255, 1), 60px 230px 0 0 rgba(255, 255, 255, 1),
  65px 230px 0 0 rgba(255, 255, 255, 1), 70px 230px 0 0 rgba(255, 255, 255, 1),
  75px 230px 0 0 rgba(255, 255, 255, 1), 80px 230px 0 0 rgba(255, 255, 255, 1),
  85px 230px 0 0 rgba(255, 255, 255, 1), 90px 230px 0 0 rgba(255, 255, 255, 1),
  95px 230px 0 0 rgba(255, 255, 255, 1), 100px 230px 0 0 rgba(255, 255, 255, 1),
  105px 230px 0 0 rgba(255, 255, 255, 1), 110px 230px 0 0 rgba(255, 255, 255, 1),
  115px 230px 0 0 rgba(255, 255, 255, 1), 120px 230px 0 0 rgba(255, 255, 255, 1),
  125px 230px 0 0 rgba(255, 255, 255, 1), 130px 230px 0 0 rgba(255, 255, 255, 1),
  135px 230px 0 0 rgba(255, 255, 255, 1), 140px 230px 0 0 rgba(255, 255, 255, 1),
  145px 230px 0 0 rgba(255, 255, 255, 1), 150px 230px 0 0 rgba(255, 255, 255, 1),
  155px 230px 0 0 rgba(255, 255, 255, 1), 160px 230px 0 0 rgba(255, 255, 255, 1),
  165px 230px 0 0 rgba(255, 255, 255, 1), 170px 230px 0 0 rgba(255, 255, 255, 1),
  175px 230px 0 0 rgba(255, 255, 255, 1), 180px 230px 0 0 rgba(255, 255, 255, 1),
  185px 230px 0 0 rgba(255, 255, 255, 1), 190px 230px 0 0 rgba(255, 255, 255, 1),
  195px 230px 0 0 rgba(255, 255, 255, 1), 200px 230px 0 0 rgba(255, 255, 255, 1),
  205px 230px 0 0 rgba(255, 255, 255, 1), 210px 230px 0 0 rgba(255, 255, 255, 1),
  215px 230px 0 0 rgba(255, 255, 255, 1), 220px 230px 0 0 rgba(255, 255, 255, 1),
  225px 230px 0 0 rgba(255, 255, 255, 1), 230px 230px 0 0 rgba(255, 255, 255, 1),
  235px 230px 0 0 rgba(255, 255, 255, 1), 240px 230px 0 0 rgba(255, 255, 255, 1),
  245px 230px 0 0 rgba(255, 255, 255, 1), 250px 230px 0 0 rgba(255, 255, 255, 1),
  255px 230px 0 0 rgba(255, 255, 255, 1), 260px 230px 0 0 rgba(255, 255, 255, 1),
  265px 230px 0 0 rgba(255, 255, 255, 1), 270px 230px 0 0 rgba(255, 255, 255, 1),
  275px 230px 0 0 rgba(255, 255, 255, 1), 280px 230px 0 0 rgba(255, 255, 255, 1),
  285px 230px 0 0 rgba(255, 255, 255, 1), 290px 230px 0 0 rgba(255, 255, 255, 1),
  295px 230px 0 0 rgba(255, 255, 255, 1), 300px 230px 0 0 rgba(255, 255, 255, 1),
  305px 230px 0 0 rgba(255, 255, 255, 1), 310px 230px 0 0 rgba(255, 255, 255, 1),
  315px 230px 0 0 rgba(255, 255, 255, 1), 320px 230px 0 0 rgba(255, 255, 255, 1),
  325px 230px 0 0 rgba(255, 255, 255, 1), 330px 230px 0 0 rgba(255, 255, 255, 1),
  335px 230px 0 0 rgba(255, 255, 255, 1), 340px 230px 0 0 rgba(255, 255, 255, 1),
  345px 230px 0 0 rgba(255, 255, 255, 1), 350px 230px 0 0 rgba(255, 255, 255, 1),
  355px 230px 0 0 rgba(255, 255, 255, 1), 360px 230px 0 0 rgba(255, 255, 255, 1),
  365px 230px 0 0 rgba(255, 255, 255, 1), 370px 230px 0 0 rgba(255, 255, 255, 1),
  375px 230px 0 0 rgba(255, 255, 255, 1), 380px 230px 0 0 rgba(255, 255, 255, 1),
  385px 230px 0 0 rgba(255, 255, 255, 1), 390px 230px 0 0 rgba(255, 255, 255, 1),
  395px 230px 0 0 rgba(255, 255, 255, 1), 400px 230px 0 0 rgba(255, 255, 255, 1),
  405px 230px 0 0 rgba(255, 255, 255, 1), 410px 230px 0 0 rgba(255, 255, 255, 1),
  415px 230px 0 0 rgba(255, 255, 255, 1), 420px 230px 0 0 rgba(255, 255, 255, 1),
  425px 230px 0 0 rgba(255, 255, 255, 1), 430px 230px 0 0 rgba(255, 255, 255, 1),
  435px 230px 0 0 rgba(255, 255, 255, 1), 440px 230px 0 0 rgba(255, 255, 255, 1),
  445px 230px 0 0 rgba(255, 255, 255, 1), 450px 230px 0 0 rgba(255, 255, 255, 1),
  455px 230px 0 0 rgba(255, 255, 255, 1), 460px 230px 0 0 rgba(255, 255, 255, 1),
  465px 230px 0 0 rgba(255, 255, 255, 1), 470px 230px 0 0 rgba(255, 255, 255, 1),
  475px 230px 0 0 rgba(255, 255, 255, 1), 480px 230px 0 0 rgba(255, 255, 255, 1),
  485px 230px 0 0 rgba(255, 255, 255, 1), 490px 230px 0 0 rgba(255, 255, 255, 1),
  495px 230px 0 0 rgba(255, 255, 255, 1), 500px 230px 0 0 rgba(255, 255, 255, 1),
  505px 230px 0 0 rgba(255, 255, 255, 1), 510px 230px 0 0 rgba(255, 255, 255, 1),
  515px 230px 0 0 rgba(255, 255, 255, 1), 520px 230px 0 0 rgba(255, 255, 255, 1),
  525px 230px 0 0 rgba(255, 255, 255, 1), 530px 230px 0 0 rgba(255, 255, 255, 1),
  535px 230px 0 0 rgba(255, 255, 255, 1), 540px 230px 0 0 rgba(255, 255, 255, 1),
  545px 230px 0 0 rgba(255, 255, 255, 1), 550px 230px 0 0 rgba(255, 255, 255, 1),
  555px 230px 0 0 rgba(255, 255, 255, 1), 560px 230px 0 0 rgba(255, 255, 255, 1),
  565px 230px 0 0 rgba(255, 255, 255, 1), 570px 230px 0 0 rgba(255, 255, 255, 1),
  575px 230px 0 0 rgba(255, 255, 255, 1), 580px 230px 0 0 rgba(255, 255, 255, 1),
  585px 230px 0 0 rgba(255, 255, 255, 1), 590px 230px 0 0 rgba(255, 255, 255, 1),
  595px 230px 0 0 rgba(255, 255, 255, 1), 600px 230px 0 0 rgba(255, 255, 255, 1),
  605px 230px 0 0 rgba(255, 255, 255, 1), 610px 230px 0 0 rgba(255, 255, 255, 1),
  615px 230px 0 0 rgba(255, 255, 255, 1), 620px 230px 0 0 rgba(255, 255, 255, 1),
  625px 230px 0 0 rgba(255, 255, 255, 1), 630px 230px 0 0 rgba(255, 255, 255, 1),
  635px 230px 0 0 rgba(255, 255, 255, 1), 640px 230px 0 0 rgba(255, 255, 255, 1),
  645px 230px 0 0 rgba(255, 255, 255, 1), 650px 230px 0 0 rgba(255, 255, 255, 1),
  655px 230px 0 0 rgba(255, 255, 255, 1), 660px 230px 0 0 rgba(255, 255, 255, 1),
  665px 230px 0 0 rgba(255, 255, 255, 1), 670px 230px 0 0 rgba(255, 255, 255, 1),
  675px 230px 0 0 rgba(255, 255, 255, 1), 680px 230px 0 0 rgba(255, 255, 255, 1),
  685px 230px 0 0 rgba(203, 109, 181, 1), 690px 230px 0 0 rgba(255, 205, 234, 1),
  695px 230px 0 0 rgba(255, 205, 234, 1), 700px 230px 0 0 rgba(168, 90, 150, 1),
  705px 230px 0 0 rgba(203, 109, 181, 1), 5px 235px 0 0 rgba(203, 109, 181, 1),
  10px 235px 0 0 rgba(252, 231, 243, 1), 15px 235px 0 0 rgba(255, 205, 234, 1),
  20px 235px 0 0 rgba(255, 205, 234, 1), 25px 235px 0 0 rgba(203, 109, 181, 1),
  30px 235px 0 0 rgba(110, 205, 199, 1), 35px 235px 0 0 rgba(255, 255, 255, 1),
  40px 235px 0 0 rgba(110, 205, 199, 1), 45px 235px 0 0 rgba(255, 255, 255, 1),
  50px 235px 0 0 rgba(110, 205, 199, 1), 55px 235px 0 0 rgba(255, 255, 255, 1),
  60px 235px 0 0 rgba(110, 205, 199, 1), 65px 235px 0 0 rgba(255, 255, 255, 1),
  70px 235px 0 0 rgba(110, 205, 199, 1), 75px 235px 0 0 rgba(255, 255, 255, 1),
  80px 235px 0 0 rgba(110, 205, 199, 1), 85px 235px 0 0 rgba(255, 255, 255, 1),
  90px 235px 0 0 rgba(110, 205, 199, 1), 95px 235px 0 0 rgba(255, 255, 255, 1),
  100px 235px 0 0 rgba(110, 205, 199, 1), 105px 235px 0 0 rgba(255, 255, 255, 1),
  110px 235px 0 0 rgba(110, 205, 199, 1), 115px 235px 0 0 rgba(255, 255, 255, 1),
  120px 235px 0 0 rgba(110, 205, 199, 1), 125px 235px 0 0 rgba(255, 255, 255, 1),
  130px 235px 0 0 rgba(110, 205, 199, 1), 135px 235px 0 0 rgba(255, 255, 255, 1),
  140px 235px 0 0 rgba(110, 205, 199, 1), 145px 235px 0 0 rgba(255, 255, 255, 1),
  150px 235px 0 0 rgba(110, 205, 199, 1), 155px 235px 0 0 rgba(255, 255, 255, 1),
  160px 235px 0 0 rgba(110, 205, 199, 1), 165px 235px 0 0 rgba(255, 255, 255, 1),
  170px 235px 0 0 rgba(110, 205, 199, 1), 175px 235px 0 0 rgba(255, 255, 255, 1),
  180px 235px 0 0 rgba(110, 205, 199, 1), 185px 235px 0 0 rgba(255, 255, 255, 1),
  190px 235px 0 0 rgba(110, 205, 199, 1), 195px 235px 0 0 rgba(255, 255, 255, 1),
  200px 235px 0 0 rgba(110, 205, 199, 1), 205px 235px 0 0 rgba(255, 255, 255, 1),
  210px 235px 0 0 rgba(110, 205, 199, 1), 215px 235px 0 0 rgba(255, 255, 255, 1),
  220px 235px 0 0 rgba(110, 205, 199, 1), 225px 235px 0 0 rgba(255, 255, 255, 1),
  230px 235px 0 0 rgba(110, 205, 199, 1), 235px 235px 0 0 rgba(255, 255, 255, 1),
  240px 235px 0 0 rgba(110, 205, 199, 1), 245px 235px 0 0 rgba(255, 255, 255, 1),
  250px 235px 0 0 rgba(110, 205, 199, 1), 255px 235px 0 0 rgba(255, 255, 255, 1),
  260px 235px 0 0 rgba(110, 205, 199, 1), 265px 235px 0 0 rgba(255, 255, 255, 1),
  270px 235px 0 0 rgba(110, 205, 199, 1), 275px 235px 0 0 rgba(255, 255, 255, 1),
  280px 235px 0 0 rgba(110, 205, 199, 1), 285px 235px 0 0 rgba(255, 255, 255, 1),
  290px 235px 0 0 rgba(110, 205, 199, 1), 295px 235px 0 0 rgba(255, 255, 255, 1),
  300px 235px 0 0 rgba(110, 205, 199, 1), 305px 235px 0 0 rgba(255, 255, 255, 1),
  310px 235px 0 0 rgba(110, 205, 199, 1), 315px 235px 0 0 rgba(255, 255, 255, 1),
  320px 235px 0 0 rgba(110, 205, 199, 1), 325px 235px 0 0 rgba(255, 255, 255, 1),
  330px 235px 0 0 rgba(110, 205, 199, 1), 335px 235px 0 0 rgba(255, 255, 255, 1),
  340px 235px 0 0 rgba(110, 205, 199, 1), 345px 235px 0 0 rgba(255, 255, 255, 1),
  350px 235px 0 0 rgba(110, 205, 199, 1), 355px 235px 0 0 rgba(255, 255, 255, 1),
  360px 235px 0 0 rgba(110, 205, 199, 1), 365px 235px 0 0 rgba(255, 255, 255, 1),
  370px 235px 0 0 rgba(110, 205, 199, 1), 375px 235px 0 0 rgba(255, 255, 255, 1),
  380px 235px 0 0 rgba(110, 205, 199, 1), 385px 235px 0 0 rgba(255, 255, 255, 1),
  390px 235px 0 0 rgba(110, 205, 199, 1), 395px 235px 0 0 rgba(255, 255, 255, 1),
  400px 235px 0 0 rgba(110, 205, 199, 1), 405px 235px 0 0 rgba(255, 255, 255, 1),
  410px 235px 0 0 rgba(110, 205, 199, 1), 415px 235px 0 0 rgba(255, 255, 255, 1),
  420px 235px 0 0 rgba(110, 205, 199, 1), 425px 235px 0 0 rgba(255, 255, 255, 1),
  430px 235px 0 0 rgba(110, 205, 199, 1), 435px 235px 0 0 rgba(255, 255, 255, 1),
  440px 235px 0 0 rgba(110, 205, 199, 1), 445px 235px 0 0 rgba(255, 255, 255, 1),
  450px 235px 0 0 rgba(110, 205, 199, 1), 455px 235px 0 0 rgba(255, 255, 255, 1),
  460px 235px 0 0 rgba(110, 205, 199, 1), 465px 235px 0 0 rgba(255, 255, 255, 1),
  470px 235px 0 0 rgba(110, 205, 199, 1), 475px 235px 0 0 rgba(255, 255, 255, 1),
  480px 235px 0 0 rgba(110, 205, 199, 1), 485px 235px 0 0 rgba(255, 255, 255, 1),
  490px 235px 0 0 rgba(110, 205, 199, 1), 495px 235px 0 0 rgba(255, 255, 255, 1),
  500px 235px 0 0 rgba(110, 205, 199, 1), 505px 235px 0 0 rgba(255, 255, 255, 1),
  510px 235px 0 0 rgba(110, 205, 199, 1), 515px 235px 0 0 rgba(255, 255, 255, 1),
  520px 235px 0 0 rgba(110, 205, 199, 1), 525px 235px 0 0 rgba(255, 255, 255, 1),
  530px 235px 0 0 rgba(110, 205, 199, 1), 535px 235px 0 0 rgba(255, 255, 255, 1),
  540px 235px 0 0 rgba(110, 205, 199, 1), 545px 235px 0 0 rgba(255, 255, 255, 1),
  550px 235px 0 0 rgba(110, 205, 199, 1), 555px 235px 0 0 rgba(255, 255, 255, 1),
  560px 235px 0 0 rgba(110, 205, 199, 1), 565px 235px 0 0 rgba(255, 255, 255, 1),
  570px 235px 0 0 rgba(110, 205, 199, 1), 575px 235px 0 0 rgba(255, 255, 255, 1),
  580px 235px 0 0 rgba(110, 205, 199, 1), 585px 235px 0 0 rgba(255, 255, 255, 1),
  590px 235px 0 0 rgba(110, 205, 199, 1), 595px 235px 0 0 rgba(255, 255, 255, 1),
  600px 235px 0 0 rgba(110, 205, 199, 1), 605px 235px 0 0 rgba(255, 255, 255, 1),
  610px 235px 0 0 rgba(110, 205, 199, 1), 615px 235px 0 0 rgba(255, 255, 255, 1),
  620px 235px 0 0 rgba(110, 205, 199, 1), 625px 235px 0 0 rgba(255, 255, 255, 1),
  630px 235px 0 0 rgba(110, 205, 199, 1), 635px 235px 0 0 rgba(255, 255, 255, 1),
  640px 235px 0 0 rgba(110, 205, 199, 1), 645px 235px 0 0 rgba(255, 255, 255, 1),
  650px 235px 0 0 rgba(110, 205, 199, 1), 655px 235px 0 0 rgba(255, 255, 255, 1),
  660px 235px 0 0 rgba(110, 205, 199, 1), 665px 235px 0 0 rgba(255, 255, 255, 1),
  670px 235px 0 0 rgba(110, 205, 199, 1), 675px 235px 0 0 rgba(255, 255, 255, 1),
  680px 235px 0 0 rgba(110, 205, 199, 1), 685px 235px 0 0 rgba(203, 109, 181, 1),
  690px 235px 0 0 rgba(255, 205, 234, 1), 695px 235px 0 0 rgba(255, 205, 234, 1),
  700px 235px 0 0 rgba(168, 90, 150, 1), 705px 235px 0 0 rgba(203, 109, 181, 1),
  5px 240px 0 0 rgba(203, 109, 181, 1), 10px 240px 0 0 rgba(252, 231, 243, 1),
  15px 240px 0 0 rgba(255, 205, 234, 1), 20px 240px 0 0 rgba(255, 205, 234, 1),
  25px 240px 0 0 rgba(203, 109, 181, 1), 30px 240px 0 0 rgba(255, 255, 255, 1),
  35px 240px 0 0 rgba(255, 255, 255, 1), 40px 240px 0 0 rgba(255, 255, 255, 1),
  45px 240px 0 0 rgba(255, 255, 255, 1), 50px 240px 0 0 rgba(255, 255, 255, 1),
  55px 240px 0 0 rgba(255, 255, 255, 1), 60px 240px 0 0 rgba(255, 255, 255, 1),
  65px 240px 0 0 rgba(255, 255, 255, 1), 70px 240px 0 0 rgba(255, 255, 255, 1),
  75px 240px 0 0 rgba(255, 255, 255, 1), 80px 240px 0 0 rgba(255, 255, 255, 1),
  85px 240px 0 0 rgba(255, 255, 255, 1), 90px 240px 0 0 rgba(255, 255, 255, 1),
  95px 240px 0 0 rgba(255, 255, 255, 1), 100px 240px 0 0 rgba(255, 255, 255, 1),
  105px 240px 0 0 rgba(255, 255, 255, 1), 110px 240px 0 0 rgba(255, 255, 255, 1),
  115px 240px 0 0 rgba(255, 255, 255, 1), 120px 240px 0 0 rgba(255, 255, 255, 1),
  125px 240px 0 0 rgba(255, 255, 255, 1), 130px 240px 0 0 rgba(255, 255, 255, 1),
  135px 240px 0 0 rgba(255, 255, 255, 1), 140px 240px 0 0 rgba(255, 255, 255, 1),
  145px 240px 0 0 rgba(255, 255, 255, 1), 150px 240px 0 0 rgba(255, 255, 255, 1),
  155px 240px 0 0 rgba(255, 255, 255, 1), 160px 240px 0 0 rgba(255, 255, 255, 1),
  165px 240px 0 0 rgba(255, 255, 255, 1), 170px 240px 0 0 rgba(255, 255, 255, 1),
  175px 240px 0 0 rgba(255, 255, 255, 1), 180px 240px 0 0 rgba(255, 255, 255, 1),
  185px 240px 0 0 rgba(255, 255, 255, 1), 190px 240px 0 0 rgba(255, 255, 255, 1),
  195px 240px 0 0 rgba(255, 255, 255, 1), 200px 240px 0 0 rgba(255, 255, 255, 1),
  205px 240px 0 0 rgba(255, 255, 255, 1), 210px 240px 0 0 rgba(255, 255, 255, 1),
  215px 240px 0 0 rgba(255, 255, 255, 1), 220px 240px 0 0 rgba(255, 255, 255, 1),
  225px 240px 0 0 rgba(255, 255, 255, 1), 230px 240px 0 0 rgba(255, 255, 255, 1),
  235px 240px 0 0 rgba(255, 255, 255, 1), 240px 240px 0 0 rgba(255, 255, 255, 1),
  245px 240px 0 0 rgba(255, 255, 255, 1), 250px 240px 0 0 rgba(255, 255, 255, 1),
  255px 240px 0 0 rgba(255, 255, 255, 1), 260px 240px 0 0 rgba(255, 255, 255, 1),
  265px 240px 0 0 rgba(255, 255, 255, 1), 270px 240px 0 0 rgba(255, 255, 255, 1),
  275px 240px 0 0 rgba(255, 255, 255, 1), 280px 240px 0 0 rgba(255, 255, 255, 1),
  285px 240px 0 0 rgba(255, 255, 255, 1), 290px 240px 0 0 rgba(255, 255, 255, 1),
  295px 240px 0 0 rgba(255, 255, 255, 1), 300px 240px 0 0 rgba(255, 255, 255, 1),
  305px 240px 0 0 rgba(255, 255, 255, 1), 310px 240px 0 0 rgba(255, 255, 255, 1),
  315px 240px 0 0 rgba(255, 255, 255, 1), 320px 240px 0 0 rgba(255, 255, 255, 1),
  325px 240px 0 0 rgba(255, 255, 255, 1), 330px 240px 0 0 rgba(255, 255, 255, 1),
  335px 240px 0 0 rgba(255, 255, 255, 1), 340px 240px 0 0 rgba(255, 255, 255, 1),
  345px 240px 0 0 rgba(255, 255, 255, 1), 350px 240px 0 0 rgba(255, 255, 255, 1),
  355px 240px 0 0 rgba(255, 255, 255, 1), 360px 240px 0 0 rgba(255, 255, 255, 1),
  365px 240px 0 0 rgba(255, 255, 255, 1), 370px 240px 0 0 rgba(255, 255, 255, 1),
  375px 240px 0 0 rgba(255, 255, 255, 1), 380px 240px 0 0 rgba(255, 255, 255, 1),
  385px 240px 0 0 rgba(255, 255, 255, 1), 390px 240px 0 0 rgba(255, 255, 255, 1),
  395px 240px 0 0 rgba(255, 255, 255, 1), 400px 240px 0 0 rgba(255, 255, 255, 1),
  405px 240px 0 0 rgba(255, 255, 255, 1), 410px 240px 0 0 rgba(255, 255, 255, 1),
  415px 240px 0 0 rgba(255, 255, 255, 1), 420px 240px 0 0 rgba(255, 255, 255, 1),
  425px 240px 0 0 rgba(255, 255, 255, 1), 430px 240px 0 0 rgba(255, 255, 255, 1),
  435px 240px 0 0 rgba(255, 255, 255, 1), 440px 240px 0 0 rgba(255, 255, 255, 1),
  445px 240px 0 0 rgba(255, 255, 255, 1), 450px 240px 0 0 rgba(255, 255, 255, 1),
  455px 240px 0 0 rgba(255, 255, 255, 1), 460px 240px 0 0 rgba(255, 255, 255, 1),
  465px 240px 0 0 rgba(255, 255, 255, 1), 470px 240px 0 0 rgba(255, 255, 255, 1),
  475px 240px 0 0 rgba(255, 255, 255, 1), 480px 240px 0 0 rgba(255, 255, 255, 1),
  485px 240px 0 0 rgba(255, 255, 255, 1), 490px 240px 0 0 rgba(255, 255, 255, 1),
  495px 240px 0 0 rgba(255, 255, 255, 1), 500px 240px 0 0 rgba(255, 255, 255, 1),
  505px 240px 0 0 rgba(255, 255, 255, 1), 510px 240px 0 0 rgba(255, 255, 255, 1),
  515px 240px 0 0 rgba(255, 255, 255, 1), 520px 240px 0 0 rgba(255, 255, 255, 1),
  525px 240px 0 0 rgba(255, 255, 255, 1), 530px 240px 0 0 rgba(255, 255, 255, 1),
  535px 240px 0 0 rgba(255, 255, 255, 1), 540px 240px 0 0 rgba(255, 255, 255, 1),
  545px 240px 0 0 rgba(255, 255, 255, 1), 550px 240px 0 0 rgba(255, 255, 255, 1),
  555px 240px 0 0 rgba(255, 255, 255, 1), 560px 240px 0 0 rgba(255, 255, 255, 1),
  565px 240px 0 0 rgba(255, 255, 255, 1), 570px 240px 0 0 rgba(255, 255, 255, 1),
  575px 240px 0 0 rgba(255, 255, 255, 1), 580px 240px 0 0 rgba(255, 255, 255, 1),
  585px 240px 0 0 rgba(255, 255, 255, 1), 590px 240px 0 0 rgba(255, 255, 255, 1),
  595px 240px 0 0 rgba(255, 255, 255, 1), 600px 240px 0 0 rgba(255, 255, 255, 1),
  605px 240px 0 0 rgba(255, 255, 255, 1), 610px 240px 0 0 rgba(255, 255, 255, 1),
  615px 240px 0 0 rgba(255, 255, 255, 1), 620px 240px 0 0 rgba(255, 255, 255, 1),
  625px 240px 0 0 rgba(255, 255, 255, 1), 630px 240px 0 0 rgba(255, 255, 255, 1),
  635px 240px 0 0 rgba(255, 255, 255, 1), 640px 240px 0 0 rgba(255, 255, 255, 1),
  645px 240px 0 0 rgba(255, 255, 255, 1), 650px 240px 0 0 rgba(255, 255, 255, 1),
  655px 240px 0 0 rgba(255, 255, 255, 1), 660px 240px 0 0 rgba(255, 255, 255, 1),
  665px 240px 0 0 rgba(255, 255, 255, 1), 670px 240px 0 0 rgba(255, 255, 255, 1),
  675px 240px 0 0 rgba(255, 255, 255, 1), 680px 240px 0 0 rgba(255, 255, 255, 1),
  685px 240px 0 0 rgba(203, 109, 181, 1), 690px 240px 0 0 rgba(255, 205, 234, 1),
  695px 240px 0 0 rgba(255, 205, 234, 1), 700px 240px 0 0 rgba(168, 90, 150, 1),
  705px 240px 0 0 rgba(203, 109, 181, 1), 5px 245px 0 0 rgba(203, 109, 181, 1),
  10px 245px 0 0 rgba(252, 231, 243, 1), 15px 245px 0 0 rgba(255, 205, 234, 1),
  20px 245px 0 0 rgba(255, 205, 234, 1), 25px 245px 0 0 rgba(203, 109, 181, 1),
  30px 245px 0 0 rgba(255, 255, 255, 1), 35px 245px 0 0 rgba(255, 255, 255, 1),
  40px 245px 0 0 rgba(110, 205, 199, 1), 45px 245px 0 0 rgba(255, 255, 255, 1),
  50px 245px 0 0 rgba(255, 255, 255, 1), 55px 245px 0 0 rgba(255, 255, 255, 1),
  60px 245px 0 0 rgba(110, 205, 199, 1), 65px 245px 0 0 rgba(255, 255, 255, 1),
  70px 245px 0 0 rgba(255, 255, 255, 1), 75px 245px 0 0 rgba(255, 255, 255, 1),
  80px 245px 0 0 rgba(110, 205, 199, 1), 85px 245px 0 0 rgba(255, 255, 255, 1),
  90px 245px 0 0 rgba(255, 255, 255, 1), 95px 245px 0 0 rgba(255, 255, 255, 1),
  100px 245px 0 0 rgba(110, 205, 199, 1), 105px 245px 0 0 rgba(255, 255, 255, 1),
  110px 245px 0 0 rgba(255, 255, 255, 1), 115px 245px 0 0 rgba(255, 255, 255, 1),
  120px 245px 0 0 rgba(110, 205, 199, 1), 125px 245px 0 0 rgba(255, 255, 255, 1),
  130px 245px 0 0 rgba(255, 255, 255, 1), 135px 245px 0 0 rgba(255, 255, 255, 1),
  140px 245px 0 0 rgba(110, 205, 199, 1), 145px 245px 0 0 rgba(255, 255, 255, 1),
  150px 245px 0 0 rgba(255, 255, 255, 1), 155px 245px 0 0 rgba(255, 255, 255, 1),
  160px 245px 0 0 rgba(110, 205, 199, 1), 165px 245px 0 0 rgba(255, 255, 255, 1),
  170px 245px 0 0 rgba(255, 255, 255, 1), 175px 245px 0 0 rgba(255, 255, 255, 1),
  180px 245px 0 0 rgba(110, 205, 199, 1), 185px 245px 0 0 rgba(255, 255, 255, 1),
  190px 245px 0 0 rgba(255, 255, 255, 1), 195px 245px 0 0 rgba(255, 255, 255, 1),
  200px 245px 0 0 rgba(110, 205, 199, 1), 205px 245px 0 0 rgba(255, 255, 255, 1),
  210px 245px 0 0 rgba(255, 255, 255, 1), 215px 245px 0 0 rgba(255, 255, 255, 1),
  220px 245px 0 0 rgba(110, 205, 199, 1), 225px 245px 0 0 rgba(255, 255, 255, 1),
  230px 245px 0 0 rgba(255, 255, 255, 1), 235px 245px 0 0 rgba(255, 255, 255, 1),
  240px 245px 0 0 rgba(110, 205, 199, 1), 245px 245px 0 0 rgba(255, 255, 255, 1),
  250px 245px 0 0 rgba(255, 255, 255, 1), 255px 245px 0 0 rgba(255, 255, 255, 1),
  260px 245px 0 0 rgba(110, 205, 199, 1), 265px 245px 0 0 rgba(255, 255, 255, 1),
  270px 245px 0 0 rgba(255, 255, 255, 1), 275px 245px 0 0 rgba(255, 255, 255, 1),
  280px 245px 0 0 rgba(110, 205, 199, 1), 285px 245px 0 0 rgba(255, 255, 255, 1),
  290px 245px 0 0 rgba(255, 255, 255, 1), 295px 245px 0 0 rgba(255, 255, 255, 1),
  300px 245px 0 0 rgba(110, 205, 199, 1), 305px 245px 0 0 rgba(255, 255, 255, 1),
  310px 245px 0 0 rgba(255, 255, 255, 1), 315px 245px 0 0 rgba(255, 255, 255, 1),
  320px 245px 0 0 rgba(110, 205, 199, 1), 325px 245px 0 0 rgba(255, 255, 255, 1),
  330px 245px 0 0 rgba(255, 255, 255, 1), 335px 245px 0 0 rgba(255, 255, 255, 1),
  340px 245px 0 0 rgba(110, 205, 199, 1), 345px 245px 0 0 rgba(255, 255, 255, 1),
  350px 245px 0 0 rgba(255, 255, 255, 1), 355px 245px 0 0 rgba(255, 255, 255, 1),
  360px 245px 0 0 rgba(110, 205, 199, 1), 365px 245px 0 0 rgba(255, 255, 255, 1),
  370px 245px 0 0 rgba(255, 255, 255, 1), 375px 245px 0 0 rgba(255, 255, 255, 1),
  380px 245px 0 0 rgba(110, 205, 199, 1), 385px 245px 0 0 rgba(255, 255, 255, 1),
  390px 245px 0 0 rgba(255, 255, 255, 1), 395px 245px 0 0 rgba(255, 255, 255, 1),
  400px 245px 0 0 rgba(110, 205, 199, 1), 405px 245px 0 0 rgba(255, 255, 255, 1),
  410px 245px 0 0 rgba(255, 255, 255, 1), 415px 245px 0 0 rgba(255, 255, 255, 1),
  420px 245px 0 0 rgba(110, 205, 199, 1), 425px 245px 0 0 rgba(255, 255, 255, 1),
  430px 245px 0 0 rgba(255, 255, 255, 1), 435px 245px 0 0 rgba(255, 255, 255, 1),
  440px 245px 0 0 rgba(110, 205, 199, 1), 445px 245px 0 0 rgba(255, 255, 255, 1),
  450px 245px 0 0 rgba(255, 255, 255, 1), 455px 245px 0 0 rgba(255, 255, 255, 1),
  460px 245px 0 0 rgba(110, 205, 199, 1), 465px 245px 0 0 rgba(255, 255, 255, 1),
  470px 245px 0 0 rgba(255, 255, 255, 1), 475px 245px 0 0 rgba(255, 255, 255, 1),
  480px 245px 0 0 rgba(110, 205, 199, 1), 485px 245px 0 0 rgba(255, 255, 255, 1),
  490px 245px 0 0 rgba(255, 255, 255, 1), 495px 245px 0 0 rgba(255, 255, 255, 1),
  500px 245px 0 0 rgba(110, 205, 199, 1), 505px 245px 0 0 rgba(255, 255, 255, 1),
  510px 245px 0 0 rgba(255, 255, 255, 1), 515px 245px 0 0 rgba(255, 255, 255, 1),
  520px 245px 0 0 rgba(110, 205, 199, 1), 525px 245px 0 0 rgba(255, 255, 255, 1),
  530px 245px 0 0 rgba(255, 255, 255, 1), 535px 245px 0 0 rgba(255, 255, 255, 1),
  540px 245px 0 0 rgba(110, 205, 199, 1), 545px 245px 0 0 rgba(255, 255, 255, 1),
  550px 245px 0 0 rgba(255, 255, 255, 1), 555px 245px 0 0 rgba(255, 255, 255, 1),
  560px 245px 0 0 rgba(110, 205, 199, 1), 565px 245px 0 0 rgba(255, 255, 255, 1),
  570px 245px 0 0 rgba(255, 255, 255, 1), 575px 245px 0 0 rgba(255, 255, 255, 1),
  580px 245px 0 0 rgba(110, 205, 199, 1), 585px 245px 0 0 rgba(255, 255, 255, 1),
  590px 245px 0 0 rgba(255, 255, 255, 1), 595px 245px 0 0 rgba(255, 255, 255, 1),
  600px 245px 0 0 rgba(110, 205, 199, 1), 605px 245px 0 0 rgba(255, 255, 255, 1),
  610px 245px 0 0 rgba(255, 255, 255, 1), 615px 245px 0 0 rgba(255, 255, 255, 1),
  620px 245px 0 0 rgba(110, 205, 199, 1), 625px 245px 0 0 rgba(255, 255, 255, 1),
  630px 245px 0 0 rgba(255, 255, 255, 1), 635px 245px 0 0 rgba(255, 255, 255, 1),
  640px 245px 0 0 rgba(110, 205, 199, 1), 645px 245px 0 0 rgba(255, 255, 255, 1),
  650px 245px 0 0 rgba(255, 255, 255, 1), 655px 245px 0 0 rgba(255, 255, 255, 1),
  660px 245px 0 0 rgba(110, 205, 199, 1), 665px 245px 0 0 rgba(255, 255, 255, 1),
  670px 245px 0 0 rgba(255, 255, 255, 1), 675px 245px 0 0 rgba(255, 255, 255, 1),
  680px 245px 0 0 rgba(110, 205, 199, 1), 685px 245px 0 0 rgba(203, 109, 181, 1),
  690px 245px 0 0 rgba(255, 205, 234, 1), 695px 245px 0 0 rgba(255, 205, 234, 1),
  700px 245px 0 0 rgba(168, 90, 150, 1), 705px 245px 0 0 rgba(203, 109, 181, 1),
  5px 250px 0 0 rgba(203, 109, 181, 1), 10px 250px 0 0 rgba(252, 231, 243, 1),
  15px 250px 0 0 rgba(255, 205, 234, 1), 20px 250px 0 0 rgba(255, 205, 234, 1),
  25px 250px 0 0 rgba(203, 109, 181, 1), 30px 250px 0 0 rgba(255, 255, 255, 1),
  35px 250px 0 0 rgba(255, 255, 255, 1), 40px 250px 0 0 rgba(255, 255, 255, 1),
  45px 250px 0 0 rgba(255, 255, 255, 1), 50px 250px 0 0 rgba(255, 255, 255, 1),
  55px 250px 0 0 rgba(255, 255, 255, 1), 60px 250px 0 0 rgba(255, 255, 255, 1),
  65px 250px 0 0 rgba(255, 255, 255, 1), 70px 250px 0 0 rgba(255, 255, 255, 1),
  75px 250px 0 0 rgba(255, 255, 255, 1), 80px 250px 0 0 rgba(255, 255, 255, 1),
  85px 250px 0 0 rgba(255, 255, 255, 1), 90px 250px 0 0 rgba(255, 255, 255, 1),
  95px 250px 0 0 rgba(255, 255, 255, 1), 100px 250px 0 0 rgba(255, 255, 255, 1),
  105px 250px 0 0 rgba(255, 255, 255, 1), 110px 250px 0 0 rgba(255, 255, 255, 1),
  115px 250px 0 0 rgba(255, 255, 255, 1), 120px 250px 0 0 rgba(255, 255, 255, 1),
  125px 250px 0 0 rgba(255, 255, 255, 1), 130px 250px 0 0 rgba(255, 255, 255, 1),
  135px 250px 0 0 rgba(255, 255, 255, 1), 140px 250px 0 0 rgba(255, 255, 255, 1),
  145px 250px 0 0 rgba(255, 255, 255, 1), 150px 250px 0 0 rgba(255, 255, 255, 1),
  155px 250px 0 0 rgba(255, 255, 255, 1), 160px 250px 0 0 rgba(255, 255, 255, 1),
  165px 250px 0 0 rgba(255, 255, 255, 1), 170px 250px 0 0 rgba(255, 255, 255, 1),
  175px 250px 0 0 rgba(255, 255, 255, 1), 180px 250px 0 0 rgba(255, 255, 255, 1),
  185px 250px 0 0 rgba(255, 255, 255, 1), 190px 250px 0 0 rgba(255, 255, 255, 1),
  195px 250px 0 0 rgba(255, 255, 255, 1), 200px 250px 0 0 rgba(255, 255, 255, 1),
  205px 250px 0 0 rgba(255, 255, 255, 1), 210px 250px 0 0 rgba(255, 255, 255, 1),
  215px 250px 0 0 rgba(255, 255, 255, 1), 220px 250px 0 0 rgba(255, 255, 255, 1),
  225px 250px 0 0 rgba(255, 255, 255, 1), 230px 250px 0 0 rgba(255, 255, 255, 1),
  235px 250px 0 0 rgba(255, 255, 255, 1), 240px 250px 0 0 rgba(255, 255, 255, 1),
  245px 250px 0 0 rgba(255, 255, 255, 1), 250px 250px 0 0 rgba(255, 255, 255, 1),
  255px 250px 0 0 rgba(255, 255, 255, 1), 260px 250px 0 0 rgba(255, 255, 255, 1),
  265px 250px 0 0 rgba(255, 255, 255, 1), 270px 250px 0 0 rgba(255, 255, 255, 1),
  275px 250px 0 0 rgba(255, 255, 255, 1), 280px 250px 0 0 rgba(255, 255, 255, 1),
  285px 250px 0 0 rgba(255, 255, 255, 1), 290px 250px 0 0 rgba(255, 255, 255, 1),
  295px 250px 0 0 rgba(255, 255, 255, 1), 300px 250px 0 0 rgba(255, 255, 255, 1),
  305px 250px 0 0 rgba(255, 255, 255, 1), 310px 250px 0 0 rgba(255, 255, 255, 1),
  315px 250px 0 0 rgba(255, 255, 255, 1), 320px 250px 0 0 rgba(255, 255, 255, 1),
  325px 250px 0 0 rgba(255, 255, 255, 1), 330px 250px 0 0 rgba(255, 255, 255, 1),
  335px 250px 0 0 rgba(255, 255, 255, 1), 340px 250px 0 0 rgba(255, 255, 255, 1),
  345px 250px 0 0 rgba(255, 255, 255, 1), 350px 250px 0 0 rgba(255, 255, 255, 1),
  355px 250px 0 0 rgba(255, 255, 255, 1), 360px 250px 0 0 rgba(255, 255, 255, 1),
  365px 250px 0 0 rgba(255, 255, 255, 1), 370px 250px 0 0 rgba(255, 255, 255, 1),
  375px 250px 0 0 rgba(255, 255, 255, 1), 380px 250px 0 0 rgba(255, 255, 255, 1),
  385px 250px 0 0 rgba(255, 255, 255, 1), 390px 250px 0 0 rgba(255, 255, 255, 1),
  395px 250px 0 0 rgba(255, 255, 255, 1), 400px 250px 0 0 rgba(255, 255, 255, 1),
  405px 250px 0 0 rgba(255, 255, 255, 1), 410px 250px 0 0 rgba(255, 255, 255, 1),
  415px 250px 0 0 rgba(255, 255, 255, 1), 420px 250px 0 0 rgba(255, 255, 255, 1),
  425px 250px 0 0 rgba(255, 255, 255, 1), 430px 250px 0 0 rgba(255, 255, 255, 1),
  435px 250px 0 0 rgba(255, 255, 255, 1), 440px 250px 0 0 rgba(255, 255, 255, 1),
  445px 250px 0 0 rgba(255, 255, 255, 1), 450px 250px 0 0 rgba(255, 255, 255, 1),
  455px 250px 0 0 rgba(255, 255, 255, 1), 460px 250px 0 0 rgba(255, 255, 255, 1),
  465px 250px 0 0 rgba(255, 255, 255, 1), 470px 250px 0 0 rgba(255, 255, 255, 1),
  475px 250px 0 0 rgba(255, 255, 255, 1), 480px 250px 0 0 rgba(255, 255, 255, 1),
  485px 250px 0 0 rgba(255, 255, 255, 1), 490px 250px 0 0 rgba(255, 255, 255, 1),
  495px 250px 0 0 rgba(255, 255, 255, 1), 500px 250px 0 0 rgba(255, 255, 255, 1),
  505px 250px 0 0 rgba(255, 255, 255, 1), 510px 250px 0 0 rgba(255, 255, 255, 1),
  515px 250px 0 0 rgba(255, 255, 255, 1), 520px 250px 0 0 rgba(255, 255, 255, 1),
  525px 250px 0 0 rgba(255, 255, 255, 1), 530px 250px 0 0 rgba(255, 255, 255, 1),
  535px 250px 0 0 rgba(255, 255, 255, 1), 540px 250px 0 0 rgba(255, 255, 255, 1),
  545px 250px 0 0 rgba(255, 255, 255, 1), 550px 250px 0 0 rgba(255, 255, 255, 1),
  555px 250px 0 0 rgba(255, 255, 255, 1), 560px 250px 0 0 rgba(255, 255, 255, 1),
  565px 250px 0 0 rgba(255, 255, 255, 1), 570px 250px 0 0 rgba(255, 255, 255, 1),
  575px 250px 0 0 rgba(255, 255, 255, 1), 580px 250px 0 0 rgba(255, 255, 255, 1),
  585px 250px 0 0 rgba(255, 255, 255, 1), 590px 250px 0 0 rgba(255, 255, 255, 1),
  595px 250px 0 0 rgba(255, 255, 255, 1), 600px 250px 0 0 rgba(255, 255, 255, 1),
  605px 250px 0 0 rgba(255, 255, 255, 1), 610px 250px 0 0 rgba(255, 255, 255, 1),
  615px 250px 0 0 rgba(255, 255, 255, 1), 620px 250px 0 0 rgba(255, 255, 255, 1),
  625px 250px 0 0 rgba(255, 255, 255, 1), 630px 250px 0 0 rgba(255, 255, 255, 1),
  635px 250px 0 0 rgba(255, 255, 255, 1), 640px 250px 0 0 rgba(255, 255, 255, 1),
  645px 250px 0 0 rgba(255, 255, 255, 1), 650px 250px 0 0 rgba(255, 255, 255, 1),
  655px 250px 0 0 rgba(255, 255, 255, 1), 660px 250px 0 0 rgba(255, 255, 255, 1),
  665px 250px 0 0 rgba(255, 255, 255, 1), 670px 250px 0 0 rgba(255, 255, 255, 1),
  675px 250px 0 0 rgba(255, 255, 255, 1), 680px 250px 0 0 rgba(255, 255, 255, 1),
  685px 250px 0 0 rgba(203, 109, 181, 1), 690px 250px 0 0 rgba(255, 205, 234, 1),
  695px 250px 0 0 rgba(255, 205, 234, 1), 700px 250px 0 0 rgba(168, 90, 150, 1),
  705px 250px 0 0 rgba(203, 109, 181, 1), 5px 255px 0 0 rgba(203, 109, 181, 1),
  10px 255px 0 0 rgba(252, 231, 243, 1), 15px 255px 0 0 rgba(255, 205, 234, 1),
  20px 255px 0 0 rgba(255, 205, 234, 1), 25px 255px 0 0 rgba(203, 109, 181, 1),
  30px 255px 0 0 rgba(110, 205, 199, 1), 35px 255px 0 0 rgba(255, 255, 255, 1),
  40px 255px 0 0 rgba(255, 255, 255, 1), 45px 255px 0 0 rgba(255, 255, 255, 1),
  50px 255px 0 0 rgba(110, 205, 199, 1), 55px 255px 0 0 rgba(255, 255, 255, 1),
  60px 255px 0 0 rgba(255, 255, 255, 1), 65px 255px 0 0 rgba(255, 255, 255, 1),
  70px 255px 0 0 rgba(110, 205, 199, 1), 75px 255px 0 0 rgba(255, 255, 255, 1),
  80px 255px 0 0 rgba(255, 255, 255, 1), 85px 255px 0 0 rgba(255, 255, 255, 1),
  90px 255px 0 0 rgba(110, 205, 199, 1), 95px 255px 0 0 rgba(255, 255, 255, 1),
  100px 255px 0 0 rgba(255, 255, 255, 1), 105px 255px 0 0 rgba(255, 255, 255, 1),
  110px 255px 0 0 rgba(110, 205, 199, 1), 115px 255px 0 0 rgba(255, 255, 255, 1),
  120px 255px 0 0 rgba(255, 255, 255, 1), 125px 255px 0 0 rgba(255, 255, 255, 1),
  130px 255px 0 0 rgba(110, 205, 199, 1), 135px 255px 0 0 rgba(255, 255, 255, 1),
  140px 255px 0 0 rgba(255, 255, 255, 1), 145px 255px 0 0 rgba(255, 255, 255, 1),
  150px 255px 0 0 rgba(110, 205, 199, 1), 155px 255px 0 0 rgba(255, 255, 255, 1),
  160px 255px 0 0 rgba(255, 255, 255, 1), 165px 255px 0 0 rgba(255, 255, 255, 1),
  170px 255px 0 0 rgba(110, 205, 199, 1), 175px 255px 0 0 rgba(255, 255, 255, 1),
  180px 255px 0 0 rgba(255, 255, 255, 1), 185px 255px 0 0 rgba(255, 255, 255, 1),
  190px 255px 0 0 rgba(110, 205, 199, 1), 195px 255px 0 0 rgba(255, 255, 255, 1),
  200px 255px 0 0 rgba(255, 255, 255, 1), 205px 255px 0 0 rgba(255, 255, 255, 1),
  210px 255px 0 0 rgba(110, 205, 199, 1), 215px 255px 0 0 rgba(255, 255, 255, 1),
  220px 255px 0 0 rgba(255, 255, 255, 1), 225px 255px 0 0 rgba(255, 255, 255, 1),
  230px 255px 0 0 rgba(110, 205, 199, 1), 235px 255px 0 0 rgba(255, 255, 255, 1),
  240px 255px 0 0 rgba(255, 255, 255, 1), 245px 255px 0 0 rgba(255, 255, 255, 1),
  250px 255px 0 0 rgba(110, 205, 199, 1), 255px 255px 0 0 rgba(255, 255, 255, 1),
  260px 255px 0 0 rgba(255, 255, 255, 1), 265px 255px 0 0 rgba(255, 255, 255, 1),
  270px 255px 0 0 rgba(110, 205, 199, 1), 275px 255px 0 0 rgba(255, 255, 255, 1),
  280px 255px 0 0 rgba(255, 255, 255, 1), 285px 255px 0 0 rgba(255, 255, 255, 1),
  290px 255px 0 0 rgba(110, 205, 199, 1), 295px 255px 0 0 rgba(255, 255, 255, 1),
  300px 255px 0 0 rgba(255, 255, 255, 1), 305px 255px 0 0 rgba(255, 255, 255, 1),
  310px 255px 0 0 rgba(110, 205, 199, 1), 315px 255px 0 0 rgba(255, 255, 255, 1),
  320px 255px 0 0 rgba(255, 255, 255, 1), 325px 255px 0 0 rgba(255, 255, 255, 1),
  330px 255px 0 0 rgba(110, 205, 199, 1), 335px 255px 0 0 rgba(255, 255, 255, 1),
  340px 255px 0 0 rgba(255, 255, 255, 1), 345px 255px 0 0 rgba(255, 255, 255, 1),
  350px 255px 0 0 rgba(110, 205, 199, 1), 355px 255px 0 0 rgba(255, 255, 255, 1),
  360px 255px 0 0 rgba(255, 255, 255, 1), 365px 255px 0 0 rgba(255, 255, 255, 1),
  370px 255px 0 0 rgba(110, 205, 199, 1), 375px 255px 0 0 rgba(255, 255, 255, 1),
  380px 255px 0 0 rgba(255, 255, 255, 1), 385px 255px 0 0 rgba(255, 255, 255, 1),
  390px 255px 0 0 rgba(110, 205, 199, 1), 395px 255px 0 0 rgba(255, 255, 255, 1),
  400px 255px 0 0 rgba(255, 255, 255, 1), 405px 255px 0 0 rgba(255, 255, 255, 1),
  410px 255px 0 0 rgba(110, 205, 199, 1), 415px 255px 0 0 rgba(255, 255, 255, 1),
  420px 255px 0 0 rgba(255, 255, 255, 1), 425px 255px 0 0 rgba(255, 255, 255, 1),
  430px 255px 0 0 rgba(110, 205, 199, 1), 435px 255px 0 0 rgba(255, 255, 255, 1),
  440px 255px 0 0 rgba(255, 255, 255, 1), 445px 255px 0 0 rgba(255, 255, 255, 1),
  450px 255px 0 0 rgba(110, 205, 199, 1), 455px 255px 0 0 rgba(255, 255, 255, 1),
  460px 255px 0 0 rgba(255, 255, 255, 1), 465px 255px 0 0 rgba(255, 255, 255, 1),
  470px 255px 0 0 rgba(110, 205, 199, 1), 475px 255px 0 0 rgba(255, 255, 255, 1),
  480px 255px 0 0 rgba(255, 255, 255, 1), 485px 255px 0 0 rgba(255, 255, 255, 1),
  490px 255px 0 0 rgba(110, 205, 199, 1), 495px 255px 0 0 rgba(255, 255, 255, 1),
  500px 255px 0 0 rgba(255, 255, 255, 1), 505px 255px 0 0 rgba(255, 255, 255, 1),
  510px 255px 0 0 rgba(110, 205, 199, 1), 515px 255px 0 0 rgba(255, 255, 255, 1),
  520px 255px 0 0 rgba(255, 255, 255, 1), 525px 255px 0 0 rgba(255, 255, 255, 1),
  530px 255px 0 0 rgba(110, 205, 199, 1), 535px 255px 0 0 rgba(255, 255, 255, 1),
  540px 255px 0 0 rgba(255, 255, 255, 1), 545px 255px 0 0 rgba(255, 255, 255, 1),
  550px 255px 0 0 rgba(110, 205, 199, 1), 555px 255px 0 0 rgba(255, 255, 255, 1),
  560px 255px 0 0 rgba(255, 255, 255, 1), 565px 255px 0 0 rgba(255, 255, 255, 1),
  570px 255px 0 0 rgba(110, 205, 199, 1), 575px 255px 0 0 rgba(255, 255, 255, 1),
  580px 255px 0 0 rgba(255, 255, 255, 1), 585px 255px 0 0 rgba(255, 255, 255, 1),
  590px 255px 0 0 rgba(110, 205, 199, 1), 595px 255px 0 0 rgba(255, 255, 255, 1),
  600px 255px 0 0 rgba(255, 255, 255, 1), 605px 255px 0 0 rgba(255, 255, 255, 1),
  610px 255px 0 0 rgba(110, 205, 199, 1), 615px 255px 0 0 rgba(255, 255, 255, 1),
  620px 255px 0 0 rgba(255, 255, 255, 1), 625px 255px 0 0 rgba(255, 255, 255, 1),
  630px 255px 0 0 rgba(110, 205, 199, 1), 635px 255px 0 0 rgba(255, 255, 255, 1),
  640px 255px 0 0 rgba(255, 255, 255, 1), 645px 255px 0 0 rgba(255, 255, 255, 1),
  650px 255px 0 0 rgba(110, 205, 199, 1), 655px 255px 0 0 rgba(255, 255, 255, 1),
  660px 255px 0 0 rgba(255, 255, 255, 1), 665px 255px 0 0 rgba(255, 255, 255, 1),
  670px 255px 0 0 rgba(255, 255, 255, 1), 675px 255px 0 0 rgba(255, 255, 255, 1),
  680px 255px 0 0 rgba(255, 255, 255, 1), 685px 255px 0 0 rgba(203, 109, 181, 1),
  690px 255px 0 0 rgba(255, 205, 234, 1), 695px 255px 0 0 rgba(255, 205, 234, 1),
  700px 255px 0 0 rgba(168, 90, 150, 1), 705px 255px 0 0 rgba(203, 109, 181, 1),
  5px 260px 0 0 rgba(203, 109, 181, 1), 10px 260px 0 0 rgba(252, 231, 243, 1),
  15px 260px 0 0 rgba(255, 205, 234, 1), 20px 260px 0 0 rgba(255, 205, 234, 1),
  25px 260px 0 0 rgba(203, 109, 181, 1), 30px 260px 0 0 rgba(255, 255, 255, 1),
  35px 260px 0 0 rgba(255, 255, 255, 1), 40px 260px 0 0 rgba(255, 255, 255, 1),
  45px 260px 0 0 rgba(255, 255, 255, 1), 50px 260px 0 0 rgba(255, 255, 255, 1),
  55px 260px 0 0 rgba(255, 255, 255, 1), 60px 260px 0 0 rgba(255, 255, 255, 1),
  65px 260px 0 0 rgba(255, 255, 255, 1), 70px 260px 0 0 rgba(255, 255, 255, 1),
  75px 260px 0 0 rgba(255, 255, 255, 1), 80px 260px 0 0 rgba(255, 255, 255, 1),
  85px 260px 0 0 rgba(255, 255, 255, 1), 90px 260px 0 0 rgba(255, 255, 255, 1),
  95px 260px 0 0 rgba(255, 255, 255, 1), 100px 260px 0 0 rgba(255, 255, 255, 1),
  105px 260px 0 0 rgba(255, 255, 255, 1), 110px 260px 0 0 rgba(255, 255, 255, 1),
  115px 260px 0 0 rgba(255, 255, 255, 1), 120px 260px 0 0 rgba(255, 255, 255, 1),
  125px 260px 0 0 rgba(255, 255, 255, 1), 130px 260px 0 0 rgba(255, 255, 255, 1),
  135px 260px 0 0 rgba(255, 255, 255, 1), 140px 260px 0 0 rgba(255, 255, 255, 1),
  145px 260px 0 0 rgba(255, 255, 255, 1), 150px 260px 0 0 rgba(255, 255, 255, 1),
  155px 260px 0 0 rgba(255, 255, 255, 1), 160px 260px 0 0 rgba(255, 255, 255, 1),
  165px 260px 0 0 rgba(255, 255, 255, 1), 170px 260px 0 0 rgba(255, 255, 255, 1),
  175px 260px 0 0 rgba(255, 255, 255, 1), 180px 260px 0 0 rgba(255, 255, 255, 1),
  185px 260px 0 0 rgba(255, 255, 255, 1), 190px 260px 0 0 rgba(255, 255, 255, 1),
  195px 260px 0 0 rgba(255, 255, 255, 1), 200px 260px 0 0 rgba(255, 255, 255, 1),
  205px 260px 0 0 rgba(255, 255, 255, 1), 210px 260px 0 0 rgba(255, 255, 255, 1),
  215px 260px 0 0 rgba(255, 255, 255, 1), 220px 260px 0 0 rgba(255, 255, 255, 1),
  225px 260px 0 0 rgba(255, 255, 255, 1), 230px 260px 0 0 rgba(255, 255, 255, 1),
  235px 260px 0 0 rgba(255, 255, 255, 1), 240px 260px 0 0 rgba(255, 255, 255, 1),
  245px 260px 0 0 rgba(255, 255, 255, 1), 250px 260px 0 0 rgba(255, 255, 255, 1),
  255px 260px 0 0 rgba(255, 255, 255, 1), 260px 260px 0 0 rgba(255, 255, 255, 1),
  265px 260px 0 0 rgba(255, 255, 255, 1), 270px 260px 0 0 rgba(255, 255, 255, 1),
  275px 260px 0 0 rgba(255, 255, 255, 1), 280px 260px 0 0 rgba(255, 255, 255, 1),
  285px 260px 0 0 rgba(255, 255, 255, 1), 290px 260px 0 0 rgba(255, 255, 255, 1),
  295px 260px 0 0 rgba(255, 255, 255, 1), 300px 260px 0 0 rgba(255, 255, 255, 1),
  305px 260px 0 0 rgba(255, 255, 255, 1), 310px 260px 0 0 rgba(255, 255, 255, 1),
  315px 260px 0 0 rgba(255, 255, 255, 1), 320px 260px 0 0 rgba(255, 255, 255, 1),
  325px 260px 0 0 rgba(255, 255, 255, 1), 330px 260px 0 0 rgba(255, 255, 255, 1),
  335px 260px 0 0 rgba(255, 255, 255, 1), 340px 260px 0 0 rgba(255, 255, 255, 1),
  345px 260px 0 0 rgba(255, 255, 255, 1), 350px 260px 0 0 rgba(255, 255, 255, 1),
  355px 260px 0 0 rgba(255, 255, 255, 1), 360px 260px 0 0 rgba(255, 255, 255, 1),
  365px 260px 0 0 rgba(255, 255, 255, 1), 370px 260px 0 0 rgba(255, 255, 255, 1),
  375px 260px 0 0 rgba(255, 255, 255, 1), 380px 260px 0 0 rgba(255, 255, 255, 1),
  385px 260px 0 0 rgba(255, 255, 255, 1), 390px 260px 0 0 rgba(255, 255, 255, 1),
  395px 260px 0 0 rgba(255, 255, 255, 1), 400px 260px 0 0 rgba(255, 255, 255, 1),
  405px 260px 0 0 rgba(255, 255, 255, 1), 410px 260px 0 0 rgba(255, 255, 255, 1),
  415px 260px 0 0 rgba(255, 255, 255, 1), 420px 260px 0 0 rgba(255, 255, 255, 1),
  425px 260px 0 0 rgba(255, 255, 255, 1), 430px 260px 0 0 rgba(255, 255, 255, 1),
  435px 260px 0 0 rgba(255, 255, 255, 1), 440px 260px 0 0 rgba(255, 255, 255, 1),
  445px 260px 0 0 rgba(255, 255, 255, 1), 450px 260px 0 0 rgba(255, 255, 255, 1),
  455px 260px 0 0 rgba(255, 255, 255, 1), 460px 260px 0 0 rgba(255, 255, 255, 1),
  465px 260px 0 0 rgba(255, 255, 255, 1), 470px 260px 0 0 rgba(255, 255, 255, 1),
  475px 260px 0 0 rgba(255, 255, 255, 1), 480px 260px 0 0 rgba(255, 255, 255, 1),
  485px 260px 0 0 rgba(255, 255, 255, 1), 490px 260px 0 0 rgba(255, 255, 255, 1),
  495px 260px 0 0 rgba(255, 255, 255, 1), 500px 260px 0 0 rgba(255, 255, 255, 1),
  505px 260px 0 0 rgba(255, 255, 255, 1), 510px 260px 0 0 rgba(255, 255, 255, 1),
  515px 260px 0 0 rgba(255, 255, 255, 1), 520px 260px 0 0 rgba(255, 255, 255, 1),
  525px 260px 0 0 rgba(255, 255, 255, 1), 530px 260px 0 0 rgba(255, 255, 255, 1),
  535px 260px 0 0 rgba(255, 255, 255, 1), 540px 260px 0 0 rgba(255, 255, 255, 1),
  545px 260px 0 0 rgba(255, 255, 255, 1), 550px 260px 0 0 rgba(255, 255, 255, 1),
  555px 260px 0 0 rgba(255, 255, 255, 1), 560px 260px 0 0 rgba(255, 255, 255, 1),
  565px 260px 0 0 rgba(255, 255, 255, 1), 570px 260px 0 0 rgba(255, 255, 255, 1),
  575px 260px 0 0 rgba(255, 255, 255, 1), 580px 260px 0 0 rgba(255, 255, 255, 1),
  585px 260px 0 0 rgba(255, 255, 255, 1), 590px 260px 0 0 rgba(255, 255, 255, 1),
  595px 260px 0 0 rgba(255, 255, 255, 1), 600px 260px 0 0 rgba(255, 255, 255, 1),
  605px 260px 0 0 rgba(255, 255, 255, 1), 610px 260px 0 0 rgba(255, 255, 255, 1),
  615px 260px 0 0 rgba(255, 255, 255, 1), 620px 260px 0 0 rgba(255, 255, 255, 1),
  625px 260px 0 0 rgba(255, 255, 255, 1), 630px 260px 0 0 rgba(255, 255, 255, 1),
  635px 260px 0 0 rgba(255, 255, 255, 1), 640px 260px 0 0 rgba(255, 255, 255, 1),
  645px 260px 0 0 rgba(255, 255, 255, 1), 650px 260px 0 0 rgba(255, 255, 255, 1),
  655px 260px 0 0 rgba(255, 255, 255, 1), 660px 260px 0 0 rgba(255, 255, 255, 1),
  665px 260px 0 0 rgba(255, 255, 255, 1), 670px 260px 0 0 rgba(255, 255, 255, 1),
  675px 260px 0 0 rgba(255, 255, 255, 1), 680px 260px 0 0 rgba(255, 255, 255, 1),
  685px 260px 0 0 rgba(203, 109, 181, 1), 690px 260px 0 0 rgba(255, 205, 234, 1),
  695px 260px 0 0 rgba(255, 205, 234, 1), 700px 260px 0 0 rgba(168, 90, 150, 1),
  705px 260px 0 0 rgba(203, 109, 181, 1), 5px 265px 0 0 rgba(203, 109, 181, 1),
  10px 265px 0 0 rgba(252, 231, 243, 1), 15px 265px 0 0 rgba(255, 205, 234, 1),
  20px 265px 0 0 rgba(255, 205, 234, 1), 25px 265px 0 0 rgba(203, 109, 181, 1),
  30px 265px 0 0 rgba(255, 255, 255, 1), 35px 265px 0 0 rgba(255, 255, 255, 1),
  40px 265px 0 0 rgba(255, 255, 255, 1), 45px 265px 0 0 rgba(255, 255, 255, 1),
  50px 265px 0 0 rgba(255, 255, 255, 1), 55px 265px 0 0 rgba(255, 255, 255, 1),
  60px 265px 0 0 rgba(255, 255, 255, 1), 65px 265px 0 0 rgba(255, 255, 255, 1),
  70px 265px 0 0 rgba(255, 255, 255, 1), 75px 265px 0 0 rgba(255, 255, 255, 1),
  80px 265px 0 0 rgba(255, 255, 255, 1), 85px 265px 0 0 rgba(255, 255, 255, 1),
  90px 265px 0 0 rgba(255, 255, 255, 1), 95px 265px 0 0 rgba(255, 255, 255, 1),
  100px 265px 0 0 rgba(255, 255, 255, 1), 105px 265px 0 0 rgba(255, 255, 255, 1),
  110px 265px 0 0 rgba(255, 255, 255, 1), 115px 265px 0 0 rgba(255, 255, 255, 1),
  120px 265px 0 0 rgba(255, 255, 255, 1), 125px 265px 0 0 rgba(255, 255, 255, 1),
  130px 265px 0 0 rgba(255, 255, 255, 1), 135px 265px 0 0 rgba(255, 255, 255, 1),
  140px 265px 0 0 rgba(255, 255, 255, 1), 145px 265px 0 0 rgba(255, 255, 255, 1),
  150px 265px 0 0 rgba(255, 255, 255, 1), 155px 265px 0 0 rgba(255, 255, 255, 1),
  160px 265px 0 0 rgba(255, 255, 255, 1), 165px 265px 0 0 rgba(255, 255, 255, 1),
  170px 265px 0 0 rgba(255, 255, 255, 1), 175px 265px 0 0 rgba(255, 255, 255, 1),
  180px 265px 0 0 rgba(255, 255, 255, 1), 185px 265px 0 0 rgba(255, 255, 255, 1),
  190px 265px 0 0 rgba(255, 255, 255, 1), 195px 265px 0 0 rgba(255, 255, 255, 1),
  200px 265px 0 0 rgba(255, 255, 255, 1), 205px 265px 0 0 rgba(255, 255, 255, 1),
  210px 265px 0 0 rgba(255, 255, 255, 1), 215px 265px 0 0 rgba(255, 255, 255, 1),
  220px 265px 0 0 rgba(255, 255, 255, 1), 225px 265px 0 0 rgba(255, 255, 255, 1),
  230px 265px 0 0 rgba(255, 255, 255, 1), 235px 265px 0 0 rgba(255, 255, 255, 1),
  240px 265px 0 0 rgba(255, 255, 255, 1), 245px 265px 0 0 rgba(255, 255, 255, 1),
  250px 265px 0 0 rgba(255, 255, 255, 1), 255px 265px 0 0 rgba(255, 255, 255, 1),
  260px 265px 0 0 rgba(255, 255, 255, 1), 265px 265px 0 0 rgba(255, 255, 255, 1),
  270px 265px 0 0 rgba(255, 255, 255, 1), 275px 265px 0 0 rgba(255, 255, 255, 1),
  280px 265px 0 0 rgba(255, 255, 255, 1), 285px 265px 0 0 rgba(255, 255, 255, 1),
  290px 265px 0 0 rgba(255, 255, 255, 1), 295px 265px 0 0 rgba(255, 255, 255, 1),
  300px 265px 0 0 rgba(255, 255, 255, 1), 305px 265px 0 0 rgba(255, 255, 255, 1),
  310px 265px 0 0 rgba(255, 255, 255, 1), 315px 265px 0 0 rgba(255, 255, 255, 1),
  320px 265px 0 0 rgba(255, 255, 255, 1), 325px 265px 0 0 rgba(255, 255, 255, 1),
  330px 265px 0 0 rgba(255, 255, 255, 1), 335px 265px 0 0 rgba(255, 255, 255, 1),
  340px 265px 0 0 rgba(255, 255, 255, 1), 345px 265px 0 0 rgba(255, 255, 255, 1),
  350px 265px 0 0 rgba(255, 255, 255, 1), 355px 265px 0 0 rgba(255, 255, 255, 1),
  360px 265px 0 0 rgba(255, 255, 255, 1), 365px 265px 0 0 rgba(255, 255, 255, 1),
  370px 265px 0 0 rgba(255, 255, 255, 1), 375px 265px 0 0 rgba(255, 255, 255, 1),
  380px 265px 0 0 rgba(255, 255, 255, 1), 385px 265px 0 0 rgba(255, 255, 255, 1),
  390px 265px 0 0 rgba(255, 255, 255, 1), 395px 265px 0 0 rgba(255, 255, 255, 1),
  400px 265px 0 0 rgba(255, 255, 255, 1), 405px 265px 0 0 rgba(255, 255, 255, 1),
  410px 265px 0 0 rgba(255, 255, 255, 1), 415px 265px 0 0 rgba(255, 255, 255, 1),
  420px 265px 0 0 rgba(255, 255, 255, 1), 425px 265px 0 0 rgba(255, 255, 255, 1),
  430px 265px 0 0 rgba(255, 255, 255, 1), 435px 265px 0 0 rgba(255, 255, 255, 1),
  440px 265px 0 0 rgba(255, 255, 255, 1), 445px 265px 0 0 rgba(255, 255, 255, 1),
  450px 265px 0 0 rgba(255, 255, 255, 1), 455px 265px 0 0 rgba(255, 255, 255, 1),
  460px 265px 0 0 rgba(255, 255, 255, 1), 465px 265px 0 0 rgba(255, 255, 255, 1),
  470px 265px 0 0 rgba(255, 255, 255, 1), 475px 265px 0 0 rgba(255, 255, 255, 1),
  480px 265px 0 0 rgba(255, 255, 255, 1), 485px 265px 0 0 rgba(255, 255, 255, 1),
  490px 265px 0 0 rgba(255, 255, 255, 1), 495px 265px 0 0 rgba(255, 255, 255, 1),
  500px 265px 0 0 rgba(255, 255, 255, 1), 505px 265px 0 0 rgba(255, 255, 255, 1),
  510px 265px 0 0 rgba(255, 255, 255, 1), 515px 265px 0 0 rgba(255, 255, 255, 1),
  520px 265px 0 0 rgba(255, 255, 255, 1), 525px 265px 0 0 rgba(255, 255, 255, 1),
  530px 265px 0 0 rgba(255, 255, 255, 1), 535px 265px 0 0 rgba(255, 255, 255, 1),
  540px 265px 0 0 rgba(255, 255, 255, 1), 545px 265px 0 0 rgba(255, 255, 255, 1),
  550px 265px 0 0 rgba(255, 255, 255, 1), 555px 265px 0 0 rgba(255, 255, 255, 1),
  560px 265px 0 0 rgba(255, 255, 255, 1), 565px 265px 0 0 rgba(255, 255, 255, 1),
  570px 265px 0 0 rgba(255, 255, 255, 1), 575px 265px 0 0 rgba(255, 255, 255, 1),
  580px 265px 0 0 rgba(255, 255, 255, 1), 585px 265px 0 0 rgba(255, 255, 255, 1),
  590px 265px 0 0 rgba(255, 255, 255, 1), 595px 265px 0 0 rgba(255, 255, 255, 1),
  600px 265px 0 0 rgba(255, 255, 255, 1), 605px 265px 0 0 rgba(255, 255, 255, 1),
  610px 265px 0 0 rgba(255, 255, 255, 1), 615px 265px 0 0 rgba(255, 255, 255, 1),
  620px 265px 0 0 rgba(255, 255, 255, 1), 625px 265px 0 0 rgba(255, 255, 255, 1),
  630px 265px 0 0 rgba(255, 255, 255, 1), 635px 265px 0 0 rgba(255, 255, 255, 1),
  640px 265px 0 0 rgba(255, 255, 255, 1), 645px 265px 0 0 rgba(255, 255, 255, 1),
  650px 265px 0 0 rgba(255, 255, 255, 1), 655px 265px 0 0 rgba(255, 255, 255, 1),
  660px 265px 0 0 rgba(255, 255, 255, 1), 665px 265px 0 0 rgba(255, 255, 255, 1),
  670px 265px 0 0 rgba(255, 255, 255, 1), 675px 265px 0 0 rgba(255, 255, 255, 1),
  680px 265px 0 0 rgba(255, 255, 255, 1), 685px 265px 0 0 rgba(203, 109, 181, 1),
  690px 265px 0 0 rgba(255, 205, 234, 1), 695px 265px 0 0 rgba(255, 205, 234, 1),
  700px 265px 0 0 rgba(168, 90, 150, 1), 705px 265px 0 0 rgba(203, 109, 181, 1),
  5px 270px 0 0 rgba(203, 109, 181, 1), 10px 270px 0 0 rgba(252, 231, 243, 1),
  15px 270px 0 0 rgba(255, 205, 234, 1), 20px 270px 0 0 rgba(255, 205, 234, 1),
  25px 270px 0 0 rgba(203, 109, 181, 1), 30px 270px 0 0 rgba(222, 185, 134, 1),
  35px 270px 0 0 rgba(222, 185, 134, 1), 40px 270px 0 0 rgba(222, 185, 134, 1),
  45px 270px 0 0 rgba(222, 185, 134, 1), 50px 270px 0 0 rgba(222, 185, 134, 1),
  55px 270px 0 0 rgba(222, 185, 134, 1), 60px 270px 0 0 rgba(222, 185, 134, 1),
  65px 270px 0 0 rgba(222, 185, 134, 1), 70px 270px 0 0 rgba(222, 185, 134, 1),
  75px 270px 0 0 rgba(222, 185, 134, 1), 80px 270px 0 0 rgba(222, 185, 134, 1),
  85px 270px 0 0 rgba(222, 185, 134, 1), 90px 270px 0 0 rgba(222, 185, 134, 1),
  95px 270px 0 0 rgba(222, 185, 134, 1), 100px 270px 0 0 rgba(222, 185, 134, 1),
  105px 270px 0 0 rgba(222, 185, 134, 1), 110px 270px 0 0 rgba(222, 185, 134, 1),
  115px 270px 0 0 rgba(222, 185, 134, 1), 120px 270px 0 0 rgba(222, 185, 134, 1),
  125px 270px 0 0 rgba(222, 185, 134, 1), 130px 270px 0 0 rgba(222, 185, 134, 1),
  135px 270px 0 0 rgba(222, 185, 134, 1), 140px 270px 0 0 rgba(222, 185, 134, 1),
  145px 270px 0 0 rgba(222, 185, 134, 1), 150px 270px 0 0 rgba(222, 185, 134, 1),
  155px 270px 0 0 rgba(222, 185, 134, 1), 160px 270px 0 0 rgba(222, 185, 134, 1),
  165px 270px 0 0 rgba(222, 185, 134, 1), 170px 270px 0 0 rgba(222, 185, 134, 1),
  175px 270px 0 0 rgba(222, 185, 134, 1), 180px 270px 0 0 rgba(222, 185, 134, 1),
  185px 270px 0 0 rgba(222, 185, 134, 1), 190px 270px 0 0 rgba(222, 185, 134, 1),
  195px 270px 0 0 rgba(222, 185, 134, 1), 200px 270px 0 0 rgba(222, 185, 134, 1),
  205px 270px 0 0 rgba(222, 185, 134, 1), 210px 270px 0 0 rgba(222, 185, 134, 1),
  215px 270px 0 0 rgba(222, 185, 134, 1), 220px 270px 0 0 rgba(222, 185, 134, 1),
  225px 270px 0 0 rgba(222, 185, 134, 1), 230px 270px 0 0 rgba(222, 185, 134, 1),
  235px 270px 0 0 rgba(222, 185, 134, 1), 240px 270px 0 0 rgba(222, 185, 134, 1),
  245px 270px 0 0 rgba(222, 185, 134, 1), 250px 270px 0 0 rgba(222, 185, 134, 1),
  255px 270px 0 0 rgba(222, 185, 134, 1), 260px 270px 0 0 rgba(222, 185, 134, 1),
  265px 270px 0 0 rgba(222, 185, 134, 1), 270px 270px 0 0 rgba(222, 185, 134, 1),
  275px 270px 0 0 rgba(222, 185, 134, 1), 280px 270px 0 0 rgba(222, 185, 134, 1),
  285px 270px 0 0 rgba(222, 185, 134, 1), 290px 270px 0 0 rgba(222, 185, 134, 1),
  295px 270px 0 0 rgba(222, 185, 134, 1), 300px 270px 0 0 rgba(222, 185, 134, 1),
  305px 270px 0 0 rgba(222, 185, 134, 1), 310px 270px 0 0 rgba(222, 185, 134, 1),
  315px 270px 0 0 rgba(222, 185, 134, 1), 320px 270px 0 0 rgba(222, 185, 134, 1),
  325px 270px 0 0 rgba(222, 185, 134, 1), 330px 270px 0 0 rgba(222, 185, 134, 1),
  335px 270px 0 0 rgba(222, 185, 134, 1), 340px 270px 0 0 rgba(222, 185, 134, 1),
  345px 270px 0 0 rgba(222, 185, 134, 1), 350px 270px 0 0 rgba(222, 185, 134, 1),
  355px 270px 0 0 rgba(222, 185, 134, 1), 360px 270px 0 0 rgba(222, 185, 134, 1),
  365px 270px 0 0 rgba(222, 185, 134, 1), 370px 270px 0 0 rgba(222, 185, 134, 1),
  375px 270px 0 0 rgba(222, 185, 134, 1), 380px 270px 0 0 rgba(222, 185, 134, 1),
  385px 270px 0 0 rgba(222, 185, 134, 1), 390px 270px 0 0 rgba(222, 185, 134, 1),
  395px 270px 0 0 rgba(222, 185, 134, 1), 400px 270px 0 0 rgba(222, 185, 134, 1),
  405px 270px 0 0 rgba(222, 185, 134, 1), 410px 270px 0 0 rgba(222, 185, 134, 1),
  415px 270px 0 0 rgba(222, 185, 134, 1), 420px 270px 0 0 rgba(222, 185, 134, 1),
  425px 270px 0 0 rgba(222, 185, 134, 1), 430px 270px 0 0 rgba(222, 185, 134, 1),
  435px 270px 0 0 rgba(222, 185, 134, 1), 440px 270px 0 0 rgba(222, 185, 134, 1),
  445px 270px 0 0 rgba(222, 185, 134, 1), 450px 270px 0 0 rgba(222, 185, 134, 1),
  455px 270px 0 0 rgba(222, 185, 134, 1), 460px 270px 0 0 rgba(222, 185, 134, 1),
  465px 270px 0 0 rgba(222, 185, 134, 1), 470px 270px 0 0 rgba(222, 185, 134, 1),
  475px 270px 0 0 rgba(222, 185, 134, 1), 480px 270px 0 0 rgba(222, 185, 134, 1),
  485px 270px 0 0 rgba(222, 185, 134, 1), 490px 270px 0 0 rgba(222, 185, 134, 1),
  495px 270px 0 0 rgba(222, 185, 134, 1), 500px 270px 0 0 rgba(222, 185, 134, 1),
  505px 270px 0 0 rgba(222, 185, 134, 1), 510px 270px 0 0 rgba(222, 185, 134, 1),
  515px 270px 0 0 rgba(222, 185, 134, 1), 520px 270px 0 0 rgba(222, 185, 134, 1),
  525px 270px 0 0 rgba(222, 185, 134, 1), 530px 270px 0 0 rgba(222, 185, 134, 1),
  535px 270px 0 0 rgba(222, 185, 134, 1), 540px 270px 0 0 rgba(222, 185, 134, 1),
  545px 270px 0 0 rgba(222, 185, 134, 1), 550px 270px 0 0 rgba(222, 185, 134, 1),
  555px 270px 0 0 rgba(222, 185, 134, 1), 560px 270px 0 0 rgba(222, 185, 134, 1),
  565px 270px 0 0 rgba(222, 185, 134, 1), 570px 270px 0 0 rgba(222, 185, 134, 1),
  575px 270px 0 0 rgba(222, 185, 134, 1), 580px 270px 0 0 rgba(222, 185, 134, 1),
  585px 270px 0 0 rgba(222, 185, 134, 1), 590px 270px 0 0 rgba(222, 185, 134, 1),
  595px 270px 0 0 rgba(222, 185, 134, 1), 600px 270px 0 0 rgba(222, 185, 134, 1),
  605px 270px 0 0 rgba(222, 185, 134, 1), 610px 270px 0 0 rgba(222, 185, 134, 1),
  615px 270px 0 0 rgba(222, 185, 134, 1), 620px 270px 0 0 rgba(222, 185, 134, 1),
  625px 270px 0 0 rgba(222, 185, 134, 1), 630px 270px 0 0 rgba(222, 185, 134, 1),
  635px 270px 0 0 rgba(222, 185, 134, 1), 640px 270px 0 0 rgba(222, 185, 134, 1),
  645px 270px 0 0 rgba(222, 185, 134, 1), 650px 270px 0 0 rgba(222, 185, 134, 1),
  655px 270px 0 0 rgba(222, 185, 134, 1), 660px 270px 0 0 rgba(222, 185, 134, 1),
  665px 270px 0 0 rgba(222, 185, 134, 1), 670px 270px 0 0 rgba(222, 185, 134, 1),
  675px 270px 0 0 rgba(222, 185, 134, 1), 680px 270px 0 0 rgba(222, 185, 134, 1),
  685px 270px 0 0 rgba(203, 109, 181, 1), 690px 270px 0 0 rgba(255, 205, 234, 1),
  695px 270px 0 0 rgba(255, 205, 234, 1), 700px 270px 0 0 rgba(168, 90, 150, 1),
  705px 270px 0 0 rgba(203, 109, 181, 1), 5px 275px 0 0 rgba(203, 109, 181, 1),
  10px 275px 0 0 rgba(252, 231, 243, 1), 15px 275px 0 0 rgba(255, 205, 234, 1),
  20px 275px 0 0 rgba(255, 205, 234, 1), 25px 275px 0 0 rgba(203, 109, 181, 1),
  120px 275px 0 0 rgba(222, 185, 134, 1), 125px 275px 0 0 rgba(222, 185, 134, 1),
  245px 275px 0 0 rgba(222, 185, 134, 1), 250px 275px 0 0 rgba(222, 185, 134, 1),
  330px 275px 0 0 rgba(222, 185, 134, 1), 390px 275px 0 0 rgba(222, 185, 134, 1),
  395px 275px 0 0 rgba(222, 185, 134, 1), 490px 275px 0 0 rgba(222, 185, 134, 1),
  495px 275px 0 0 rgba(222, 185, 134, 1), 590px 275px 0 0 rgba(222, 185, 134, 1),
  595px 275px 0 0 rgba(222, 185, 134, 1), 600px 275px 0 0 rgba(222, 185, 134, 1),
  685px 275px 0 0 rgba(203, 109, 181, 1), 690px 275px 0 0 rgba(255, 205, 234, 1),
  695px 275px 0 0 rgba(255, 205, 234, 1), 700px 275px 0 0 rgba(168, 90, 150, 1),
  705px 275px 0 0 rgba(203, 109, 181, 1), 5px 280px 0 0 rgba(203, 109, 181, 1),
  10px 280px 0 0 rgba(252, 231, 243, 1), 15px 280px 0 0 rgba(255, 205, 234, 1),
  20px 280px 0 0 rgba(255, 205, 234, 1), 25px 280px 0 0 rgba(203, 109, 181, 1),
  110px 280px 0 0 rgba(222, 185, 134, 1), 115px 280px 0 0 rgba(222, 185, 134, 1),
  240px 280px 0 0 rgba(222, 185, 134, 1), 245px 280px 0 0 rgba(222, 185, 134, 1),
  330px 280px 0 0 rgba(222, 185, 134, 1), 395px 280px 0 0 rgba(222, 185, 134, 1),
  400px 280px 0 0 rgba(222, 185, 134, 1), 500px 280px 0 0 rgba(222, 185, 134, 1),
  505px 280px 0 0 rgba(222, 185, 134, 1), 605px 280px 0 0 rgba(222, 185, 134, 1),
  610px 280px 0 0 rgba(222, 185, 134, 1), 615px 280px 0 0 rgba(222, 185, 134, 1),
  685px 280px 0 0 rgba(203, 109, 181, 1), 690px 280px 0 0 rgba(255, 205, 234, 1),
  695px 280px 0 0 rgba(255, 205, 234, 1), 700px 280px 0 0 rgba(168, 90, 150, 1),
  705px 280px 0 0 rgba(203, 109, 181, 1), 5px 285px 0 0 rgba(203, 109, 181, 1),
  10px 285px 0 0 rgba(252, 231, 243, 1), 15px 285px 0 0 rgba(255, 205, 234, 1),
  20px 285px 0 0 rgba(255, 205, 234, 1), 25px 285px 0 0 rgba(203, 109, 181, 1),
  100px 285px 0 0 rgba(222, 185, 134, 1), 105px 285px 0 0 rgba(222, 185, 134, 1),
  235px 285px 0 0 rgba(222, 185, 134, 1), 240px 285px 0 0 rgba(222, 185, 134, 1),
  330px 285px 0 0 rgba(222, 185, 134, 1), 400px 285px 0 0 rgba(222, 185, 134, 1),
  405px 285px 0 0 rgba(222, 185, 134, 1), 510px 285px 0 0 rgba(222, 185, 134, 1),
  515px 285px 0 0 rgba(222, 185, 134, 1), 620px 285px 0 0 rgba(222, 185, 134, 1),
  625px 285px 0 0 rgba(222, 185, 134, 1), 685px 285px 0 0 rgba(203, 109, 181, 1),
  690px 285px 0 0 rgba(255, 205, 234, 1), 695px 285px 0 0 rgba(255, 205, 234, 1),
  700px 285px 0 0 rgba(168, 90, 150, 1), 705px 285px 0 0 rgba(203, 109, 181, 1),
  5px 290px 0 0 rgba(203, 109, 181, 1), 10px 290px 0 0 rgba(252, 231, 243, 1),
  15px 290px 0 0 rgba(255, 205, 234, 1), 20px 290px 0 0 rgba(255, 205, 234, 1),
  25px 290px 0 0 rgba(203, 109, 181, 1), 30px 290px 0 0 rgba(222, 185, 134, 1),
  35px 290px 0 0 rgba(222, 185, 134, 1), 40px 290px 0 0 rgba(222, 185, 134, 1),
  45px 290px 0 0 rgba(222, 185, 134, 1), 50px 290px 0 0 rgba(222, 185, 134, 1),
  55px 290px 0 0 rgba(222, 185, 134, 1), 60px 290px 0 0 rgba(222, 185, 134, 1),
  65px 290px 0 0 rgba(222, 185, 134, 1), 70px 290px 0 0 rgba(222, 185, 134, 1),
  75px 290px 0 0 rgba(222, 185, 134, 1), 80px 290px 0 0 rgba(222, 185, 134, 1),
  85px 290px 0 0 rgba(222, 185, 134, 1), 90px 290px 0 0 rgba(222, 185, 134, 1),
  95px 290px 0 0 rgba(222, 185, 134, 1), 100px 290px 0 0 rgba(222, 185, 134, 1),
  105px 290px 0 0 rgba(222, 185, 134, 1), 110px 290px 0 0 rgba(222, 185, 134, 1),
  115px 290px 0 0 rgba(222, 185, 134, 1), 120px 290px 0 0 rgba(222, 185, 134, 1),
  125px 290px 0 0 rgba(222, 185, 134, 1), 130px 290px 0 0 rgba(222, 185, 134, 1),
  135px 290px 0 0 rgba(222, 185, 134, 1), 140px 290px 0 0 rgba(222, 185, 134, 1),
  145px 290px 0 0 rgba(222, 185, 134, 1), 150px 290px 0 0 rgba(222, 185, 134, 1),
  155px 290px 0 0 rgba(222, 185, 134, 1), 160px 290px 0 0 rgba(222, 185, 134, 1),
  165px 290px 0 0 rgba(222, 185, 134, 1), 170px 290px 0 0 rgba(222, 185, 134, 1),
  175px 290px 0 0 rgba(222, 185, 134, 1), 180px 290px 0 0 rgba(222, 185, 134, 1),
  185px 290px 0 0 rgba(222, 185, 134, 1), 190px 290px 0 0 rgba(222, 185, 134, 1),
  195px 290px 0 0 rgba(222, 185, 134, 1), 200px 290px 0 0 rgba(222, 185, 134, 1),
  205px 290px 0 0 rgba(222, 185, 134, 1), 210px 290px 0 0 rgba(222, 185, 134, 1),
  215px 290px 0 0 rgba(222, 185, 134, 1), 220px 290px 0 0 rgba(222, 185, 134, 1),
  225px 290px 0 0 rgba(222, 185, 134, 1), 230px 290px 0 0 rgba(222, 185, 134, 1),
  235px 290px 0 0 rgba(222, 185, 134, 1), 240px 290px 0 0 rgba(222, 185, 134, 1),
  245px 290px 0 0 rgba(222, 185, 134, 1), 250px 290px 0 0 rgba(222, 185, 134, 1),
  255px 290px 0 0 rgba(222, 185, 134, 1), 260px 290px 0 0 rgba(222, 185, 134, 1),
  265px 290px 0 0 rgba(222, 185, 134, 1), 270px 290px 0 0 rgba(222, 185, 134, 1),
  275px 290px 0 0 rgba(222, 185, 134, 1), 280px 290px 0 0 rgba(222, 185, 134, 1),
  285px 290px 0 0 rgba(222, 185, 134, 1), 290px 290px 0 0 rgba(222, 185, 134, 1),
  295px 290px 0 0 rgba(222, 185, 134, 1), 300px 290px 0 0 rgba(222, 185, 134, 1),
  305px 290px 0 0 rgba(222, 185, 134, 1), 310px 290px 0 0 rgba(222, 185, 134, 1),
  315px 290px 0 0 rgba(222, 185, 134, 1), 320px 290px 0 0 rgba(222, 185, 134, 1),
  325px 290px 0 0 rgba(222, 185, 134, 1), 330px 290px 0 0 rgba(222, 185, 134, 1),
  335px 290px 0 0 rgba(222, 185, 134, 1), 340px 290px 0 0 rgba(222, 185, 134, 1),
  345px 290px 0 0 rgba(222, 185, 134, 1), 350px 290px 0 0 rgba(222, 185, 134, 1),
  355px 290px 0 0 rgba(222, 185, 134, 1), 360px 290px 0 0 rgba(222, 185, 134, 1),
  365px 290px 0 0 rgba(222, 185, 134, 1), 370px 290px 0 0 rgba(222, 185, 134, 1),
  375px 290px 0 0 rgba(222, 185, 134, 1), 380px 290px 0 0 rgba(222, 185, 134, 1),
  385px 290px 0 0 rgba(222, 185, 134, 1), 390px 290px 0 0 rgba(222, 185, 134, 1),
  395px 290px 0 0 rgba(222, 185, 134, 1), 400px 290px 0 0 rgba(222, 185, 134, 1),
  405px 290px 0 0 rgba(222, 185, 134, 1), 410px 290px 0 0 rgba(222, 185, 134, 1),
  415px 290px 0 0 rgba(222, 185, 134, 1), 420px 290px 0 0 rgba(222, 185, 134, 1),
  425px 290px 0 0 rgba(222, 185, 134, 1), 430px 290px 0 0 rgba(222, 185, 134, 1),
  435px 290px 0 0 rgba(222, 185, 134, 1), 440px 290px 0 0 rgba(222, 185, 134, 1),
  445px 290px 0 0 rgba(222, 185, 134, 1), 450px 290px 0 0 rgba(222, 185, 134, 1),
  455px 290px 0 0 rgba(222, 185, 134, 1), 460px 290px 0 0 rgba(222, 185, 134, 1),
  465px 290px 0 0 rgba(222, 185, 134, 1), 470px 290px 0 0 rgba(222, 185, 134, 1),
  475px 290px 0 0 rgba(222, 185, 134, 1), 480px 290px 0 0 rgba(222, 185, 134, 1),
  485px 290px 0 0 rgba(222, 185, 134, 1), 490px 290px 0 0 rgba(222, 185, 134, 1),
  495px 290px 0 0 rgba(222, 185, 134, 1), 500px 290px 0 0 rgba(222, 185, 134, 1),
  505px 290px 0 0 rgba(222, 185, 134, 1), 510px 290px 0 0 rgba(222, 185, 134, 1),
  515px 290px 0 0 rgba(222, 185, 134, 1), 520px 290px 0 0 rgba(222, 185, 134, 1),
  525px 290px 0 0 rgba(222, 185, 134, 1), 530px 290px 0 0 rgba(222, 185, 134, 1),
  535px 290px 0 0 rgba(222, 185, 134, 1), 540px 290px 0 0 rgba(222, 185, 134, 1),
  545px 290px 0 0 rgba(222, 185, 134, 1), 550px 290px 0 0 rgba(222, 185, 134, 1),
  555px 290px 0 0 rgba(222, 185, 134, 1), 560px 290px 0 0 rgba(222, 185, 134, 1),
  565px 290px 0 0 rgba(222, 185, 134, 1), 570px 290px 0 0 rgba(222, 185, 134, 1),
  575px 290px 0 0 rgba(222, 185, 134, 1), 580px 290px 0 0 rgba(222, 185, 134, 1),
  585px 290px 0 0 rgba(222, 185, 134, 1), 590px 290px 0 0 rgba(222, 185, 134, 1),
  595px 290px 0 0 rgba(222, 185, 134, 1), 600px 290px 0 0 rgba(222, 185, 134, 1),
  605px 290px 0 0 rgba(222, 185, 134, 1), 610px 290px 0 0 rgba(222, 185, 134, 1),
  615px 290px 0 0 rgba(222, 185, 134, 1), 620px 290px 0 0 rgba(222, 185, 134, 1),
  625px 290px 0 0 rgba(222, 185, 134, 1), 630px 290px 0 0 rgba(222, 185, 134, 1),
  635px 290px 0 0 rgba(222, 185, 134, 1), 640px 290px 0 0 rgba(222, 185, 134, 1),
  645px 290px 0 0 rgba(222, 185, 134, 1), 650px 290px 0 0 rgba(222, 185, 134, 1),
  655px 290px 0 0 rgba(222, 185, 134, 1), 660px 290px 0 0 rgba(222, 185, 134, 1),
  665px 290px 0 0 rgba(222, 185, 134, 1), 670px 290px 0 0 rgba(222, 185, 134, 1),
  675px 290px 0 0 rgba(222, 185, 134, 1), 680px 290px 0 0 rgba(222, 185, 134, 1),
  685px 290px 0 0 rgba(203, 109, 181, 1), 690px 290px 0 0 rgba(255, 205, 234, 1),
  695px 290px 0 0 rgba(255, 205, 234, 1), 700px 290px 0 0 rgba(168, 90, 150, 1),
  705px 290px 0 0 rgba(203, 109, 181, 1), 5px 295px 0 0 rgba(203, 109, 181, 1),
  10px 295px 0 0 rgba(252, 231, 243, 1), 15px 295px 0 0 rgba(255, 205, 234, 1),
  20px 295px 0 0 rgba(255, 205, 234, 1), 25px 295px 0 0 rgba(203, 109, 181, 1),
  85px 295px 0 0 rgba(222, 185, 134, 1), 90px 295px 0 0 rgba(222, 185, 134, 1),
  225px 295px 0 0 rgba(222, 185, 134, 1), 230px 295px 0 0 rgba(222, 185, 134, 1),
  330px 295px 0 0 rgba(222, 185, 134, 1), 410px 295px 0 0 rgba(110, 205, 199, 1),
  415px 295px 0 0 rgba(110, 205, 199, 1), 525px 295px 0 0 rgba(110, 205, 199, 1),
  530px 295px 0 0 rgba(110, 205, 199, 1), 630px 295px 0 0 rgba(110, 205, 199, 1),
  635px 295px 0 0 rgba(110, 205, 199, 1), 685px 295px 0 0 rgba(203, 109, 181, 1),
  690px 295px 0 0 rgba(255, 205, 234, 1), 695px 295px 0 0 rgba(255, 205, 234, 1),
  700px 295px 0 0 rgba(168, 90, 150, 1), 705px 295px 0 0 rgba(203, 109, 181, 1),
  5px 300px 0 0 rgba(203, 109, 181, 1), 10px 300px 0 0 rgba(252, 231, 243, 1),
  15px 300px 0 0 rgba(255, 205, 234, 1), 20px 300px 0 0 rgba(255, 205, 234, 1),
  25px 300px 0 0 rgba(203, 109, 181, 1), 75px 300px 0 0 rgba(222, 185, 134, 1),
  80px 300px 0 0 rgba(222, 185, 134, 1), 220px 300px 0 0 rgba(222, 185, 134, 1),
  225px 300px 0 0 rgba(222, 185, 134, 1), 330px 300px 0 0 rgba(222, 185, 134, 1),
  415px 300px 0 0 rgba(110, 205, 199, 1), 420px 300px 0 0 rgba(110, 205, 199, 1),
  535px 300px 0 0 rgba(110, 205, 199, 1), 540px 300px 0 0 rgba(110, 205, 199, 1),
  640px 300px 0 0 rgba(110, 205, 199, 1), 645px 300px 0 0 rgba(110, 205, 199, 1),
  685px 300px 0 0 rgba(203, 109, 181, 1), 690px 300px 0 0 rgba(255, 205, 234, 1),
  695px 300px 0 0 rgba(255, 205, 234, 1), 700px 300px 0 0 rgba(168, 90, 150, 1),
  705px 300px 0 0 rgba(203, 109, 181, 1), 5px 305px 0 0 rgba(203, 109, 181, 1),
  10px 305px 0 0 rgba(252, 231, 243, 1), 15px 305px 0 0 rgba(255, 205, 234, 1),
  20px 305px 0 0 rgba(255, 205, 234, 1), 25px 305px 0 0 rgba(203, 109, 181, 1),
  65px 305px 0 0 rgba(222, 185, 134, 1), 70px 305px 0 0 rgba(222, 185, 134, 1),
  215px 305px 0 0 rgba(110, 205, 199, 1), 220px 305px 0 0 rgba(110, 205, 199, 1),
  330px 305px 0 0 rgba(110, 205, 199, 1), 420px 305px 0 0 rgba(110, 205, 199, 1),
  425px 305px 0 0 rgba(110, 205, 199, 1), 545px 305px 0 0 rgba(110, 205, 199, 1),
  550px 305px 0 0 rgba(110, 205, 199, 1), 650px 305px 0 0 rgba(110, 205, 199, 1),
  655px 305px 0 0 rgba(110, 205, 199, 1), 685px 305px 0 0 rgba(203, 109, 181, 1),
  690px 305px 0 0 rgba(255, 205, 234, 1), 695px 305px 0 0 rgba(255, 205, 234, 1),
  700px 305px 0 0 rgba(168, 90, 150, 1), 705px 305px 0 0 rgba(203, 109, 181, 1),
  5px 310px 0 0 rgba(203, 109, 181, 1), 10px 310px 0 0 rgba(252, 231, 243, 1),
  15px 310px 0 0 rgba(255, 205, 234, 1), 20px 310px 0 0 rgba(255, 205, 234, 1),
  25px 310px 0 0 rgba(203, 109, 181, 1), 55px 310px 0 0 rgba(222, 185, 134, 1),
  60px 310px 0 0 rgba(222, 185, 134, 1), 210px 310px 0 0 rgba(110, 205, 199, 1),
  215px 310px 0 0 rgba(110, 205, 199, 1), 330px 310px 0 0 rgba(110, 205, 199, 1),
  425px 310px 0 0 rgba(110, 205, 199, 1), 430px 310px 0 0 rgba(110, 205, 199, 1),
  555px 310px 0 0 rgba(110, 205, 199, 1), 560px 310px 0 0 rgba(110, 205, 199, 1),
  660px 310px 0 0 rgba(110, 205, 199, 1), 665px 310px 0 0 rgba(110, 205, 199, 1),
  685px 310px 0 0 rgba(203, 109, 181, 1), 690px 310px 0 0 rgba(255, 205, 234, 1),
  695px 310px 0 0 rgba(255, 205, 234, 1), 700px 310px 0 0 rgba(168, 90, 150, 1),
  705px 310px 0 0 rgba(203, 109, 181, 1), 5px 315px 0 0 rgba(203, 109, 181, 1),
  10px 315px 0 0 rgba(252, 231, 243, 1), 15px 315px 0 0 rgba(255, 205, 234, 1),
  20px 315px 0 0 rgba(255, 205, 234, 1), 25px 315px 0 0 rgba(203, 109, 181, 1),
  45px 315px 0 0 rgba(222, 185, 134, 1), 50px 315px 0 0 rgba(222, 185, 134, 1),
  205px 315px 0 0 rgba(110, 205, 199, 1), 210px 315px 0 0 rgba(110, 205, 199, 1),
  330px 315px 0 0 rgba(110, 205, 199, 1), 430px 315px 0 0 rgba(110, 205, 199, 1),
  435px 315px 0 0 rgba(110, 205, 199, 1), 565px 315px 0 0 rgba(110, 205, 199, 1),
  570px 315px 0 0 rgba(110, 205, 199, 1), 670px 315px 0 0 rgba(110, 205, 199, 1),
  675px 315px 0 0 rgba(110, 205, 199, 1), 685px 315px 0 0 rgba(203, 109, 181, 1),
  690px 315px 0 0 rgba(255, 205, 234, 1), 695px 315px 0 0 rgba(255, 205, 234, 1),
  700px 315px 0 0 rgba(168, 90, 150, 1), 705px 315px 0 0 rgba(203, 109, 181, 1),
  5px 320px 0 0 rgba(203, 109, 181, 1), 10px 320px 0 0 rgba(252, 231, 243, 1),
  15px 320px 0 0 rgba(255, 205, 234, 1), 20px 320px 0 0 rgba(255, 205, 234, 1),
  25px 320px 0 0 rgba(203, 109, 181, 1), 35px 320px 0 0 rgba(110, 205, 199, 1),
  40px 320px 0 0 rgba(110, 205, 199, 1), 200px 320px 0 0 rgba(110, 205, 199, 1),
  205px 320px 0 0 rgba(110, 205, 199, 1), 330px 320px 0 0 rgba(110, 205, 199, 1),
  435px 320px 0 0 rgba(110, 205, 199, 1), 440px 320px 0 0 rgba(110, 205, 199, 1),
  575px 320px 0 0 rgba(110, 205, 199, 1), 580px 320px 0 0 rgba(110, 205, 199, 1),
  680px 320px 0 0 rgba(110, 205, 199, 1), 685px 320px 0 0 rgba(203, 109, 181, 1),
  690px 320px 0 0 rgba(255, 205, 234, 1), 695px 320px 0 0 rgba(255, 205, 234, 1),
  700px 320px 0 0 rgba(168, 90, 150, 1), 705px 320px 0 0 rgba(203, 109, 181, 1),
  5px 325px 0 0 rgba(203, 109, 181, 1), 10px 325px 0 0 rgba(252, 231, 243, 1),
  15px 325px 0 0 rgba(255, 205, 234, 1), 20px 325px 0 0 rgba(255, 205, 234, 1),
  25px 325px 0 0 rgba(203, 109, 181, 1), 30px 325px 0 0 rgba(110, 205, 199, 1),
  195px 325px 0 0 rgba(110, 205, 199, 1), 200px 325px 0 0 rgba(110, 205, 199, 1),
  330px 325px 0 0 rgba(110, 205, 199, 1), 440px 325px 0 0 rgba(110, 205, 199, 1),
  445px 325px 0 0 rgba(110, 205, 199, 1), 585px 325px 0 0 rgba(110, 205, 199, 1),
  590px 325px 0 0 rgba(110, 205, 199, 1), 685px 325px 0 0 rgba(203, 109, 181, 1),
  690px 325px 0 0 rgba(255, 205, 234, 1), 695px 325px 0 0 rgba(255, 205, 234, 1),
  700px 325px 0 0 rgba(168, 90, 150, 1), 705px 325px 0 0 rgba(203, 109, 181, 1),
  5px 330px 0 0 rgba(203, 109, 181, 1), 10px 330px 0 0 rgba(252, 231, 243, 1),
  15px 330px 0 0 rgba(255, 205, 234, 1), 20px 330px 0 0 rgba(255, 205, 234, 1),
  25px 330px 0 0 rgba(203, 109, 181, 1), 190px 330px 0 0 rgba(110, 205, 199, 1),
  195px 330px 0 0 rgba(110, 205, 199, 1), 330px 330px 0 0 rgba(110, 205, 199, 1),
  445px 330px 0 0 rgba(110, 205, 199, 1), 450px 330px 0 0 rgba(110, 205, 199, 1),
  595px 330px 0 0 rgba(110, 205, 199, 1), 600px 330px 0 0 rgba(110, 205, 199, 1),
  685px 330px 0 0 rgba(203, 109, 181, 1), 690px 330px 0 0 rgba(255, 205, 234, 1),
  695px 330px 0 0 rgba(255, 205, 234, 1), 700px 330px 0 0 rgba(168, 90, 150, 1),
  705px 330px 0 0 rgba(203, 109, 181, 1), 5px 335px 0 0 rgba(203, 109, 181, 1),
  10px 335px 0 0 rgba(252, 231, 243, 1), 15px 335px 0 0 rgba(255, 205, 234, 1),
  20px 335px 0 0 rgba(255, 205, 234, 1), 25px 335px 0 0 rgba(203, 109, 181, 1),
  30px 335px 0 0 rgba(110, 205, 199, 1), 35px 335px 0 0 rgba(110, 205, 199, 1),
  40px 335px 0 0 rgba(110, 205, 199, 1), 45px 335px 0 0 rgba(110, 205, 199, 1),
  50px 335px 0 0 rgba(110, 205, 199, 1), 55px 335px 0 0 rgba(110, 205, 199, 1),
  60px 335px 0 0 rgba(110, 205, 199, 1), 65px 335px 0 0 rgba(110, 205, 199, 1),
  70px 335px 0 0 rgba(110, 205, 199, 1), 75px 335px 0 0 rgba(110, 205, 199, 1),
  80px 335px 0 0 rgba(110, 205, 199, 1), 85px 335px 0 0 rgba(110, 205, 199, 1),
  90px 335px 0 0 rgba(110, 205, 199, 1), 95px 335px 0 0 rgba(110, 205, 199, 1),
  100px 335px 0 0 rgba(110, 205, 199, 1), 105px 335px 0 0 rgba(110, 205, 199, 1),
  110px 335px 0 0 rgba(110, 205, 199, 1), 115px 335px 0 0 rgba(110, 205, 199, 1),
  120px 335px 0 0 rgba(110, 205, 199, 1), 125px 335px 0 0 rgba(110, 205, 199, 1),
  130px 335px 0 0 rgba(110, 205, 199, 1), 135px 335px 0 0 rgba(110, 205, 199, 1),
  140px 335px 0 0 rgba(110, 205, 199, 1), 145px 335px 0 0 rgba(110, 205, 199, 1),
  150px 335px 0 0 rgba(110, 205, 199, 1), 155px 335px 0 0 rgba(110, 205, 199, 1),
  160px 335px 0 0 rgba(110, 205, 199, 1), 165px 335px 0 0 rgba(110, 205, 199, 1),
  170px 335px 0 0 rgba(110, 205, 199, 1), 175px 335px 0 0 rgba(110, 205, 199, 1),
  180px 335px 0 0 rgba(110, 205, 199, 1), 185px 335px 0 0 rgba(110, 205, 199, 1),
  190px 335px 0 0 rgba(110, 205, 199, 1), 195px 335px 0 0 rgba(110, 205, 199, 1),
  200px 335px 0 0 rgba(110, 205, 199, 1), 205px 335px 0 0 rgba(110, 205, 199, 1),
  210px 335px 0 0 rgba(110, 205, 199, 1), 215px 335px 0 0 rgba(110, 205, 199, 1),
  220px 335px 0 0 rgba(110, 205, 199, 1), 225px 335px 0 0 rgba(110, 205, 199, 1),
  230px 335px 0 0 rgba(110, 205, 199, 1), 235px 335px 0 0 rgba(110, 205, 199, 1),
  240px 335px 0 0 rgba(110, 205, 199, 1), 245px 335px 0 0 rgba(110, 205, 199, 1),
  250px 335px 0 0 rgba(110, 205, 199, 1), 255px 335px 0 0 rgba(110, 205, 199, 1),
  260px 335px 0 0 rgba(110, 205, 199, 1), 265px 335px 0 0 rgba(110, 205, 199, 1),
  270px 335px 0 0 rgba(110, 205, 199, 1), 275px 335px 0 0 rgba(110, 205, 199, 1),
  280px 335px 0 0 rgba(110, 205, 199, 1), 285px 335px 0 0 rgba(110, 205, 199, 1),
  290px 335px 0 0 rgba(110, 205, 199, 1), 295px 335px 0 0 rgba(110, 205, 199, 1),
  300px 335px 0 0 rgba(110, 205, 199, 1), 305px 335px 0 0 rgba(110, 205, 199, 1),
  310px 335px 0 0 rgba(110, 205, 199, 1), 315px 335px 0 0 rgba(110, 205, 199, 1),
  320px 335px 0 0 rgba(110, 205, 199, 1), 325px 335px 0 0 rgba(110, 205, 199, 1),
  330px 335px 0 0 rgba(110, 205, 199, 1), 335px 335px 0 0 rgba(110, 205, 199, 1),
  340px 335px 0 0 rgba(110, 205, 199, 1), 345px 335px 0 0 rgba(110, 205, 199, 1),
  350px 335px 0 0 rgba(110, 205, 199, 1), 355px 335px 0 0 rgba(110, 205, 199, 1),
  360px 335px 0 0 rgba(110, 205, 199, 1), 365px 335px 0 0 rgba(110, 205, 199, 1),
  370px 335px 0 0 rgba(110, 205, 199, 1), 375px 335px 0 0 rgba(110, 205, 199, 1),
  380px 335px 0 0 rgba(110, 205, 199, 1), 385px 335px 0 0 rgba(110, 205, 199, 1),
  390px 335px 0 0 rgba(110, 205, 199, 1), 395px 335px 0 0 rgba(110, 205, 199, 1),
  400px 335px 0 0 rgba(110, 205, 199, 1), 405px 335px 0 0 rgba(110, 205, 199, 1),
  410px 335px 0 0 rgba(110, 205, 199, 1), 415px 335px 0 0 rgba(110, 205, 199, 1),
  420px 335px 0 0 rgba(110, 205, 199, 1), 425px 335px 0 0 rgba(110, 205, 199, 1),
  430px 335px 0 0 rgba(110, 205, 199, 1), 435px 335px 0 0 rgba(110, 205, 199, 1),
  440px 335px 0 0 rgba(110, 205, 199, 1), 445px 335px 0 0 rgba(110, 205, 199, 1),
  450px 335px 0 0 rgba(110, 205, 199, 1), 455px 335px 0 0 rgba(110, 205, 199, 1),
  460px 335px 0 0 rgba(110, 205, 199, 1), 465px 335px 0 0 rgba(110, 205, 199, 1),
  470px 335px 0 0 rgba(110, 205, 199, 1), 475px 335px 0 0 rgba(110, 205, 199, 1),
  480px 335px 0 0 rgba(110, 205, 199, 1), 485px 335px 0 0 rgba(110, 205, 199, 1),
  490px 335px 0 0 rgba(110, 205, 199, 1), 495px 335px 0 0 rgba(110, 205, 199, 1),
  500px 335px 0 0 rgba(110, 205, 199, 1), 505px 335px 0 0 rgba(110, 205, 199, 1),
  510px 335px 0 0 rgba(110, 205, 199, 1), 515px 335px 0 0 rgba(110, 205, 199, 1),
  520px 335px 0 0 rgba(110, 205, 199, 1), 525px 335px 0 0 rgba(110, 205, 199, 1),
  530px 335px 0 0 rgba(110, 205, 199, 1), 535px 335px 0 0 rgba(110, 205, 199, 1),
  540px 335px 0 0 rgba(110, 205, 199, 1), 545px 335px 0 0 rgba(110, 205, 199, 1),
  550px 335px 0 0 rgba(110, 205, 199, 1), 555px 335px 0 0 rgba(110, 205, 199, 1),
  560px 335px 0 0 rgba(110, 205, 199, 1), 565px 335px 0 0 rgba(110, 205, 199, 1),
  570px 335px 0 0 rgba(110, 205, 199, 1), 575px 335px 0 0 rgba(110, 205, 199, 1),
  580px 335px 0 0 rgba(110, 205, 199, 1), 585px 335px 0 0 rgba(110, 205, 199, 1),
  590px 335px 0 0 rgba(110, 205, 199, 1), 595px 335px 0 0 rgba(110, 205, 199, 1),
  600px 335px 0 0 rgba(110, 205, 199, 1), 605px 335px 0 0 rgba(110, 205, 199, 1),
  610px 335px 0 0 rgba(110, 205, 199, 1), 615px 335px 0 0 rgba(110, 205, 199, 1),
  620px 335px 0 0 rgba(110, 205, 199, 1), 625px 335px 0 0 rgba(110, 205, 199, 1),
  630px 335px 0 0 rgba(110, 205, 199, 1), 635px 335px 0 0 rgba(110, 205, 199, 1),
  640px 335px 0 0 rgba(110, 205, 199, 1), 645px 335px 0 0 rgba(110, 205, 199, 1),
  650px 335px 0 0 rgba(110, 205, 199, 1), 655px 335px 0 0 rgba(110, 205, 199, 1),
  660px 335px 0 0 rgba(110, 205, 199, 1), 665px 335px 0 0 rgba(110, 205, 199, 1),
  670px 335px 0 0 rgba(110, 205, 199, 1), 675px 335px 0 0 rgba(110, 205, 199, 1),
  680px 335px 0 0 rgba(110, 205, 199, 1), 685px 335px 0 0 rgba(203, 109, 181, 1),
  690px 335px 0 0 rgba(255, 205, 234, 1), 695px 335px 0 0 rgba(255, 205, 234, 1),
  700px 335px 0 0 rgba(168, 90, 150, 1), 705px 335px 0 0 rgba(203, 109, 181, 1),
  5px 340px 0 0 rgba(203, 109, 181, 1), 10px 340px 0 0 rgba(252, 231, 243, 1),
  15px 340px 0 0 rgba(255, 205, 234, 1), 20px 340px 0 0 rgba(255, 205, 234, 1),
  25px 340px 0 0 rgba(203, 109, 181, 1), 180px 340px 0 0 rgba(110, 205, 199, 1),
  185px 340px 0 0 rgba(110, 205, 199, 1), 330px 340px 0 0 rgba(110, 205, 199, 1),
  455px 340px 0 0 rgba(110, 205, 199, 1), 460px 340px 0 0 rgba(110, 205, 199, 1),
  610px 340px 0 0 rgba(110, 205, 199, 1), 615px 340px 0 0 rgba(110, 205, 199, 1),
  685px 340px 0 0 rgba(203, 109, 181, 1), 690px 340px 0 0 rgba(255, 205, 234, 1),
  695px 340px 0 0 rgba(255, 205, 234, 1), 700px 340px 0 0 rgba(168, 90, 150, 1),
  705px 340px 0 0 rgba(203, 109, 181, 1), 5px 345px 0 0 rgba(203, 109, 181, 1),
  10px 345px 0 0 rgba(252, 231, 243, 1), 15px 345px 0 0 rgba(255, 205, 234, 1),
  20px 345px 0 0 rgba(255, 205, 234, 1), 25px 345px 0 0 rgba(203, 109, 181, 1),
  175px 345px 0 0 rgba(110, 205, 199, 1), 180px 345px 0 0 rgba(110, 205, 199, 1),
  330px 345px 0 0 rgba(110, 205, 199, 1), 460px 345px 0 0 rgba(110, 205, 199, 1),
  465px 345px 0 0 rgba(110, 205, 199, 1), 620px 345px 0 0 rgba(110, 205, 199, 1),
  625px 345px 0 0 rgba(110, 205, 199, 1), 685px 345px 0 0 rgba(203, 109, 181, 1),
  690px 345px 0 0 rgba(255, 205, 234, 1), 695px 345px 0 0 rgba(255, 205, 234, 1),
  700px 345px 0 0 rgba(168, 90, 150, 1), 705px 345px 0 0 rgba(203, 109, 181, 1),
  5px 350px 0 0 rgba(203, 109, 181, 1), 10px 350px 0 0 rgba(252, 231, 243, 1),
  15px 350px 0 0 rgba(255, 205, 234, 1), 20px 350px 0 0 rgba(255, 205, 234, 1),
  25px 350px 0 0 rgba(203, 109, 181, 1), 170px 350px 0 0 rgba(110, 205, 199, 1),
  175px 350px 0 0 rgba(110, 205, 199, 1), 330px 350px 0 0 rgba(110, 205, 199, 1),
  465px 350px 0 0 rgba(110, 205, 199, 1), 470px 350px 0 0 rgba(110, 205, 199, 1),
  630px 350px 0 0 rgba(110, 205, 199, 1), 635px 350px 0 0 rgba(110, 205, 199, 1),
  685px 350px 0 0 rgba(203, 109, 181, 1), 690px 350px 0 0 rgba(255, 205, 234, 1),
  695px 350px 0 0 rgba(255, 205, 234, 1), 700px 350px 0 0 rgba(168, 90, 150, 1),
  705px 350px 0 0 rgba(203, 109, 181, 1), 5px 355px 0 0 rgba(203, 109, 181, 1),
  10px 355px 0 0 rgba(252, 231, 243, 1), 15px 355px 0 0 rgba(255, 205, 234, 1),
  20px 355px 0 0 rgba(255, 205, 234, 1), 25px 355px 0 0 rgba(203, 109, 181, 1),
  165px 355px 0 0 rgba(110, 205, 199, 1), 170px 355px 0 0 rgba(110, 205, 199, 1),
  330px 355px 0 0 rgba(110, 205, 199, 1), 470px 355px 0 0 rgba(110, 205, 199, 1),
  475px 355px 0 0 rgba(110, 205, 199, 1), 640px 355px 0 0 rgba(110, 205, 199, 1),
  645px 355px 0 0 rgba(110, 205, 199, 1), 685px 355px 0 0 rgba(203, 109, 181, 1),
  690px 355px 0 0 rgba(255, 205, 234, 1), 695px 355px 0 0 rgba(255, 205, 234, 1),
  700px 355px 0 0 rgba(168, 90, 150, 1), 705px 355px 0 0 rgba(203, 109, 181, 1),
  5px 360px 0 0 rgba(203, 109, 181, 1), 10px 360px 0 0 rgba(252, 231, 243, 1),
  15px 360px 0 0 rgba(255, 205, 234, 1), 20px 360px 0 0 rgba(255, 205, 234, 1),
  25px 360px 0 0 rgba(203, 109, 181, 1), 160px 360px 0 0 rgba(110, 205, 199, 1),
  165px 360px 0 0 rgba(110, 205, 199, 1), 330px 360px 0 0 rgba(191, 93, 157, 1),
  475px 360px 0 0 rgba(110, 205, 199, 1), 480px 360px 0 0 rgba(110, 205, 199, 1),
  650px 360px 0 0 rgba(110, 205, 199, 1), 655px 360px 0 0 rgba(110, 205, 199, 1),
  685px 360px 0 0 rgba(203, 109, 181, 1), 690px 360px 0 0 rgba(255, 205, 234, 1),
  695px 360px 0 0 rgba(255, 205, 234, 1), 700px 360px 0 0 rgba(168, 90, 150, 1),
  705px 360px 0 0 rgba(203, 109, 181, 1), 5px 365px 0 0 rgba(203, 109, 181, 1),
  10px 365px 0 0 rgba(252, 231, 243, 1), 15px 365px 0 0 rgba(255, 205, 234, 1),
  20px 365px 0 0 rgba(255, 205, 234, 1), 25px 365px 0 0 rgba(203, 109, 181, 1),
  155px 365px 0 0 rgba(191, 93, 157, 1), 160px 365px 0 0 rgba(191, 93, 157, 1),
  330px 365px 0 0 rgba(110, 205, 199, 1), 480px 365px 0 0 rgba(110, 205, 199, 1),
  485px 365px 0 0 rgba(110, 205, 199, 1), 660px 365px 0 0 rgba(110, 205, 199, 1),
  665px 365px 0 0 rgba(110, 205, 199, 1), 685px 365px 0 0 rgba(203, 109, 181, 1),
  690px 365px 0 0 rgba(255, 205, 234, 1), 695px 365px 0 0 rgba(255, 205, 234, 1),
  700px 365px 0 0 rgba(168, 90, 150, 1), 705px 365px 0 0 rgba(203, 109, 181, 1),
  5px 370px 0 0 rgba(203, 109, 181, 1), 10px 370px 0 0 rgba(252, 231, 243, 1),
  15px 370px 0 0 rgba(255, 205, 234, 1), 20px 370px 0 0 rgba(255, 205, 234, 1),
  25px 370px 0 0 rgba(203, 109, 181, 1), 150px 370px 0 0 rgba(191, 93, 157, 1),
  155px 370px 0 0 rgba(191, 93, 157, 1), 330px 370px 0 0 rgba(191, 93, 157, 1),
  485px 370px 0 0 rgba(191, 93, 157, 1), 490px 370px 0 0 rgba(191, 93, 157, 1),
  670px 370px 0 0 rgba(110, 205, 199, 1), 675px 370px 0 0 rgba(110, 205, 199, 1),
  685px 370px 0 0 rgba(203, 109, 181, 1), 690px 370px 0 0 rgba(255, 205, 234, 1),
  695px 370px 0 0 rgba(255, 205, 234, 1), 700px 370px 0 0 rgba(168, 90, 150, 1),
  705px 370px 0 0 rgba(203, 109, 181, 1), 5px 375px 0 0 rgba(203, 109, 181, 1),
  10px 375px 0 0 rgba(252, 231, 243, 1), 15px 375px 0 0 rgba(255, 205, 234, 1),
  20px 375px 0 0 rgba(255, 205, 234, 1), 25px 375px 0 0 rgba(203, 109, 181, 1),
  145px 375px 0 0 rgba(191, 93, 157, 1), 150px 375px 0 0 rgba(191, 93, 157, 1),
  330px 375px 0 0 rgba(110, 205, 199, 1), 490px 375px 0 0 rgba(191, 93, 157, 1),
  495px 375px 0 0 rgba(191, 93, 157, 1), 680px 375px 0 0 rgba(110, 205, 199, 1),
  685px 375px 0 0 rgba(203, 109, 181, 1), 690px 375px 0 0 rgba(255, 205, 234, 1),
  695px 375px 0 0 rgba(255, 205, 234, 1), 700px 375px 0 0 rgba(168, 90, 150, 1),
  705px 375px 0 0 rgba(203, 109, 181, 1), 5px 380px 0 0 rgba(203, 109, 181, 1),
  10px 380px 0 0 rgba(252, 231, 243, 1), 15px 380px 0 0 rgba(255, 205, 234, 1),
  20px 380px 0 0 rgba(255, 205, 234, 1), 25px 380px 0 0 rgba(203, 109, 181, 1),
  140px 380px 0 0 rgba(191, 93, 157, 1), 145px 380px 0 0 rgba(191, 93, 157, 1),
  330px 380px 0 0 rgba(110, 205, 199, 1), 495px 380px 0 0 rgba(191, 93, 157, 1),
  500px 380px 0 0 rgba(191, 93, 157, 1), 685px 380px 0 0 rgba(203, 109, 181, 1),
  690px 380px 0 0 rgba(255, 205, 234, 1), 695px 380px 0 0 rgba(255, 205, 234, 1),
  700px 380px 0 0 rgba(168, 90, 150, 1), 705px 380px 0 0 rgba(203, 109, 181, 1),
  5px 385px 0 0 rgba(203, 109, 181, 1), 10px 385px 0 0 rgba(252, 231, 243, 1),
  15px 385px 0 0 rgba(255, 205, 234, 1), 20px 385px 0 0 rgba(255, 205, 234, 1),
  25px 385px 0 0 rgba(203, 109, 181, 1), 135px 385px 0 0 rgba(191, 93, 157, 1),
  140px 385px 0 0 rgba(191, 93, 157, 1), 330px 385px 0 0 rgba(191, 93, 157, 1),
  500px 385px 0 0 rgba(191, 93, 157, 1), 505px 385px 0 0 rgba(191, 93, 157, 1),
  685px 385px 0 0 rgba(203, 109, 181, 1), 690px 385px 0 0 rgba(255, 205, 234, 1),
  695px 385px 0 0 rgba(255, 205, 234, 1), 700px 385px 0 0 rgba(168, 90, 150, 1),
  705px 385px 0 0 rgba(203, 109, 181, 1), 5px 390px 0 0 rgba(203, 109, 181, 1),
  10px 390px 0 0 rgba(252, 231, 243, 1), 15px 390px 0 0 rgba(255, 205, 234, 1),
  20px 390px 0 0 rgba(255, 205, 234, 1), 25px 390px 0 0 rgba(203, 109, 181, 1),
  130px 390px 0 0 rgba(191, 93, 157, 1), 135px 390px 0 0 rgba(191, 93, 157, 1),
  330px 390px 0 0 rgba(191, 93, 157, 1), 505px 390px 0 0 rgba(191, 93, 157, 1),
  510px 390px 0 0 rgba(191, 93, 157, 1), 685px 390px 0 0 rgba(203, 109, 181, 1),
  690px 390px 0 0 rgba(255, 205, 234, 1), 695px 390px 0 0 rgba(255, 205, 234, 1),
  700px 390px 0 0 rgba(168, 90, 150, 1), 705px 390px 0 0 rgba(203, 109, 181, 1),
  5px 395px 0 0 rgba(203, 109, 181, 1), 10px 395px 0 0 rgba(252, 231, 243, 1),
  15px 395px 0 0 rgba(255, 205, 234, 1), 20px 395px 0 0 rgba(255, 205, 234, 1),
  25px 395px 0 0 rgba(203, 109, 181, 1), 125px 395px 0 0 rgba(191, 93, 157, 1),
  130px 395px 0 0 rgba(191, 93, 157, 1), 330px 395px 0 0 rgba(191, 93, 157, 1),
  510px 395px 0 0 rgba(191, 93, 157, 1), 515px 395px 0 0 rgba(191, 93, 157, 1),
  685px 395px 0 0 rgba(203, 109, 181, 1), 690px 395px 0 0 rgba(255, 205, 234, 1),
  695px 395px 0 0 rgba(255, 205, 234, 1), 700px 395px 0 0 rgba(168, 90, 150, 1),
  705px 395px 0 0 rgba(203, 109, 181, 1), 5px 400px 0 0 rgba(203, 109, 181, 1),
  10px 400px 0 0 rgba(252, 231, 243, 1), 15px 400px 0 0 rgba(255, 205, 234, 1),
  20px 400px 0 0 rgba(255, 205, 234, 1), 25px 400px 0 0 rgba(203, 109, 181, 1),
  120px 400px 0 0 rgba(191, 93, 157, 1), 125px 400px 0 0 rgba(191, 93, 157, 1),
  330px 400px 0 0 rgba(191, 93, 157, 1), 515px 400px 0 0 rgba(191, 93, 157, 1),
  520px 400px 0 0 rgba(191, 93, 157, 1), 685px 400px 0 0 rgba(203, 109, 181, 1),
  690px 400px 0 0 rgba(255, 205, 234, 1), 695px 400px 0 0 rgba(255, 205, 234, 1),
  700px 400px 0 0 rgba(168, 90, 150, 1), 705px 400px 0 0 rgba(203, 109, 181, 1),
  5px 405px 0 0 rgba(203, 109, 181, 1), 10px 405px 0 0 rgba(252, 231, 243, 1),
  15px 405px 0 0 rgba(255, 205, 234, 1), 20px 405px 0 0 rgba(255, 205, 234, 1),
  25px 405px 0 0 rgba(203, 109, 181, 1), 115px 405px 0 0 rgba(191, 93, 157, 1),
  120px 405px 0 0 rgba(191, 93, 157, 1), 330px 405px 0 0 rgba(191, 93, 157, 1),
  520px 405px 0 0 rgba(191, 93, 157, 1), 685px 405px 0 0 rgba(203, 109, 181, 1),
  690px 405px 0 0 rgba(255, 205, 234, 1), 695px 405px 0 0 rgba(255, 205, 234, 1),
  700px 405px 0 0 rgba(168, 90, 150, 1), 705px 405px 0 0 rgba(203, 109, 181, 1),
  5px 410px 0 0 rgba(203, 109, 181, 1), 10px 410px 0 0 rgba(252, 231, 243, 1),
  15px 410px 0 0 rgba(255, 205, 234, 1), 20px 410px 0 0 rgba(255, 205, 234, 1),
  25px 410px 0 0 rgba(203, 109, 181, 1), 30px 410px 0 0 rgba(191, 93, 157, 1),
  35px 410px 0 0 rgba(191, 93, 157, 1), 40px 410px 0 0 rgba(191, 93, 157, 1),
  45px 410px 0 0 rgba(191, 93, 157, 1), 50px 410px 0 0 rgba(191, 93, 157, 1),
  55px 410px 0 0 rgba(191, 93, 157, 1), 60px 410px 0 0 rgba(191, 93, 157, 1),
  65px 410px 0 0 rgba(191, 93, 157, 1), 70px 410px 0 0 rgba(191, 93, 157, 1),
  75px 410px 0 0 rgba(191, 93, 157, 1), 80px 410px 0 0 rgba(191, 93, 157, 1),
  85px 410px 0 0 rgba(191, 93, 157, 1), 90px 410px 0 0 rgba(191, 93, 157, 1),
  95px 410px 0 0 rgba(191, 93, 157, 1), 100px 410px 0 0 rgba(191, 93, 157, 1),
  105px 410px 0 0 rgba(191, 93, 157, 1), 110px 410px 0 0 rgba(191, 93, 157, 1),
  115px 410px 0 0 rgba(191, 93, 157, 1), 120px 410px 0 0 rgba(191, 93, 157, 1),
  125px 410px 0 0 rgba(191, 93, 157, 1), 130px 410px 0 0 rgba(191, 93, 157, 1),
  135px 410px 0 0 rgba(191, 93, 157, 1), 140px 410px 0 0 rgba(191, 93, 157, 1),
  145px 410px 0 0 rgba(191, 93, 157, 1), 150px 410px 0 0 rgba(191, 93, 157, 1),
  155px 410px 0 0 rgba(191, 93, 157, 1), 160px 410px 0 0 rgba(191, 93, 157, 1),
  165px 410px 0 0 rgba(191, 93, 157, 1), 170px 410px 0 0 rgba(191, 93, 157, 1),
  175px 410px 0 0 rgba(191, 93, 157, 1), 180px 410px 0 0 rgba(191, 93, 157, 1),
  185px 410px 0 0 rgba(191, 93, 157, 1), 190px 410px 0 0 rgba(191, 93, 157, 1),
  195px 410px 0 0 rgba(191, 93, 157, 1), 200px 410px 0 0 rgba(191, 93, 157, 1),
  205px 410px 0 0 rgba(191, 93, 157, 1), 210px 410px 0 0 rgba(191, 93, 157, 1),
  215px 410px 0 0 rgba(191, 93, 157, 1), 220px 410px 0 0 rgba(191, 93, 157, 1),
  225px 410px 0 0 rgba(191, 93, 157, 1), 230px 410px 0 0 rgba(191, 93, 157, 1),
  235px 410px 0 0 rgba(191, 93, 157, 1), 240px 410px 0 0 rgba(191, 93, 157, 1),
  245px 410px 0 0 rgba(191, 93, 157, 1), 250px 410px 0 0 rgba(191, 93, 157, 1),
  255px 410px 0 0 rgba(191, 93, 157, 1), 260px 410px 0 0 rgba(191, 93, 157, 1),
  265px 410px 0 0 rgba(191, 93, 157, 1), 270px 410px 0 0 rgba(191, 93, 157, 1),
  275px 410px 0 0 rgba(191, 93, 157, 1), 280px 410px 0 0 rgba(191, 93, 157, 1),
  285px 410px 0 0 rgba(191, 93, 157, 1), 290px 410px 0 0 rgba(191, 93, 157, 1),
  295px 410px 0 0 rgba(191, 93, 157, 1), 300px 410px 0 0 rgba(191, 93, 157, 1),
  305px 410px 0 0 rgba(191, 93, 157, 1), 310px 410px 0 0 rgba(191, 93, 157, 1),
  315px 410px 0 0 rgba(191, 93, 157, 1), 320px 410px 0 0 rgba(191, 93, 157, 1),
  325px 410px 0 0 rgba(191, 93, 157, 1), 330px 410px 0 0 rgba(191, 93, 157, 1),
  335px 410px 0 0 rgba(191, 93, 157, 1), 340px 410px 0 0 rgba(191, 93, 157, 1),
  345px 410px 0 0 rgba(191, 93, 157, 1), 350px 410px 0 0 rgba(191, 93, 157, 1),
  355px 410px 0 0 rgba(191, 93, 157, 1), 360px 410px 0 0 rgba(191, 93, 157, 1),
  365px 410px 0 0 rgba(191, 93, 157, 1), 370px 410px 0 0 rgba(191, 93, 157, 1),
  375px 410px 0 0 rgba(191, 93, 157, 1), 380px 410px 0 0 rgba(191, 93, 157, 1),
  385px 410px 0 0 rgba(191, 93, 157, 1), 390px 410px 0 0 rgba(191, 93, 157, 1),
  395px 410px 0 0 rgba(191, 93, 157, 1), 400px 410px 0 0 rgba(191, 93, 157, 1),
  405px 410px 0 0 rgba(191, 93, 157, 1), 410px 410px 0 0 rgba(191, 93, 157, 1),
  415px 410px 0 0 rgba(191, 93, 157, 1), 420px 410px 0 0 rgba(191, 93, 157, 1),
  425px 410px 0 0 rgba(191, 93, 157, 1), 430px 410px 0 0 rgba(191, 93, 157, 1),
  435px 410px 0 0 rgba(191, 93, 157, 1), 440px 410px 0 0 rgba(191, 93, 157, 1),
  445px 410px 0 0 rgba(191, 93, 157, 1), 450px 410px 0 0 rgba(191, 93, 157, 1),
  455px 410px 0 0 rgba(191, 93, 157, 1), 460px 410px 0 0 rgba(191, 93, 157, 1),
  465px 410px 0 0 rgba(191, 93, 157, 1), 470px 410px 0 0 rgba(191, 93, 157, 1),
  475px 410px 0 0 rgba(191, 93, 157, 1), 480px 410px 0 0 rgba(191, 93, 157, 1),
  485px 410px 0 0 rgba(191, 93, 157, 1), 490px 410px 0 0 rgba(191, 93, 157, 1),
  495px 410px 0 0 rgba(191, 93, 157, 1), 500px 410px 0 0 rgba(191, 93, 157, 1),
  505px 410px 0 0 rgba(191, 93, 157, 1), 510px 410px 0 0 rgba(191, 93, 157, 1),
  515px 410px 0 0 rgba(191, 93, 157, 1), 520px 410px 0 0 rgba(191, 93, 157, 1),
  525px 410px 0 0 rgba(191, 93, 157, 1), 530px 410px 0 0 rgba(191, 93, 157, 1),
  535px 410px 0 0 rgba(191, 93, 157, 1), 540px 410px 0 0 rgba(191, 93, 157, 1),
  545px 410px 0 0 rgba(191, 93, 157, 1), 550px 410px 0 0 rgba(191, 93, 157, 1),
  555px 410px 0 0 rgba(191, 93, 157, 1), 560px 410px 0 0 rgba(191, 93, 157, 1),
  565px 410px 0 0 rgba(191, 93, 157, 1), 570px 410px 0 0 rgba(191, 93, 157, 1),
  575px 410px 0 0 rgba(191, 93, 157, 1), 580px 410px 0 0 rgba(191, 93, 157, 1),
  585px 410px 0 0 rgba(191, 93, 157, 1), 590px 410px 0 0 rgba(191, 93, 157, 1),
  595px 410px 0 0 rgba(191, 93, 157, 1), 600px 410px 0 0 rgba(191, 93, 157, 1),
  605px 410px 0 0 rgba(191, 93, 157, 1), 610px 410px 0 0 rgba(191, 93, 157, 1),
  615px 410px 0 0 rgba(191, 93, 157, 1), 620px 410px 0 0 rgba(191, 93, 157, 1),
  625px 410px 0 0 rgba(191, 93, 157, 1), 630px 410px 0 0 rgba(191, 93, 157, 1),
  635px 410px 0 0 rgba(191, 93, 157, 1), 640px 410px 0 0 rgba(191, 93, 157, 1),
  645px 410px 0 0 rgba(191, 93, 157, 1), 650px 410px 0 0 rgba(191, 93, 157, 1),
  655px 410px 0 0 rgba(191, 93, 157, 1), 660px 410px 0 0 rgba(191, 93, 157, 1),
  665px 410px 0 0 rgba(191, 93, 157, 1), 670px 410px 0 0 rgba(191, 93, 157, 1),
  675px 410px 0 0 rgba(191, 93, 157, 1), 680px 410px 0 0 rgba(191, 93, 157, 1),
  685px 410px 0 0 rgba(203, 109, 181, 1), 690px 410px 0 0 rgba(255, 205, 234, 1),
  695px 410px 0 0 rgba(255, 205, 234, 1), 700px 410px 0 0 rgba(168, 90, 150, 1),
  705px 410px 0 0 rgba(203, 109, 181, 1), 5px 415px 0 0 rgba(203, 109, 181, 1),
  10px 415px 0 0 rgba(252, 231, 243, 1), 15px 415px 0 0 rgba(255, 205, 234, 1),
  20px 415px 0 0 rgba(255, 205, 234, 1), 25px 415px 0 0 rgba(203, 109, 181, 1),
  105px 415px 0 0 rgba(191, 93, 157, 1), 110px 415px 0 0 rgba(191, 93, 157, 1),
  330px 415px 0 0 rgba(191, 93, 157, 1), 530px 415px 0 0 rgba(191, 93, 157, 1),
  535px 415px 0 0 rgba(191, 93, 157, 1), 685px 415px 0 0 rgba(203, 109, 181, 1),
  690px 415px 0 0 rgba(255, 205, 234, 1), 695px 415px 0 0 rgba(255, 205, 234, 1),
  700px 415px 0 0 rgba(168, 90, 150, 1), 705px 415px 0 0 rgba(203, 109, 181, 1),
  5px 420px 0 0 rgba(203, 109, 181, 1), 10px 420px 0 0 rgba(252, 231, 243, 1),
  15px 420px 0 0 rgba(255, 205, 234, 1), 20px 420px 0 0 rgba(255, 205, 234, 1),
  25px 420px 0 0 rgba(203, 109, 181, 1), 100px 420px 0 0 rgba(191, 93, 157, 1),
  105px 420px 0 0 rgba(191, 93, 157, 1), 330px 420px 0 0 rgba(191, 93, 157, 1),
  535px 420px 0 0 rgba(191, 93, 157, 1), 540px 420px 0 0 rgba(191, 93, 157, 1),
  685px 420px 0 0 rgba(203, 109, 181, 1), 690px 420px 0 0 rgba(255, 205, 234, 1),
  695px 420px 0 0 rgba(255, 205, 234, 1), 700px 420px 0 0 rgba(168, 90, 150, 1),
  705px 420px 0 0 rgba(203, 109, 181, 1), 5px 425px 0 0 rgba(203, 109, 181, 1),
  10px 425px 0 0 rgba(252, 231, 243, 1), 15px 425px 0 0 rgba(255, 205, 234, 1),
  20px 425px 0 0 rgba(255, 205, 234, 1), 25px 425px 0 0 rgba(203, 109, 181, 1),
  95px 425px 0 0 rgba(191, 93, 157, 1), 100px 425px 0 0 rgba(191, 93, 157, 1),
  330px 425px 0 0 rgba(191, 93, 157, 1), 540px 425px 0 0 rgba(191, 93, 157, 1),
  545px 425px 0 0 rgba(191, 93, 157, 1), 685px 425px 0 0 rgba(203, 109, 181, 1),
  690px 425px 0 0 rgba(255, 205, 234, 1), 695px 425px 0 0 rgba(255, 205, 234, 1),
  700px 425px 0 0 rgba(168, 90, 150, 1), 705px 425px 0 0 rgba(203, 109, 181, 1),
  5px 430px 0 0 rgba(203, 109, 181, 1), 10px 430px 0 0 rgba(252, 231, 243, 1),
  15px 430px 0 0 rgba(255, 205, 234, 1), 20px 430px 0 0 rgba(255, 205, 234, 1),
  25px 430px 0 0 rgba(203, 109, 181, 1), 90px 430px 0 0 rgba(191, 93, 157, 1),
  95px 430px 0 0 rgba(191, 93, 157, 1), 330px 430px 0 0 rgba(146, 99, 176, 1),
  545px 430px 0 0 rgba(191, 93, 157, 1), 550px 430px 0 0 rgba(191, 93, 157, 1),
  685px 430px 0 0 rgba(203, 109, 181, 1), 690px 430px 0 0 rgba(255, 205, 234, 1),
  695px 430px 0 0 rgba(255, 205, 234, 1), 700px 430px 0 0 rgba(168, 90, 150, 1),
  705px 430px 0 0 rgba(203, 109, 181, 1), 5px 435px 0 0 rgba(203, 109, 181, 1),
  10px 435px 0 0 rgba(252, 231, 243, 1), 15px 435px 0 0 rgba(255, 205, 234, 1),
  20px 435px 0 0 rgba(255, 205, 234, 1), 25px 435px 0 0 rgba(203, 109, 181, 1),
  85px 435px 0 0 rgba(191, 93, 157, 1), 90px 435px 0 0 rgba(191, 93, 157, 1),
  330px 435px 0 0 rgba(191, 93, 157, 1), 550px 435px 0 0 rgba(191, 93, 157, 1),
  555px 435px 0 0 rgba(191, 93, 157, 1), 685px 435px 0 0 rgba(203, 109, 181, 1),
  690px 435px 0 0 rgba(255, 205, 234, 1), 695px 435px 0 0 rgba(255, 205, 234, 1),
  700px 435px 0 0 rgba(168, 90, 150, 1), 705px 435px 0 0 rgba(203, 109, 181, 1),
  5px 440px 0 0 rgba(203, 109, 181, 1), 10px 440px 0 0 rgba(252, 231, 243, 1),
  15px 440px 0 0 rgba(255, 205, 234, 1), 20px 440px 0 0 rgba(255, 205, 234, 1),
  25px 440px 0 0 rgba(203, 109, 181, 1), 80px 440px 0 0 rgba(191, 93, 157, 1),
  85px 440px 0 0 rgba(191, 93, 157, 1), 330px 440px 0 0 rgba(146, 99, 176, 1),
  555px 440px 0 0 rgba(191, 93, 157, 1), 560px 440px 0 0 rgba(191, 93, 157, 1),
  685px 440px 0 0 rgba(203, 109, 181, 1), 690px 440px 0 0 rgba(255, 205, 234, 1),
  695px 440px 0 0 rgba(255, 205, 234, 1), 700px 440px 0 0 rgba(168, 90, 150, 1),
  705px 440px 0 0 rgba(203, 109, 181, 1), 5px 445px 0 0 rgba(203, 109, 181, 1),
  10px 445px 0 0 rgba(252, 231, 243, 1), 15px 445px 0 0 rgba(255, 205, 234, 1),
  20px 445px 0 0 rgba(255, 205, 234, 1), 25px 445px 0 0 rgba(203, 109, 181, 1),
  75px 445px 0 0 rgba(146, 99, 176, 1), 80px 445px 0 0 rgba(146, 99, 176, 1),
  330px 445px 0 0 rgba(146, 99, 176, 1), 560px 445px 0 0 rgba(191, 93, 157, 1),
  565px 445px 0 0 rgba(191, 93, 157, 1), 685px 445px 0 0 rgba(203, 109, 181, 1),
  690px 445px 0 0 rgba(255, 205, 234, 1), 695px 445px 0 0 rgba(255, 205, 234, 1),
  700px 445px 0 0 rgba(168, 90, 150, 1), 705px 445px 0 0 rgba(203, 109, 181, 1),
  5px 450px 0 0 rgba(203, 109, 181, 1), 10px 450px 0 0 rgba(252, 231, 243, 1),
  15px 450px 0 0 rgba(255, 205, 234, 1), 20px 450px 0 0 rgba(255, 205, 234, 1),
  25px 450px 0 0 rgba(203, 109, 181, 1), 70px 450px 0 0 rgba(146, 99, 176, 1),
  75px 450px 0 0 rgba(146, 99, 176, 1), 330px 450px 0 0 rgba(146, 99, 176, 1),
  565px 450px 0 0 rgba(146, 99, 176, 1), 570px 450px 0 0 rgba(146, 99, 176, 1),
  685px 450px 0 0 rgba(203, 109, 181, 1), 690px 450px 0 0 rgba(255, 205, 234, 1),
  695px 450px 0 0 rgba(255, 205, 234, 1), 700px 450px 0 0 rgba(168, 90, 150, 1),
  705px 450px 0 0 rgba(203, 109, 181, 1), 5px 455px 0 0 rgba(203, 109, 181, 1),
  10px 455px 0 0 rgba(254, 221, 240, 1), 15px 455px 0 0 rgba(255, 205, 234, 1),
  20px 455px 0 0 rgba(255, 205, 234, 1), 25px 455px 0 0 rgba(203, 109, 181, 1),
  65px 455px 0 0 rgba(146, 99, 176, 1), 70px 455px 0 0 rgba(146, 99, 176, 1),
  330px 455px 0 0 rgba(146, 99, 176, 1), 570px 455px 0 0 rgba(146, 99, 176, 1),
  575px 455px 0 0 rgba(146, 99, 176, 1), 685px 455px 0 0 rgba(203, 109, 181, 1),
  690px 455px 0 0 rgba(255, 205, 234, 1), 695px 455px 0 0 rgba(255, 205, 234, 1),
  700px 455px 0 0 rgba(168, 90, 150, 1), 705px 455px 0 0 rgba(203, 109, 181, 1),
  5px 460px 0 0 rgba(203, 109, 181, 1), 10px 460px 0 0 rgba(252, 231, 243, 1),
  15px 460px 0 0 rgba(255, 205, 234, 1), 20px 460px 0 0 rgba(255, 205, 234, 1),
  25px 460px 0 0 rgba(203, 109, 181, 1), 60px 460px 0 0 rgba(146, 99, 176, 1),
  65px 460px 0 0 rgba(146, 99, 176, 1), 330px 460px 0 0 rgba(146, 99, 176, 1),
  575px 460px 0 0 rgba(146, 99, 176, 1), 580px 460px 0 0 rgba(146, 99, 176, 1),
  685px 460px 0 0 rgba(203, 109, 181, 1), 690px 460px 0 0 rgba(255, 205, 234, 1),
  695px 460px 0 0 rgba(255, 205, 234, 1), 700px 460px 0 0 rgba(168, 90, 150, 1),
  705px 460px 0 0 rgba(203, 109, 181, 1), 5px 465px 0 0 rgba(203, 109, 181, 1),
  10px 465px 0 0 rgba(252, 231, 243, 1), 15px 465px 0 0 rgba(255, 205, 234, 1),
  20px 465px 0 0 rgba(255, 205, 234, 1), 25px 465px 0 0 rgba(203, 109, 181, 1),
  55px 465px 0 0 rgba(146, 99, 176, 1), 60px 465px 0 0 rgba(146, 99, 176, 1),
  330px 465px 0 0 rgba(146, 99, 176, 1), 580px 465px 0 0 rgba(146, 99, 176, 1),
  585px 465px 0 0 rgba(146, 99, 176, 1), 685px 465px 0 0 rgba(203, 109, 181, 1),
  690px 465px 0 0 rgba(255, 205, 234, 1), 695px 465px 0 0 rgba(255, 205, 234, 1),
  700px 465px 0 0 rgba(168, 90, 150, 1), 705px 465px 0 0 rgba(203, 109, 181, 1),
  5px 470px 0 0 rgba(203, 109, 181, 1), 10px 470px 0 0 rgba(252, 231, 243, 1),
  15px 470px 0 0 rgba(255, 205, 234, 1), 20px 470px 0 0 rgba(255, 205, 234, 1),
  25px 470px 0 0 rgba(203, 109, 181, 1), 50px 470px 0 0 rgba(146, 99, 176, 1),
  55px 470px 0 0 rgba(146, 99, 176, 1), 330px 470px 0 0 rgba(146, 99, 176, 1),
  585px 470px 0 0 rgba(146, 99, 176, 1), 590px 470px 0 0 rgba(146, 99, 176, 1),
  685px 470px 0 0 rgba(203, 109, 181, 1), 690px 470px 0 0 rgba(255, 205, 234, 1),
  695px 470px 0 0 rgba(255, 205, 234, 1), 700px 470px 0 0 rgba(168, 90, 150, 1),
  705px 470px 0 0 rgba(203, 109, 181, 1), 5px 475px 0 0 rgba(203, 109, 181, 1),
  10px 475px 0 0 rgba(252, 231, 243, 1), 15px 475px 0 0 rgba(255, 205, 234, 1),
  20px 475px 0 0 rgba(255, 205, 234, 1), 25px 475px 0 0 rgba(203, 109, 181, 1),
  45px 475px 0 0 rgba(146, 99, 176, 1), 50px 475px 0 0 rgba(146, 99, 176, 1),
  330px 475px 0 0 rgba(146, 99, 176, 1), 590px 475px 0 0 rgba(146, 99, 176, 1),
  595px 475px 0 0 rgba(146, 99, 176, 1), 685px 475px 0 0 rgba(203, 109, 181, 1),
  690px 475px 0 0 rgba(255, 205, 234, 1), 695px 475px 0 0 rgba(255, 205, 234, 1),
  700px 475px 0 0 rgba(168, 90, 150, 1), 705px 475px 0 0 rgba(203, 109, 181, 1),
  5px 480px 0 0 rgba(203, 109, 181, 1), 10px 480px 0 0 rgba(252, 231, 243, 1),
  15px 480px 0 0 rgba(255, 205, 234, 1), 20px 480px 0 0 rgba(255, 205, 234, 1),
  25px 480px 0 0 rgba(203, 109, 181, 1), 40px 480px 0 0 rgba(146, 99, 176, 1),
  45px 480px 0 0 rgba(146, 99, 176, 1), 330px 480px 0 0 rgba(146, 99, 176, 1),
  595px 480px 0 0 rgba(146, 99, 176, 1), 600px 480px 0 0 rgba(146, 99, 176, 1),
  685px 480px 0 0 rgba(203, 109, 181, 1), 690px 480px 0 0 rgba(255, 205, 234, 1),
  695px 480px 0 0 rgba(255, 205, 234, 1), 700px 480px 0 0 rgba(168, 90, 150, 1),
  705px 480px 0 0 rgba(203, 109, 181, 1), 5px 485px 0 0 rgba(203, 109, 181, 1),
  10px 485px 0 0 rgba(252, 231, 243, 1), 15px 485px 0 0 rgba(255, 205, 234, 1),
  20px 485px 0 0 rgba(255, 205, 234, 1), 25px 485px 0 0 rgba(203, 109, 181, 1),
  35px 485px 0 0 rgba(146, 99, 176, 1), 40px 485px 0 0 rgba(146, 99, 176, 1),
  330px 485px 0 0 rgba(146, 99, 176, 1), 600px 485px 0 0 rgba(146, 99, 176, 1),
  605px 485px 0 0 rgba(146, 99, 176, 1), 685px 485px 0 0 rgba(203, 109, 181, 1),
  690px 485px 0 0 rgba(255, 205, 234, 1), 695px 485px 0 0 rgba(255, 205, 234, 1),
  700px 485px 0 0 rgba(168, 90, 150, 1), 705px 485px 0 0 rgba(203, 109, 181, 1),
  5px 490px 0 0 rgba(203, 109, 181, 1), 10px 490px 0 0 rgba(252, 231, 243, 1),
  15px 490px 0 0 rgba(255, 205, 234, 1), 20px 490px 0 0 rgba(255, 205, 234, 1),
  25px 490px 0 0 rgba(203, 109, 181, 1), 30px 490px 0 0 rgba(146, 99, 176, 1),
  35px 490px 0 0 rgba(146, 99, 176, 1), 330px 490px 0 0 rgba(146, 99, 176, 1),
  605px 490px 0 0 rgba(146, 99, 176, 1), 610px 490px 0 0 rgba(146, 99, 176, 1),
  685px 490px 0 0 rgba(203, 109, 181, 1), 690px 490px 0 0 rgba(255, 205, 234, 1),
  695px 490px 0 0 rgba(255, 205, 234, 1), 700px 490px 0 0 rgba(168, 90, 150, 1),
  705px 490px 0 0 rgba(203, 109, 181, 1), 5px 495px 0 0 rgba(203, 109, 181, 1),
  10px 495px 0 0 rgba(252, 231, 243, 1), 15px 495px 0 0 rgba(255, 205, 234, 1),
  20px 495px 0 0 rgba(255, 205, 234, 1), 25px 495px 0 0 rgba(203, 109, 181, 1),
  30px 495px 0 0 rgba(146, 99, 176, 1), 35px 495px 0 0 rgba(146, 99, 176, 1),
  40px 495px 0 0 rgba(146, 99, 176, 1), 45px 495px 0 0 rgba(146, 99, 176, 1),
  50px 495px 0 0 rgba(146, 99, 176, 1), 55px 495px 0 0 rgba(146, 99, 176, 1),
  60px 495px 0 0 rgba(146, 99, 176, 1), 65px 495px 0 0 rgba(146, 99, 176, 1),
  70px 495px 0 0 rgba(146, 99, 176, 1), 75px 495px 0 0 rgba(146, 99, 176, 1),
  80px 495px 0 0 rgba(146, 99, 176, 1), 85px 495px 0 0 rgba(146, 99, 176, 1),
  90px 495px 0 0 rgba(146, 99, 176, 1), 95px 495px 0 0 rgba(146, 99, 176, 1),
  100px 495px 0 0 rgba(146, 99, 176, 1), 105px 495px 0 0 rgba(146, 99, 176, 1),
  110px 495px 0 0 rgba(146, 99, 176, 1), 115px 495px 0 0 rgba(146, 99, 176, 1),
  120px 495px 0 0 rgba(146, 99, 176, 1), 125px 495px 0 0 rgba(146, 99, 176, 1),
  130px 495px 0 0 rgba(146, 99, 176, 1), 135px 495px 0 0 rgba(146, 99, 176, 1),
  140px 495px 0 0 rgba(146, 99, 176, 1), 145px 495px 0 0 rgba(146, 99, 176, 1),
  150px 495px 0 0 rgba(146, 99, 176, 1), 155px 495px 0 0 rgba(146, 99, 176, 1),
  160px 495px 0 0 rgba(146, 99, 176, 1), 165px 495px 0 0 rgba(146, 99, 176, 1),
  170px 495px 0 0 rgba(146, 99, 176, 1), 175px 495px 0 0 rgba(146, 99, 176, 1),
  180px 495px 0 0 rgba(146, 99, 176, 1), 185px 495px 0 0 rgba(146, 99, 176, 1),
  190px 495px 0 0 rgba(146, 99, 176, 1), 195px 495px 0 0 rgba(146, 99, 176, 1),
  200px 495px 0 0 rgba(146, 99, 176, 1), 205px 495px 0 0 rgba(146, 99, 176, 1),
  210px 495px 0 0 rgba(146, 99, 176, 1), 215px 495px 0 0 rgba(146, 99, 176, 1),
  220px 495px 0 0 rgba(146, 99, 176, 1), 225px 495px 0 0 rgba(146, 99, 176, 1),
  230px 495px 0 0 rgba(146, 99, 176, 1), 235px 495px 0 0 rgba(146, 99, 176, 1),
  240px 495px 0 0 rgba(146, 99, 176, 1), 245px 495px 0 0 rgba(146, 99, 176, 1),
  250px 495px 0 0 rgba(146, 99, 176, 1), 255px 495px 0 0 rgba(146, 99, 176, 1),
  260px 495px 0 0 rgba(146, 99, 176, 1), 265px 495px 0 0 rgba(146, 99, 176, 1),
  270px 495px 0 0 rgba(146, 99, 176, 1), 275px 495px 0 0 rgba(146, 99, 176, 1),
  280px 495px 0 0 rgba(146, 99, 176, 1), 285px 495px 0 0 rgba(146, 99, 176, 1),
  290px 495px 0 0 rgba(146, 99, 176, 1), 295px 495px 0 0 rgba(146, 99, 176, 1),
  300px 495px 0 0 rgba(146, 99, 176, 1), 305px 495px 0 0 rgba(146, 99, 176, 1),
  310px 495px 0 0 rgba(146, 99, 176, 1), 315px 495px 0 0 rgba(146, 99, 176, 1),
  320px 495px 0 0 rgba(146, 99, 176, 1), 325px 495px 0 0 rgba(146, 99, 176, 1),
  330px 495px 0 0 rgba(146, 99, 176, 1), 335px 495px 0 0 rgba(146, 99, 176, 1),
  340px 495px 0 0 rgba(146, 99, 176, 1), 345px 495px 0 0 rgba(146, 99, 176, 1),
  350px 495px 0 0 rgba(146, 99, 176, 1), 355px 495px 0 0 rgba(146, 99, 176, 1),
  360px 495px 0 0 rgba(146, 99, 176, 1), 365px 495px 0 0 rgba(146, 99, 176, 1),
  370px 495px 0 0 rgba(146, 99, 176, 1), 375px 495px 0 0 rgba(146, 99, 176, 1),
  380px 495px 0 0 rgba(146, 99, 176, 1), 385px 495px 0 0 rgba(146, 99, 176, 1),
  390px 495px 0 0 rgba(146, 99, 176, 1), 395px 495px 0 0 rgba(146, 99, 176, 1),
  400px 495px 0 0 rgba(146, 99, 176, 1), 405px 495px 0 0 rgba(146, 99, 176, 1),
  410px 495px 0 0 rgba(146, 99, 176, 1), 415px 495px 0 0 rgba(146, 99, 176, 1),
  420px 495px 0 0 rgba(146, 99, 176, 1), 425px 495px 0 0 rgba(146, 99, 176, 1),
  430px 495px 0 0 rgba(146, 99, 176, 1), 435px 495px 0 0 rgba(146, 99, 176, 1),
  440px 495px 0 0 rgba(146, 99, 176, 1), 445px 495px 0 0 rgba(146, 99, 176, 1),
  450px 495px 0 0 rgba(146, 99, 176, 1), 455px 495px 0 0 rgba(146, 99, 176, 1),
  460px 495px 0 0 rgba(146, 99, 176, 1), 465px 495px 0 0 rgba(146, 99, 176, 1),
  470px 495px 0 0 rgba(146, 99, 176, 1), 475px 495px 0 0 rgba(146, 99, 176, 1),
  480px 495px 0 0 rgba(146, 99, 176, 1), 485px 495px 0 0 rgba(146, 99, 176, 1),
  490px 495px 0 0 rgba(146, 99, 176, 1), 495px 495px 0 0 rgba(146, 99, 176, 1),
  500px 495px 0 0 rgba(146, 99, 176, 1), 505px 495px 0 0 rgba(146, 99, 176, 1),
  510px 495px 0 0 rgba(146, 99, 176, 1), 515px 495px 0 0 rgba(146, 99, 176, 1),
  520px 495px 0 0 rgba(146, 99, 176, 1), 525px 495px 0 0 rgba(146, 99, 176, 1),
  530px 495px 0 0 rgba(146, 99, 176, 1), 535px 495px 0 0 rgba(146, 99, 176, 1),
  540px 495px 0 0 rgba(146, 99, 176, 1), 545px 495px 0 0 rgba(146, 99, 176, 1),
  550px 495px 0 0 rgba(146, 99, 176, 1), 555px 495px 0 0 rgba(146, 99, 176, 1),
  560px 495px 0 0 rgba(146, 99, 176, 1), 565px 495px 0 0 rgba(146, 99, 176, 1),
  570px 495px 0 0 rgba(146, 99, 176, 1), 575px 495px 0 0 rgba(146, 99, 176, 1),
  580px 495px 0 0 rgba(146, 99, 176, 1), 585px 495px 0 0 rgba(146, 99, 176, 1),
  590px 495px 0 0 rgba(146, 99, 176, 1), 595px 495px 0 0 rgba(146, 99, 176, 1),
  600px 495px 0 0 rgba(146, 99, 176, 1), 605px 495px 0 0 rgba(146, 99, 176, 1),
  610px 495px 0 0 rgba(146, 99, 176, 1), 615px 495px 0 0 rgba(146, 99, 176, 1),
  620px 495px 0 0 rgba(146, 99, 176, 1), 625px 495px 0 0 rgba(146, 99, 176, 1),
  630px 495px 0 0 rgba(146, 99, 176, 1), 635px 495px 0 0 rgba(146, 99, 176, 1),
  640px 495px 0 0 rgba(146, 99, 176, 1), 645px 495px 0 0 rgba(146, 99, 176, 1),
  650px 495px 0 0 rgba(146, 99, 176, 1), 655px 495px 0 0 rgba(146, 99, 176, 1),
  660px 495px 0 0 rgba(146, 99, 176, 1), 665px 495px 0 0 rgba(146, 99, 176, 1),
  670px 495px 0 0 rgba(146, 99, 176, 1), 675px 495px 0 0 rgba(146, 99, 176, 1),
  680px 495px 0 0 rgba(146, 99, 176, 1), 685px 495px 0 0 rgba(203, 109, 181, 1),
  690px 495px 0 0 rgba(255, 205, 234, 1), 695px 495px 0 0 rgba(255, 205, 234, 1),
  700px 495px 0 0 rgba(168, 90, 150, 1), 705px 495px 0 0 rgba(203, 109, 181, 1),
  5px 500px 0 0 rgba(203, 109, 181, 1), 10px 500px 0 0 rgba(254, 221, 240, 1),
  15px 500px 0 0 rgba(255, 205, 234, 1), 20px 500px 0 0 rgba(255, 205, 234, 1),
  25px 500px 0 0 rgba(203, 109, 181, 1), 330px 500px 0 0 rgba(146, 99, 176, 1),
  615px 500px 0 0 rgba(146, 99, 176, 1), 620px 500px 0 0 rgba(146, 99, 176, 1),
  685px 500px 0 0 rgba(203, 109, 181, 1), 690px 500px 0 0 rgba(255, 205, 234, 1),
  695px 500px 0 0 rgba(255, 205, 234, 1), 700px 500px 0 0 rgba(168, 90, 150, 1),
  705px 500px 0 0 rgba(203, 109, 181, 1), 5px 505px 0 0 rgba(203, 109, 181, 1),
  10px 505px 0 0 rgba(252, 231, 243, 1), 15px 505px 0 0 rgba(255, 205, 234, 1),
  20px 505px 0 0 rgba(255, 205, 234, 1), 25px 505px 0 0 rgba(203, 109, 181, 1),
  330px 505px 0 0 rgba(146, 99, 176, 1), 620px 505px 0 0 rgba(146, 99, 176, 1),
  685px 505px 0 0 rgba(203, 109, 181, 1), 690px 505px 0 0 rgba(255, 205, 234, 1),
  695px 505px 0 0 rgba(255, 205, 234, 1), 700px 505px 0 0 rgba(168, 90, 150, 1),
  705px 505px 0 0 rgba(203, 109, 181, 1), 5px 510px 0 0 rgba(203, 109, 181, 1),
  10px 510px 0 0 rgba(252, 231, 243, 1), 15px 510px 0 0 rgba(255, 205, 234, 1),
  20px 510px 0 0 rgba(255, 205, 234, 1), 25px 510px 0 0 rgba(203, 109, 181, 1),
  30px 510px 0 0 rgba(203, 109, 181, 1), 35px 510px 0 0 rgba(203, 109, 181, 1),
  40px 510px 0 0 rgba(203, 109, 181, 1), 45px 510px 0 0 rgba(203, 109, 181, 1),
  50px 510px 0 0 rgba(203, 109, 181, 1), 55px 510px 0 0 rgba(203, 109, 181, 1),
  60px 510px 0 0 rgba(203, 109, 181, 1), 65px 510px 0 0 rgba(203, 109, 181, 1),
  70px 510px 0 0 rgba(203, 109, 181, 1), 75px 510px 0 0 rgba(203, 109, 181, 1),
  80px 510px 0 0 rgba(203, 109, 181, 1), 85px 510px 0 0 rgba(203, 109, 181, 1),
  90px 510px 0 0 rgba(203, 109, 181, 1), 95px 510px 0 0 rgba(203, 109, 181, 1),
  100px 510px 0 0 rgba(203, 109, 181, 1), 105px 510px 0 0 rgba(203, 109, 181, 1),
  110px 510px 0 0 rgba(203, 109, 181, 1), 115px 510px 0 0 rgba(203, 109, 181, 1),
  120px 510px 0 0 rgba(203, 109, 181, 1), 125px 510px 0 0 rgba(203, 109, 181, 1),
  130px 510px 0 0 rgba(203, 109, 181, 1), 135px 510px 0 0 rgba(203, 109, 181, 1),
  140px 510px 0 0 rgba(203, 109, 181, 1), 145px 510px 0 0 rgba(203, 109, 181, 1),
  150px 510px 0 0 rgba(203, 109, 181, 1), 155px 510px 0 0 rgba(203, 109, 181, 1),
  160px 510px 0 0 rgba(203, 109, 181, 1), 165px 510px 0 0 rgba(203, 109, 181, 1),
  170px 510px 0 0 rgba(203, 109, 181, 1), 175px 510px 0 0 rgba(203, 109, 181, 1),
  180px 510px 0 0 rgba(203, 109, 181, 1), 185px 510px 0 0 rgba(203, 109, 181, 1),
  190px 510px 0 0 rgba(203, 109, 181, 1), 195px 510px 0 0 rgba(203, 109, 181, 1),
  200px 510px 0 0 rgba(203, 109, 181, 1), 205px 510px 0 0 rgba(203, 109, 181, 1),
  210px 510px 0 0 rgba(203, 109, 181, 1), 215px 510px 0 0 rgba(203, 109, 181, 1),
  220px 510px 0 0 rgba(203, 109, 181, 1), 225px 510px 0 0 rgba(203, 109, 181, 1),
  230px 510px 0 0 rgba(203, 109, 181, 1), 235px 510px 0 0 rgba(203, 109, 181, 1),
  240px 510px 0 0 rgba(203, 109, 181, 1), 245px 510px 0 0 rgba(203, 109, 181, 1),
  250px 510px 0 0 rgba(203, 109, 181, 1), 255px 510px 0 0 rgba(203, 109, 181, 1),
  260px 510px 0 0 rgba(203, 109, 181, 1), 265px 510px 0 0 rgba(203, 109, 181, 1),
  270px 510px 0 0 rgba(203, 109, 181, 1), 275px 510px 0 0 rgba(203, 109, 181, 1),
  280px 510px 0 0 rgba(203, 109, 181, 1), 285px 510px 0 0 rgba(203, 109, 181, 1),
  290px 510px 0 0 rgba(203, 109, 181, 1), 295px 510px 0 0 rgba(203, 109, 181, 1),
  300px 510px 0 0 rgba(203, 109, 181, 1), 305px 510px 0 0 rgba(203, 109, 181, 1),
  310px 510px 0 0 rgba(203, 109, 181, 1), 315px 510px 0 0 rgba(203, 109, 181, 1),
  320px 510px 0 0 rgba(203, 109, 181, 1), 325px 510px 0 0 rgba(203, 109, 181, 1),
  330px 510px 0 0 rgba(203, 109, 181, 1), 335px 510px 0 0 rgba(203, 109, 181, 1),
  340px 510px 0 0 rgba(203, 109, 181, 1), 345px 510px 0 0 rgba(203, 109, 181, 1),
  350px 510px 0 0 rgba(203, 109, 181, 1), 355px 510px 0 0 rgba(203, 109, 181, 1),
  360px 510px 0 0 rgba(203, 109, 181, 1), 365px 510px 0 0 rgba(203, 109, 181, 1),
  370px 510px 0 0 rgba(203, 109, 181, 1), 375px 510px 0 0 rgba(203, 109, 181, 1),
  380px 510px 0 0 rgba(203, 109, 181, 1), 385px 510px 0 0 rgba(203, 109, 181, 1),
  390px 510px 0 0 rgba(203, 109, 181, 1), 395px 510px 0 0 rgba(203, 109, 181, 1),
  400px 510px 0 0 rgba(203, 109, 181, 1), 405px 510px 0 0 rgba(203, 109, 181, 1),
  410px 510px 0 0 rgba(203, 109, 181, 1), 415px 510px 0 0 rgba(203, 109, 181, 1),
  420px 510px 0 0 rgba(203, 109, 181, 1), 425px 510px 0 0 rgba(203, 109, 181, 1),
  430px 510px 0 0 rgba(203, 109, 181, 1), 435px 510px 0 0 rgba(203, 109, 181, 1),
  440px 510px 0 0 rgba(203, 109, 181, 1), 445px 510px 0 0 rgba(203, 109, 181, 1),
  450px 510px 0 0 rgba(203, 109, 181, 1), 455px 510px 0 0 rgba(203, 109, 181, 1),
  460px 510px 0 0 rgba(203, 109, 181, 1), 465px 510px 0 0 rgba(203, 109, 181, 1),
  470px 510px 0 0 rgba(203, 109, 181, 1), 475px 510px 0 0 rgba(203, 109, 181, 1),
  480px 510px 0 0 rgba(203, 109, 181, 1), 485px 510px 0 0 rgba(203, 109, 181, 1),
  490px 510px 0 0 rgba(203, 109, 181, 1), 495px 510px 0 0 rgba(203, 109, 181, 1),
  500px 510px 0 0 rgba(203, 109, 181, 1), 505px 510px 0 0 rgba(203, 109, 181, 1),
  510px 510px 0 0 rgba(203, 109, 181, 1), 515px 510px 0 0 rgba(203, 109, 181, 1),
  520px 510px 0 0 rgba(203, 109, 181, 1), 525px 510px 0 0 rgba(203, 109, 181, 1),
  530px 510px 0 0 rgba(203, 109, 181, 1), 535px 510px 0 0 rgba(203, 109, 181, 1),
  540px 510px 0 0 rgba(203, 109, 181, 1), 545px 510px 0 0 rgba(203, 109, 181, 1),
  550px 510px 0 0 rgba(203, 109, 181, 1), 555px 510px 0 0 rgba(203, 109, 181, 1),
  560px 510px 0 0 rgba(203, 109, 181, 1), 565px 510px 0 0 rgba(203, 109, 181, 1),
  570px 510px 0 0 rgba(203, 109, 181, 1), 575px 510px 0 0 rgba(203, 109, 181, 1),
  580px 510px 0 0 rgba(203, 109, 181, 1), 585px 510px 0 0 rgba(203, 109, 181, 1),
  590px 510px 0 0 rgba(203, 109, 181, 1), 595px 510px 0 0 rgba(203, 109, 181, 1),
  600px 510px 0 0 rgba(203, 109, 181, 1), 605px 510px 0 0 rgba(203, 109, 181, 1),
  610px 510px 0 0 rgba(203, 109, 181, 1), 615px 510px 0 0 rgba(203, 109, 181, 1),
  620px 510px 0 0 rgba(203, 109, 181, 1), 625px 510px 0 0 rgba(203, 109, 181, 1),
  630px 510px 0 0 rgba(203, 109, 181, 1), 635px 510px 0 0 rgba(203, 109, 181, 1),
  640px 510px 0 0 rgba(203, 109, 181, 1), 645px 510px 0 0 rgba(203, 109, 181, 1),
  650px 510px 0 0 rgba(203, 109, 181, 1), 655px 510px 0 0 rgba(203, 109, 181, 1),
  660px 510px 0 0 rgba(203, 109, 181, 1), 665px 510px 0 0 rgba(203, 109, 181, 1),
  670px 510px 0 0 rgba(203, 109, 181, 1), 675px 510px 0 0 rgba(203, 109, 181, 1),
  680px 510px 0 0 rgba(203, 109, 181, 1), 685px 510px 0 0 rgba(203, 109, 181, 1),
  690px 510px 0 0 rgba(255, 205, 234, 1), 695px 510px 0 0 rgba(255, 205, 234, 1),
  700px 510px 0 0 rgba(168, 90, 150, 1), 705px 510px 0 0 rgba(203, 109, 181, 1),
  5px 515px 0 0 rgba(203, 109, 181, 1), 10px 515px 0 0 rgba(252, 231, 243, 1),
  15px 515px 0 0 rgba(252, 231, 243, 1), 20px 515px 0 0 rgba(255, 205, 234, 1),
  25px 515px 0 0 rgba(255, 205, 234, 1), 30px 515px 0 0 rgba(255, 205, 234, 1),
  35px 515px 0 0 rgba(255, 205, 234, 1), 40px 515px 0 0 rgba(255, 205, 234, 1),
  45px 515px 0 0 rgba(255, 205, 234, 1), 50px 515px 0 0 rgba(255, 205, 234, 1),
  55px 515px 0 0 rgba(255, 205, 234, 1), 60px 515px 0 0 rgba(255, 205, 234, 1),
  65px 515px 0 0 rgba(255, 205, 234, 1), 70px 515px 0 0 rgba(255, 205, 234, 1),
  75px 515px 0 0 rgba(255, 205, 234, 1), 80px 515px 0 0 rgba(255, 205, 234, 1),
  85px 515px 0 0 rgba(255, 205, 234, 1), 90px 515px 0 0 rgba(255, 205, 234, 1),
  95px 515px 0 0 rgba(255, 205, 234, 1), 100px 515px 0 0 rgba(255, 205, 234, 1),
  105px 515px 0 0 rgba(255, 205, 234, 1), 110px 515px 0 0 rgba(255, 205, 234, 1),
  115px 515px 0 0 rgba(255, 205, 234, 1), 120px 515px 0 0 rgba(255, 205, 234, 1),
  125px 515px 0 0 rgba(255, 205, 234, 1), 130px 515px 0 0 rgba(255, 205, 234, 1),
  135px 515px 0 0 rgba(255, 205, 234, 1), 140px 515px 0 0 rgba(255, 205, 234, 1),
  145px 515px 0 0 rgba(255, 205, 234, 1), 150px 515px 0 0 rgba(255, 205, 234, 1),
  155px 515px 0 0 rgba(255, 205, 234, 1), 160px 515px 0 0 rgba(255, 205, 234, 1),
  165px 515px 0 0 rgba(255, 205, 234, 1), 170px 515px 0 0 rgba(255, 205, 234, 1),
  175px 515px 0 0 rgba(255, 205, 234, 1), 180px 515px 0 0 rgba(255, 205, 234, 1),
  185px 515px 0 0 rgba(255, 205, 234, 1), 190px 515px 0 0 rgba(255, 205, 234, 1),
  195px 515px 0 0 rgba(255, 205, 234, 1), 200px 515px 0 0 rgba(255, 205, 234, 1),
  205px 515px 0 0 rgba(255, 205, 234, 1), 210px 515px 0 0 rgba(255, 205, 234, 1),
  215px 515px 0 0 rgba(255, 205, 234, 1), 220px 515px 0 0 rgba(255, 205, 234, 1),
  225px 515px 0 0 rgba(255, 205, 234, 1), 230px 515px 0 0 rgba(255, 205, 234, 1),
  235px 515px 0 0 rgba(255, 205, 234, 1), 240px 515px 0 0 rgba(255, 205, 234, 1),
  245px 515px 0 0 rgba(255, 205, 234, 1), 250px 515px 0 0 rgba(255, 205, 234, 1),
  255px 515px 0 0 rgba(255, 205, 234, 1), 260px 515px 0 0 rgba(255, 205, 234, 1),
  265px 515px 0 0 rgba(255, 205, 234, 1), 270px 515px 0 0 rgba(255, 205, 234, 1),
  275px 515px 0 0 rgba(255, 205, 234, 1), 280px 515px 0 0 rgba(255, 205, 234, 1),
  285px 515px 0 0 rgba(255, 205, 234, 1), 290px 515px 0 0 rgba(255, 205, 234, 1),
  295px 515px 0 0 rgba(255, 205, 234, 1), 300px 515px 0 0 rgba(255, 205, 234, 1),
  305px 515px 0 0 rgba(255, 205, 234, 1), 310px 515px 0 0 rgba(255, 205, 234, 1),
  315px 515px 0 0 rgba(255, 205, 234, 1), 320px 515px 0 0 rgba(255, 205, 234, 1),
  325px 515px 0 0 rgba(255, 205, 234, 1), 330px 515px 0 0 rgba(255, 205, 234, 1),
  335px 515px 0 0 rgba(255, 205, 234, 1), 340px 515px 0 0 rgba(255, 205, 234, 1),
  345px 515px 0 0 rgba(255, 205, 234, 1), 350px 515px 0 0 rgba(172, 73, 149, 1),
  355px 515px 0 0 rgba(252, 231, 243, 1), 360px 515px 0 0 rgba(172, 73, 149, 1),
  365px 515px 0 0 rgba(255, 205, 234, 1), 370px 515px 0 0 rgba(255, 205, 234, 1),
  375px 515px 0 0 rgba(255, 205, 234, 1), 380px 515px 0 0 rgba(255, 205, 234, 1),
  385px 515px 0 0 rgba(255, 205, 234, 1), 390px 515px 0 0 rgba(255, 205, 234, 1),
  395px 515px 0 0 rgba(255, 205, 234, 1), 400px 515px 0 0 rgba(255, 205, 234, 1),
  405px 515px 0 0 rgba(255, 205, 234, 1), 410px 515px 0 0 rgba(255, 205, 234, 1),
  415px 515px 0 0 rgba(255, 205, 234, 1), 420px 515px 0 0 rgba(255, 205, 234, 1),
  425px 515px 0 0 rgba(255, 205, 234, 1), 430px 515px 0 0 rgba(255, 205, 234, 1),
  435px 515px 0 0 rgba(255, 205, 234, 1), 440px 515px 0 0 rgba(255, 205, 234, 1),
  445px 515px 0 0 rgba(255, 205, 234, 1), 450px 515px 0 0 rgba(255, 205, 234, 1),
  455px 515px 0 0 rgba(255, 205, 234, 1), 460px 515px 0 0 rgba(255, 205, 234, 1),
  465px 515px 0 0 rgba(255, 205, 234, 1), 470px 515px 0 0 rgba(255, 205, 234, 1),
  475px 515px 0 0 rgba(255, 205, 234, 1), 480px 515px 0 0 rgba(255, 205, 234, 1),
  485px 515px 0 0 rgba(255, 205, 234, 1), 490px 515px 0 0 rgba(255, 205, 234, 1),
  495px 515px 0 0 rgba(255, 205, 234, 1), 500px 515px 0 0 rgba(255, 205, 234, 1),
  505px 515px 0 0 rgba(255, 205, 234, 1), 510px 515px 0 0 rgba(255, 205, 234, 1),
  515px 515px 0 0 rgba(255, 205, 234, 1), 520px 515px 0 0 rgba(255, 205, 234, 1),
  525px 515px 0 0 rgba(255, 205, 234, 1), 530px 515px 0 0 rgba(255, 205, 234, 1),
  535px 515px 0 0 rgba(255, 205, 234, 1), 540px 515px 0 0 rgba(255, 205, 234, 1),
  545px 515px 0 0 rgba(255, 205, 234, 1), 550px 515px 0 0 rgba(255, 205, 234, 1),
  555px 515px 0 0 rgba(255, 205, 234, 1), 560px 515px 0 0 rgba(255, 205, 234, 1),
  565px 515px 0 0 rgba(255, 205, 234, 1), 570px 515px 0 0 rgba(255, 205, 234, 1),
  575px 515px 0 0 rgba(255, 205, 234, 1), 580px 515px 0 0 rgba(255, 205, 234, 1),
  585px 515px 0 0 rgba(255, 205, 234, 1), 590px 515px 0 0 rgba(255, 205, 234, 1),
  595px 515px 0 0 rgba(255, 205, 234, 1), 600px 515px 0 0 rgba(255, 205, 234, 1),
  605px 515px 0 0 rgba(255, 205, 234, 1), 610px 515px 0 0 rgba(255, 205, 234, 1),
  615px 515px 0 0 rgba(255, 205, 234, 1), 620px 515px 0 0 rgba(255, 205, 234, 1),
  625px 515px 0 0 rgba(255, 205, 234, 1), 630px 515px 0 0 rgba(255, 205, 234, 1),
  635px 515px 0 0 rgba(255, 205, 234, 1), 640px 515px 0 0 rgba(255, 205, 234, 1),
  645px 515px 0 0 rgba(255, 205, 234, 1), 650px 515px 0 0 rgba(255, 205, 234, 1),
  655px 515px 0 0 rgba(255, 205, 234, 1), 660px 515px 0 0 rgba(255, 205, 234, 1),
  665px 515px 0 0 rgba(255, 205, 234, 1), 670px 515px 0 0 rgba(255, 205, 234, 1),
  675px 515px 0 0 rgba(255, 205, 234, 1), 680px 515px 0 0 rgba(255, 205, 234, 1),
  685px 515px 0 0 rgba(255, 205, 234, 1), 690px 515px 0 0 rgba(255, 205, 234, 1),
  695px 515px 0 0 rgba(168, 90, 150, 1), 700px 515px 0 0 rgba(203, 109, 181, 1),
  705px 515px 0 0 rgba(203, 109, 181, 1), 10px 520px 0 0 rgba(203, 109, 181, 1),
  15px 520px 0 0 rgba(252, 231, 243, 1), 20px 520px 0 0 rgba(255, 205, 234, 1),
  25px 520px 0 0 rgba(255, 205, 234, 1), 30px 520px 0 0 rgba(255, 205, 234, 1),
  35px 520px 0 0 rgba(255, 205, 234, 1), 40px 520px 0 0 rgba(255, 205, 234, 1),
  45px 520px 0 0 rgba(255, 205, 234, 1), 50px 520px 0 0 rgba(255, 205, 234, 1),
  55px 520px 0 0 rgba(255, 205, 234, 1), 60px 520px 0 0 rgba(255, 205, 234, 1),
  65px 520px 0 0 rgba(255, 205, 234, 1), 70px 520px 0 0 rgba(255, 205, 234, 1),
  75px 520px 0 0 rgba(255, 205, 234, 1), 80px 520px 0 0 rgba(255, 205, 234, 1),
  85px 520px 0 0 rgba(255, 205, 234, 1), 90px 520px 0 0 rgba(255, 205, 234, 1),
  95px 520px 0 0 rgba(255, 205, 234, 1), 100px 520px 0 0 rgba(255, 205, 234, 1),
  105px 520px 0 0 rgba(255, 205, 234, 1), 110px 520px 0 0 rgba(255, 205, 234, 1),
  115px 520px 0 0 rgba(255, 205, 234, 1), 120px 520px 0 0 rgba(255, 205, 234, 1),
  125px 520px 0 0 rgba(255, 205, 234, 1), 130px 520px 0 0 rgba(255, 205, 234, 1),
  135px 520px 0 0 rgba(255, 205, 234, 1), 140px 520px 0 0 rgba(255, 205, 234, 1),
  145px 520px 0 0 rgba(255, 205, 234, 1), 150px 520px 0 0 rgba(255, 205, 234, 1),
  155px 520px 0 0 rgba(255, 205, 234, 1), 160px 520px 0 0 rgba(255, 205, 234, 1),
  165px 520px 0 0 rgba(255, 205, 234, 1), 170px 520px 0 0 rgba(255, 205, 234, 1),
  175px 520px 0 0 rgba(255, 205, 234, 1), 180px 520px 0 0 rgba(255, 205, 234, 1),
  185px 520px 0 0 rgba(255, 205, 234, 1), 190px 520px 0 0 rgba(255, 205, 234, 1),
  195px 520px 0 0 rgba(255, 205, 234, 1), 200px 520px 0 0 rgba(255, 205, 234, 1),
  205px 520px 0 0 rgba(255, 205, 234, 1), 210px 520px 0 0 rgba(255, 205, 234, 1),
  215px 520px 0 0 rgba(255, 205, 234, 1), 220px 520px 0 0 rgba(255, 205, 234, 1),
  225px 520px 0 0 rgba(255, 205, 234, 1), 230px 520px 0 0 rgba(255, 205, 234, 1),
  235px 520px 0 0 rgba(255, 205, 234, 1), 240px 520px 0 0 rgba(255, 205, 234, 1),
  245px 520px 0 0 rgba(255, 205, 234, 1), 250px 520px 0 0 rgba(255, 205, 234, 1),
  255px 520px 0 0 rgba(255, 205, 234, 1), 260px 520px 0 0 rgba(255, 205, 234, 1),
  265px 520px 0 0 rgba(255, 205, 234, 1), 270px 520px 0 0 rgba(255, 205, 234, 1),
  275px 520px 0 0 rgba(255, 205, 234, 1), 280px 520px 0 0 rgba(255, 205, 234, 1),
  285px 520px 0 0 rgba(255, 205, 234, 1), 290px 520px 0 0 rgba(255, 205, 234, 1),
  295px 520px 0 0 rgba(255, 205, 234, 1), 300px 520px 0 0 rgba(255, 205, 234, 1),
  305px 520px 0 0 rgba(255, 205, 234, 1), 310px 520px 0 0 rgba(255, 205, 234, 1),
  315px 520px 0 0 rgba(255, 205, 234, 1), 320px 520px 0 0 rgba(255, 205, 234, 1),
  325px 520px 0 0 rgba(255, 205, 234, 1), 330px 520px 0 0 rgba(255, 205, 234, 1),
  335px 520px 0 0 rgba(255, 205, 234, 1), 340px 520px 0 0 rgba(255, 205, 234, 1),
  345px 520px 0 0 rgba(172, 73, 149, 1), 350px 520px 0 0 rgba(252, 231, 243, 1),
  355px 520px 0 0 rgba(252, 231, 243, 1), 360px 520px 0 0 rgba(252, 231, 243, 1),
  365px 520px 0 0 rgba(172, 73, 149, 1), 370px 520px 0 0 rgba(255, 205, 234, 1),
  375px 520px 0 0 rgba(255, 205, 234, 1), 380px 520px 0 0 rgba(255, 205, 234, 1),
  385px 520px 0 0 rgba(255, 205, 234, 1), 390px 520px 0 0 rgba(255, 205, 234, 1),
  395px 520px 0 0 rgba(255, 205, 234, 1), 400px 520px 0 0 rgba(255, 205, 234, 1),
  405px 520px 0 0 rgba(255, 205, 234, 1), 410px 520px 0 0 rgba(255, 205, 234, 1),
  415px 520px 0 0 rgba(255, 205, 234, 1), 420px 520px 0 0 rgba(255, 205, 234, 1),
  425px 520px 0 0 rgba(255, 205, 234, 1), 430px 520px 0 0 rgba(255, 205, 234, 1),
  435px 520px 0 0 rgba(255, 205, 234, 1), 440px 520px 0 0 rgba(255, 205, 234, 1),
  445px 520px 0 0 rgba(255, 205, 234, 1), 450px 520px 0 0 rgba(255, 205, 234, 1),
  455px 520px 0 0 rgba(255, 205, 234, 1), 460px 520px 0 0 rgba(255, 205, 234, 1),
  465px 520px 0 0 rgba(255, 205, 234, 1), 470px 520px 0 0 rgba(255, 205, 234, 1),
  475px 520px 0 0 rgba(255, 205, 234, 1), 480px 520px 0 0 rgba(255, 205, 234, 1),
  485px 520px 0 0 rgba(255, 205, 234, 1), 490px 520px 0 0 rgba(255, 205, 234, 1),
  495px 520px 0 0 rgba(255, 205, 234, 1), 500px 520px 0 0 rgba(255, 205, 234, 1),
  505px 520px 0 0 rgba(255, 205, 234, 1), 510px 520px 0 0 rgba(255, 205, 234, 1),
  515px 520px 0 0 rgba(255, 205, 234, 1), 520px 520px 0 0 rgba(255, 205, 234, 1),
  525px 520px 0 0 rgba(255, 205, 234, 1), 530px 520px 0 0 rgba(255, 205, 234, 1),
  535px 520px 0 0 rgba(255, 205, 234, 1), 540px 520px 0 0 rgba(255, 205, 234, 1),
  545px 520px 0 0 rgba(255, 205, 234, 1), 550px 520px 0 0 rgba(255, 205, 234, 1),
  555px 520px 0 0 rgba(255, 205, 234, 1), 560px 520px 0 0 rgba(255, 205, 234, 1),
  565px 520px 0 0 rgba(255, 205, 234, 1), 570px 520px 0 0 rgba(255, 205, 234, 1),
  575px 520px 0 0 rgba(255, 205, 234, 1), 580px 520px 0 0 rgba(255, 205, 234, 1),
  585px 520px 0 0 rgba(255, 205, 234, 1), 590px 520px 0 0 rgba(255, 205, 234, 1),
  595px 520px 0 0 rgba(255, 205, 234, 1), 600px 520px 0 0 rgba(255, 205, 234, 1),
  605px 520px 0 0 rgba(255, 205, 234, 1), 610px 520px 0 0 rgba(255, 205, 234, 1),
  615px 520px 0 0 rgba(255, 205, 234, 1), 620px 520px 0 0 rgba(255, 205, 234, 1),
  625px 520px 0 0 rgba(255, 205, 234, 1), 630px 520px 0 0 rgba(255, 205, 234, 1),
  635px 520px 0 0 rgba(255, 205, 234, 1), 640px 520px 0 0 rgba(255, 205, 234, 1),
  645px 520px 0 0 rgba(255, 205, 234, 1), 650px 520px 0 0 rgba(255, 205, 234, 1),
  655px 520px 0 0 rgba(255, 205, 234, 1), 660px 520px 0 0 rgba(255, 205, 234, 1),
  665px 520px 0 0 rgba(255, 205, 234, 1), 670px 520px 0 0 rgba(255, 205, 234, 1),
  675px 520px 0 0 rgba(255, 205, 234, 1), 680px 520px 0 0 rgba(255, 205, 234, 1),
  685px 520px 0 0 rgba(255, 205, 234, 1), 690px 520px 0 0 rgba(255, 205, 234, 1),
  695px 520px 0 0 rgba(168, 90, 150, 1), 700px 520px 0 0 rgba(203, 109, 181, 1),
  10px 525px 0 0 rgba(203, 109, 181, 1), 15px 525px 0 0 rgba(252, 231, 243, 1),
  20px 525px 0 0 rgba(252, 231, 243, 1), 25px 525px 0 0 rgba(252, 231, 243, 1),
  30px 525px 0 0 rgba(255, 205, 234, 1), 35px 525px 0 0 rgba(255, 205, 234, 1),
  40px 525px 0 0 rgba(255, 205, 234, 1), 45px 525px 0 0 rgba(255, 205, 234, 1),
  50px 525px 0 0 rgba(255, 205, 234, 1), 55px 525px 0 0 rgba(255, 205, 234, 1),
  60px 525px 0 0 rgba(255, 205, 234, 1), 65px 525px 0 0 rgba(255, 205, 234, 1),
  70px 525px 0 0 rgba(255, 205, 234, 1), 75px 525px 0 0 rgba(255, 205, 234, 1),
  80px 525px 0 0 rgba(255, 205, 234, 1), 85px 525px 0 0 rgba(255, 205, 234, 1),
  90px 525px 0 0 rgba(255, 205, 234, 1), 95px 525px 0 0 rgba(255, 205, 234, 1),
  100px 525px 0 0 rgba(255, 205, 234, 1), 105px 525px 0 0 rgba(255, 205, 234, 1),
  110px 525px 0 0 rgba(255, 205, 234, 1), 115px 525px 0 0 rgba(255, 205, 234, 1),
  120px 525px 0 0 rgba(255, 205, 234, 1), 125px 525px 0 0 rgba(255, 205, 234, 1),
  130px 525px 0 0 rgba(255, 205, 234, 1), 135px 525px 0 0 rgba(255, 205, 234, 1),
  140px 525px 0 0 rgba(255, 205, 234, 1), 145px 525px 0 0 rgba(255, 205, 234, 1),
  150px 525px 0 0 rgba(255, 205, 234, 1), 155px 525px 0 0 rgba(255, 205, 234, 1),
  160px 525px 0 0 rgba(255, 205, 234, 1), 165px 525px 0 0 rgba(255, 205, 234, 1),
  170px 525px 0 0 rgba(255, 205, 234, 1), 175px 525px 0 0 rgba(255, 205, 234, 1),
  180px 525px 0 0 rgba(255, 205, 234, 1), 185px 525px 0 0 rgba(255, 205, 234, 1),
  190px 525px 0 0 rgba(255, 205, 234, 1), 195px 525px 0 0 rgba(255, 205, 234, 1),
  200px 525px 0 0 rgba(255, 205, 234, 1), 205px 525px 0 0 rgba(255, 205, 234, 1),
  210px 525px 0 0 rgba(255, 205, 234, 1), 215px 525px 0 0 rgba(255, 205, 234, 1),
  220px 525px 0 0 rgba(255, 205, 234, 1), 225px 525px 0 0 rgba(255, 205, 234, 1),
  230px 525px 0 0 rgba(255, 205, 234, 1), 235px 525px 0 0 rgba(255, 205, 234, 1),
  240px 525px 0 0 rgba(255, 205, 234, 1), 245px 525px 0 0 rgba(255, 205, 234, 1),
  250px 525px 0 0 rgba(255, 205, 234, 1), 255px 525px 0 0 rgba(255, 205, 234, 1),
  260px 525px 0 0 rgba(255, 205, 234, 1), 265px 525px 0 0 rgba(255, 205, 234, 1),
  270px 525px 0 0 rgba(255, 205, 234, 1), 275px 525px 0 0 rgba(255, 205, 234, 1),
  280px 525px 0 0 rgba(255, 205, 234, 1), 285px 525px 0 0 rgba(255, 205, 234, 1),
  290px 525px 0 0 rgba(255, 205, 234, 1), 295px 525px 0 0 rgba(255, 205, 234, 1),
  300px 525px 0 0 rgba(255, 205, 234, 1), 305px 525px 0 0 rgba(255, 205, 234, 1),
  310px 525px 0 0 rgba(255, 205, 234, 1), 315px 525px 0 0 rgba(255, 205, 234, 1),
  320px 525px 0 0 rgba(255, 205, 234, 1), 325px 525px 0 0 rgba(255, 205, 234, 1),
  330px 525px 0 0 rgba(255, 205, 234, 1), 335px 525px 0 0 rgba(255, 205, 234, 1),
  340px 525px 0 0 rgba(255, 205, 234, 1), 345px 525px 0 0 rgba(255, 205, 234, 1),
  350px 525px 0 0 rgba(172, 73, 149, 1), 355px 525px 0 0 rgba(252, 231, 243, 1),
  360px 525px 0 0 rgba(172, 73, 149, 1), 365px 525px 0 0 rgba(255, 205, 234, 1),
  370px 525px 0 0 rgba(255, 205, 234, 1), 375px 525px 0 0 rgba(255, 205, 234, 1),
  380px 525px 0 0 rgba(255, 205, 234, 1), 385px 525px 0 0 rgba(255, 205, 234, 1),
  390px 525px 0 0 rgba(255, 205, 234, 1), 395px 525px 0 0 rgba(255, 205, 234, 1),
  400px 525px 0 0 rgba(255, 205, 234, 1), 405px 525px 0 0 rgba(255, 205, 234, 1),
  410px 525px 0 0 rgba(255, 205, 234, 1), 415px 525px 0 0 rgba(255, 205, 234, 1),
  420px 525px 0 0 rgba(255, 205, 234, 1), 425px 525px 0 0 rgba(255, 205, 234, 1),
  430px 525px 0 0 rgba(255, 205, 234, 1), 435px 525px 0 0 rgba(255, 205, 234, 1),
  440px 525px 0 0 rgba(255, 205, 234, 1), 445px 525px 0 0 rgba(255, 205, 234, 1),
  450px 525px 0 0 rgba(255, 205, 234, 1), 455px 525px 0 0 rgba(255, 205, 234, 1),
  460px 525px 0 0 rgba(255, 205, 234, 1), 465px 525px 0 0 rgba(255, 205, 234, 1),
  470px 525px 0 0 rgba(255, 205, 234, 1), 475px 525px 0 0 rgba(255, 205, 234, 1),
  480px 525px 0 0 rgba(255, 205, 234, 1), 485px 525px 0 0 rgba(255, 205, 234, 1),
  490px 525px 0 0 rgba(255, 205, 234, 1), 495px 525px 0 0 rgba(255, 205, 234, 1),
  500px 525px 0 0 rgba(255, 205, 234, 1), 505px 525px 0 0 rgba(255, 205, 234, 1),
  510px 525px 0 0 rgba(255, 205, 234, 1), 515px 525px 0 0 rgba(255, 205, 234, 1),
  520px 525px 0 0 rgba(255, 205, 234, 1), 525px 525px 0 0 rgba(255, 205, 234, 1),
  530px 525px 0 0 rgba(255, 205, 234, 1), 535px 525px 0 0 rgba(255, 205, 234, 1),
  540px 525px 0 0 rgba(255, 205, 234, 1), 545px 525px 0 0 rgba(255, 205, 234, 1),
  550px 525px 0 0 rgba(255, 205, 234, 1), 555px 525px 0 0 rgba(255, 205, 234, 1),
  560px 525px 0 0 rgba(255, 205, 234, 1), 565px 525px 0 0 rgba(255, 205, 234, 1),
  570px 525px 0 0 rgba(255, 205, 234, 1), 575px 525px 0 0 rgba(255, 205, 234, 1),
  580px 525px 0 0 rgba(255, 205, 234, 1), 585px 525px 0 0 rgba(255, 205, 234, 1),
  590px 525px 0 0 rgba(255, 205, 234, 1), 595px 525px 0 0 rgba(255, 205, 234, 1),
  600px 525px 0 0 rgba(255, 205, 234, 1), 605px 525px 0 0 rgba(255, 205, 234, 1),
  610px 525px 0 0 rgba(255, 205, 234, 1), 615px 525px 0 0 rgba(255, 205, 234, 1),
  620px 525px 0 0 rgba(255, 205, 234, 1), 625px 525px 0 0 rgba(255, 205, 234, 1),
  630px 525px 0 0 rgba(255, 205, 234, 1), 635px 525px 0 0 rgba(255, 205, 234, 1),
  640px 525px 0 0 rgba(255, 205, 234, 1), 645px 525px 0 0 rgba(255, 205, 234, 1),
  650px 525px 0 0 rgba(255, 205, 234, 1), 655px 525px 0 0 rgba(255, 205, 234, 1),
  660px 525px 0 0 rgba(255, 205, 234, 1), 665px 525px 0 0 rgba(255, 205, 234, 1),
  670px 525px 0 0 rgba(255, 205, 234, 1), 675px 525px 0 0 rgba(255, 205, 234, 1),
  680px 525px 0 0 rgba(255, 205, 234, 1), 685px 525px 0 0 rgba(168, 90, 150, 1),
  690px 525px 0 0 rgba(168, 90, 150, 1), 695px 525px 0 0 rgba(168, 90, 150, 1),
  700px 525px 0 0 rgba(203, 109, 181, 1), 15px 530px 0 0 rgba(203, 109, 181, 1),
  20px 530px 0 0 rgba(203, 109, 181, 1), 25px 530px 0 0 rgba(252, 231, 243, 1),
  30px 530px 0 0 rgba(168, 90, 150, 1), 35px 530px 0 0 rgba(168, 90, 150, 1),
  40px 530px 0 0 rgba(168, 90, 150, 1), 45px 530px 0 0 rgba(168, 90, 150, 1),
  50px 530px 0 0 rgba(168, 90, 150, 1), 55px 530px 0 0 rgba(168, 90, 150, 1),
  60px 530px 0 0 rgba(168, 90, 150, 1), 65px 530px 0 0 rgba(168, 90, 150, 1),
  70px 530px 0 0 rgba(168, 90, 150, 1), 75px 530px 0 0 rgba(168, 90, 150, 1),
  80px 530px 0 0 rgba(168, 90, 150, 1), 85px 530px 0 0 rgba(168, 90, 150, 1),
  90px 530px 0 0 rgba(168, 90, 150, 1), 95px 530px 0 0 rgba(168, 90, 150, 1),
  100px 530px 0 0 rgba(168, 90, 150, 1), 105px 530px 0 0 rgba(168, 90, 150, 1),
  110px 530px 0 0 rgba(168, 90, 150, 1), 115px 530px 0 0 rgba(168, 90, 150, 1),
  120px 530px 0 0 rgba(168, 90, 150, 1), 125px 530px 0 0 rgba(168, 90, 150, 1),
  130px 530px 0 0 rgba(168, 90, 150, 1), 135px 530px 0 0 rgba(168, 90, 150, 1),
  140px 530px 0 0 rgba(168, 90, 150, 1), 145px 530px 0 0 rgba(168, 90, 150, 1),
  150px 530px 0 0 rgba(168, 90, 150, 1), 155px 530px 0 0 rgba(168, 90, 150, 1),
  160px 530px 0 0 rgba(168, 90, 150, 1), 165px 530px 0 0 rgba(168, 90, 150, 1),
  170px 530px 0 0 rgba(168, 90, 150, 1), 175px 530px 0 0 rgba(168, 90, 150, 1),
  180px 530px 0 0 rgba(168, 90, 150, 1), 185px 530px 0 0 rgba(168, 90, 150, 1),
  190px 530px 0 0 rgba(168, 90, 150, 1), 195px 530px 0 0 rgba(168, 90, 150, 1),
  200px 530px 0 0 rgba(168, 90, 150, 1), 205px 530px 0 0 rgba(168, 90, 150, 1),
  210px 530px 0 0 rgba(168, 90, 150, 1), 215px 530px 0 0 rgba(168, 90, 150, 1),
  220px 530px 0 0 rgba(168, 90, 150, 1), 225px 530px 0 0 rgba(168, 90, 150, 1),
  230px 530px 0 0 rgba(168, 90, 150, 1), 235px 530px 0 0 rgba(168, 90, 150, 1),
  240px 530px 0 0 rgba(168, 90, 150, 1), 245px 530px 0 0 rgba(168, 90, 150, 1),
  250px 530px 0 0 rgba(168, 90, 150, 1), 255px 530px 0 0 rgba(168, 90, 150, 1),
  260px 530px 0 0 rgba(168, 90, 150, 1), 265px 530px 0 0 rgba(168, 90, 150, 1),
  270px 530px 0 0 rgba(168, 90, 150, 1), 275px 530px 0 0 rgba(168, 90, 150, 1),
  280px 530px 0 0 rgba(168, 90, 150, 1), 285px 530px 0 0 rgba(168, 90, 150, 1),
  290px 530px 0 0 rgba(168, 90, 150, 1), 295px 530px 0 0 rgba(168, 90, 150, 1),
  300px 530px 0 0 rgba(168, 90, 150, 1), 305px 530px 0 0 rgba(168, 90, 150, 1),
  310px 530px 0 0 rgba(168, 90, 150, 1), 315px 530px 0 0 rgba(168, 90, 150, 1),
  320px 530px 0 0 rgba(168, 90, 150, 1), 325px 530px 0 0 rgba(168, 90, 150, 1),
  330px 530px 0 0 rgba(168, 90, 150, 1), 335px 530px 0 0 rgba(168, 90, 150, 1),
  340px 530px 0 0 rgba(168, 90, 150, 1), 345px 530px 0 0 rgba(168, 90, 150, 1),
  350px 530px 0 0 rgba(168, 90, 150, 1), 355px 530px 0 0 rgba(168, 90, 150, 1),
  360px 530px 0 0 rgba(168, 90, 150, 1), 365px 530px 0 0 rgba(168, 90, 150, 1),
  370px 530px 0 0 rgba(168, 90, 150, 1), 375px 530px 0 0 rgba(168, 90, 150, 1),
  380px 530px 0 0 rgba(168, 90, 150, 1), 385px 530px 0 0 rgba(168, 90, 150, 1),
  390px 530px 0 0 rgba(168, 90, 150, 1), 395px 530px 0 0 rgba(168, 90, 150, 1),
  400px 530px 0 0 rgba(168, 90, 150, 1), 405px 530px 0 0 rgba(168, 90, 150, 1),
  410px 530px 0 0 rgba(168, 90, 150, 1), 415px 530px 0 0 rgba(168, 90, 150, 1),
  420px 530px 0 0 rgba(168, 90, 150, 1), 425px 530px 0 0 rgba(168, 90, 150, 1),
  430px 530px 0 0 rgba(168, 90, 150, 1), 435px 530px 0 0 rgba(168, 90, 150, 1),
  440px 530px 0 0 rgba(168, 90, 150, 1), 445px 530px 0 0 rgba(168, 90, 150, 1),
  450px 530px 0 0 rgba(168, 90, 150, 1), 455px 530px 0 0 rgba(168, 90, 150, 1),
  460px 530px 0 0 rgba(168, 90, 150, 1), 465px 530px 0 0 rgba(168, 90, 150, 1),
  470px 530px 0 0 rgba(168, 90, 150, 1), 475px 530px 0 0 rgba(168, 90, 150, 1),
  480px 530px 0 0 rgba(168, 90, 150, 1), 485px 530px 0 0 rgba(168, 90, 150, 1),
  490px 530px 0 0 rgba(168, 90, 150, 1), 495px 530px 0 0 rgba(168, 90, 150, 1),
  500px 530px 0 0 rgba(168, 90, 150, 1), 505px 530px 0 0 rgba(168, 90, 150, 1),
  510px 530px 0 0 rgba(168, 90, 150, 1), 515px 530px 0 0 rgba(168, 90, 150, 1),
  520px 530px 0 0 rgba(168, 90, 150, 1), 525px 530px 0 0 rgba(168, 90, 150, 1),
  530px 530px 0 0 rgba(168, 90, 150, 1), 535px 530px 0 0 rgba(168, 90, 150, 1),
  540px 530px 0 0 rgba(168, 90, 150, 1), 545px 530px 0 0 rgba(168, 90, 150, 1),
  550px 530px 0 0 rgba(168, 90, 150, 1), 555px 530px 0 0 rgba(168, 90, 150, 1),
  560px 530px 0 0 rgba(168, 90, 150, 1), 565px 530px 0 0 rgba(168, 90, 150, 1),
  570px 530px 0 0 rgba(168, 90, 150, 1), 575px 530px 0 0 rgba(168, 90, 150, 1),
  580px 530px 0 0 rgba(168, 90, 150, 1), 585px 530px 0 0 rgba(168, 90, 150, 1),
  590px 530px 0 0 rgba(168, 90, 150, 1), 595px 530px 0 0 rgba(168, 90, 150, 1),
  600px 530px 0 0 rgba(168, 90, 150, 1), 605px 530px 0 0 rgba(168, 90, 150, 1),
  610px 530px 0 0 rgba(168, 90, 150, 1), 615px 530px 0 0 rgba(168, 90, 150, 1),
  620px 530px 0 0 rgba(168, 90, 150, 1), 625px 530px 0 0 rgba(168, 90, 150, 1),
  630px 530px 0 0 rgba(168, 90, 150, 1), 635px 530px 0 0 rgba(168, 90, 150, 1),
  640px 530px 0 0 rgba(168, 90, 150, 1), 645px 530px 0 0 rgba(168, 90, 150, 1),
  650px 530px 0 0 rgba(168, 90, 150, 1), 655px 530px 0 0 rgba(168, 90, 150, 1),
  660px 530px 0 0 rgba(168, 90, 150, 1), 665px 530px 0 0 rgba(168, 90, 150, 1),
  670px 530px 0 0 rgba(168, 90, 150, 1), 675px 530px 0 0 rgba(168, 90, 150, 1),
  680px 530px 0 0 rgba(168, 90, 150, 1), 685px 530px 0 0 rgba(168, 90, 150, 1),
  690px 530px 0 0 rgba(203, 109, 181, 1), 695px 530px 0 0 rgba(203, 109, 181, 1),
  25px 535px 0 0 rgba(203, 109, 181, 1), 30px 535px 0 0 rgba(203, 109, 181, 1),
  35px 535px 0 0 rgba(203, 109, 181, 1), 40px 535px 0 0 rgba(203, 109, 181, 1),
  45px 535px 0 0 rgba(203, 109, 181, 1), 50px 535px 0 0 rgba(203, 109, 181, 1),
  55px 535px 0 0 rgba(203, 109, 181, 1), 60px 535px 0 0 rgba(203, 109, 181, 1),
  65px 535px 0 0 rgba(203, 109, 181, 1), 70px 535px 0 0 rgba(203, 109, 181, 1),
  75px 535px 0 0 rgba(203, 109, 181, 1), 80px 535px 0 0 rgba(203, 109, 181, 1),
  85px 535px 0 0 rgba(203, 109, 181, 1), 90px 535px 0 0 rgba(203, 109, 181, 1),
  95px 535px 0 0 rgba(203, 109, 181, 1), 100px 535px 0 0 rgba(203, 109, 181, 1),
  105px 535px 0 0 rgba(203, 109, 181, 1), 110px 535px 0 0 rgba(203, 109, 181, 1),
  115px 535px 0 0 rgba(203, 109, 181, 1), 120px 535px 0 0 rgba(203, 109, 181, 1),
  125px 535px 0 0 rgba(203, 109, 181, 1), 130px 535px 0 0 rgba(203, 109, 181, 1),
  135px 535px 0 0 rgba(203, 109, 181, 1), 140px 535px 0 0 rgba(203, 109, 181, 1),
  145px 535px 0 0 rgba(203, 109, 181, 1), 150px 535px 0 0 rgba(203, 109, 181, 1),
  155px 535px 0 0 rgba(203, 109, 181, 1), 160px 535px 0 0 rgba(203, 109, 181, 1),
  165px 535px 0 0 rgba(203, 109, 181, 1), 170px 535px 0 0 rgba(203, 109, 181, 1),
  175px 535px 0 0 rgba(203, 109, 181, 1), 180px 535px 0 0 rgba(203, 109, 181, 1),
  185px 535px 0 0 rgba(203, 109, 181, 1), 190px 535px 0 0 rgba(203, 109, 181, 1),
  195px 535px 0 0 rgba(203, 109, 181, 1), 200px 535px 0 0 rgba(203, 109, 181, 1),
  205px 535px 0 0 rgba(203, 109, 181, 1), 210px 535px 0 0 rgba(203, 109, 181, 1),
  215px 535px 0 0 rgba(203, 109, 181, 1), 220px 535px 0 0 rgba(203, 109, 181, 1),
  225px 535px 0 0 rgba(203, 109, 181, 1), 230px 535px 0 0 rgba(203, 109, 181, 1),
  235px 535px 0 0 rgba(203, 109, 181, 1), 240px 535px 0 0 rgba(203, 109, 181, 1),
  245px 535px 0 0 rgba(203, 109, 181, 1), 250px 535px 0 0 rgba(203, 109, 181, 1),
  255px 535px 0 0 rgba(203, 109, 181, 1), 260px 535px 0 0 rgba(203, 109, 181, 1),
  265px 535px 0 0 rgba(203, 109, 181, 1), 270px 535px 0 0 rgba(203, 109, 181, 1),
  275px 535px 0 0 rgba(203, 109, 181, 1), 280px 535px 0 0 rgba(203, 109, 181, 1),
  285px 535px 0 0 rgba(203, 109, 181, 1), 290px 535px 0 0 rgba(203, 109, 181, 1),
  295px 535px 0 0 rgba(203, 109, 181, 1), 300px 535px 0 0 rgba(203, 109, 181, 1),
  305px 535px 0 0 rgba(203, 109, 181, 1), 310px 535px 0 0 rgba(203, 109, 181, 1),
  315px 535px 0 0 rgba(203, 109, 181, 1), 320px 535px 0 0 rgba(203, 109, 181, 1),
  325px 535px 0 0 rgba(203, 109, 181, 1), 330px 535px 0 0 rgba(203, 109, 181, 1),
  335px 535px 0 0 rgba(203, 109, 181, 1), 340px 535px 0 0 rgba(203, 109, 181, 1),
  345px 535px 0 0 rgba(203, 109, 181, 1), 350px 535px 0 0 rgba(203, 109, 181, 1),
  355px 535px 0 0 rgba(203, 109, 181, 1), 360px 535px 0 0 rgba(203, 109, 181, 1),
  365px 535px 0 0 rgba(203, 109, 181, 1), 370px 535px 0 0 rgba(203, 109, 181, 1),
  375px 535px 0 0 rgba(203, 109, 181, 1), 380px 535px 0 0 rgba(203, 109, 181, 1),
  385px 535px 0 0 rgba(203, 109, 181, 1), 390px 535px 0 0 rgba(203, 109, 181, 1),
  395px 535px 0 0 rgba(203, 109, 181, 1), 400px 535px 0 0 rgba(203, 109, 181, 1),
  405px 535px 0 0 rgba(203, 109, 181, 1), 410px 535px 0 0 rgba(203, 109, 181, 1),
  415px 535px 0 0 rgba(203, 109, 181, 1), 420px 535px 0 0 rgba(203, 109, 181, 1),
  425px 535px 0 0 rgba(203, 109, 181, 1), 430px 535px 0 0 rgba(203, 109, 181, 1),
  435px 535px 0 0 rgba(203, 109, 181, 1), 440px 535px 0 0 rgba(203, 109, 181, 1),
  445px 535px 0 0 rgba(203, 109, 181, 1), 450px 535px 0 0 rgba(203, 109, 181, 1),
  455px 535px 0 0 rgba(203, 109, 181, 1), 460px 535px 0 0 rgba(203, 109, 181, 1),
  465px 535px 0 0 rgba(203, 109, 181, 1), 470px 535px 0 0 rgba(203, 109, 181, 1),
  475px 535px 0 0 rgba(203, 109, 181, 1), 480px 535px 0 0 rgba(203, 109, 181, 1),
  485px 535px 0 0 rgba(203, 109, 181, 1), 490px 535px 0 0 rgba(203, 109, 181, 1),
  495px 535px 0 0 rgba(203, 109, 181, 1), 500px 535px 0 0 rgba(203, 109, 181, 1),
  505px 535px 0 0 rgba(203, 109, 181, 1), 510px 535px 0 0 rgba(203, 109, 181, 1),
  515px 535px 0 0 rgba(203, 109, 181, 1), 520px 535px 0 0 rgba(203, 109, 181, 1),
  525px 535px 0 0 rgba(203, 109, 181, 1), 530px 535px 0 0 rgba(203, 109, 181, 1),
  535px 535px 0 0 rgba(203, 109, 181, 1), 540px 535px 0 0 rgba(203, 109, 181, 1),
  545px 535px 0 0 rgba(203, 109, 181, 1), 550px 535px 0 0 rgba(203, 109, 181, 1),
  555px 535px 0 0 rgba(203, 109, 181, 1), 560px 535px 0 0 rgba(203, 109, 181, 1),
  565px 535px 0 0 rgba(203, 109, 181, 1), 570px 535px 0 0 rgba(203, 109, 181, 1),
  575px 535px 0 0 rgba(203, 109, 181, 1), 580px 535px 0 0 rgba(203, 109, 181, 1),
  585px 535px 0 0 rgba(203, 109, 181, 1), 590px 535px 0 0 rgba(203, 109, 181, 1),
  595px 535px 0 0 rgba(203, 109, 181, 1), 600px 535px 0 0 rgba(203, 109, 181, 1),
  605px 535px 0 0 rgba(203, 109, 181, 1), 610px 535px 0 0 rgba(203, 109, 181, 1),
  615px 535px 0 0 rgba(203, 109, 181, 1), 620px 535px 0 0 rgba(203, 109, 181, 1),
  625px 535px 0 0 rgba(203, 109, 181, 1), 630px 535px 0 0 rgba(203, 109, 181, 1),
  635px 535px 0 0 rgba(203, 109, 181, 1), 640px 535px 0 0 rgba(203, 109, 181, 1),
  645px 535px 0 0 rgba(203, 109, 181, 1), 650px 535px 0 0 rgba(203, 109, 181, 1),
  655px 535px 0 0 rgba(203, 109, 181, 1), 660px 535px 0 0 rgba(203, 109, 181, 1),
  665px 535px 0 0 rgba(203, 109, 181, 1), 670px 535px 0 0 rgba(203, 109, 181, 1),
  675px 535px 0 0 rgba(203, 109, 181, 1), 680px 535px 0 0 rgba(203, 109, 181, 1),
  685px 535px 0 0 rgba(203, 109, 181, 1);
 height: 5px;
 width: 5px;
}

.container {
 position: absolute;
 padding: 0;
 top: 50%;
 left: 50%;
 transform: translate(-50%, -50%);
 z-index: -1;
 width: 705px;
 height: 515px;
}

.folders {
 position: absolute;
 top: 50%;
 left: 50%;
 transform: translate(-50%, -50%);
 z-index: 2;
}
.bg {
 position: absolute;
 top: 50%;
 left: 50%;
 transform: translate(-50%, -50%);
 width: 675px;
 z-index: -2;
 height: 495px;
 background-image: linear-gradient(
  var(--english-violet),
  var(--royal-purple),
  var(--onyx)
 );
}
.folder:hover {
 position: absolute;
 transform: translateX(-205px) translateY(80px) scale(1.1);
}
.folder {
 position: absolute;
 transform: translateX(-190px) translateY(90px);
}

.folder::after {
 content: "";
 position: absolute;
 width: 97px;
 height: 80px;
}

.folder2:hover {
 position: absolute;
 transform: translateX(-75px) translateY(80px) scale(1.1);
}
.folder2 {
 position: absolute;
 transform: translateX(-65px) translateY(90px);
}
.folder2::after {
 content: "";
 position: absolute;
 width: 97px;
 height: 80px;
}

.text {
 position: absolute;
 transform: translateX(-190px) translateY(185px) scale(0.7);
}
.text:hover {
 position: absolute;
 transform: translateX(-200px) translateY(185px) scale(0.75);
}
.text::after {
 content: "";
 position: absolute;
 width: 97px;
 height: 80px;
}
.log {
 position: absolute;
 transform: translateX(-70px) translateY(185px) scale(0.7);
}
.log:hover {
 position: absolute;
 transform: translateX(-80px) translateY(185px) scale(0.75);
}
.log::after {
 content: "";
 position: absolute;
 width: 97px;
 height: 80px;
}

.error {
 position: absolute;
 transform: translateX(278px) translateY(12px) scale(0.4);
}

@keyframes horizontalStatic {
 0% {
  left: -5px;
 }
 20% {
  left: 3px;
 }
 50% {
  left: 5px;
 }
 75% {
  left: -2px;
 }
 80% {
  left: 1px;
 }
 100% {
  left: -3px;
 }
}

@keyframes verticalStatic {
 0% {
  top: -5px;
 }
 20% {
  top: 3px;
 }
 50% {
  top: 5px;
 }
 75% {
  top: -2px;
 }
 80% {
  top: 1px;
 }
 100% {
  top: -3px;
 }
}

// Massive kudos to this tool: <https://www.pixelartcss.com/>
// Inspired by <https://dribbble.com/tags/old_computer_aesthetic> &
// <https://d3ui957tjb5bqd.cloudfront.net/uploads/2020/09/29112311/1530x900-horizontal-51.jpg>
```

> FOR THE ABOVE IT IS IMPERITIVE TO NOTE WE ARE ONLY INTERESTED IN THE PIXEL ART FOLDER AND ITS ANIMATION. WE ALREADY HAVE BUTTON STANDARDS INCLUDED HERE. THAT SHOULD BE UTILIZED.

## FONTS

### THE LAST OF US, LARGE BOLD WHITE TEXT OVERLAY FOR SIGNIFICANT TITLES, FIRST DISCOUVERIES, ACTS OR PIVOTAL EVENTS ONLY. THIS IS NOT A REPLACEMENT FOR HEADING FONTS. IT IS A STYLIZED NEAR FULL SCREEN AESTHETIC, SIMILAR TO HOW THE LAST OF US LAID OVER THEIRS

```html
<h1>Annoying CRT retro flicker</h1>
<p>Come for the nostalgia, stay for the vertigo-inducing jiggle effect. Can be used in a more artistic / less queasy way without the animation. Works best on large blocky text.</p>
```

```css
/*Nintendoid font from <https://www.splintered.co.uk/experiments/132/>*/

@font-face {
  font-family: 'Nintendoid1';
  font-style: normal;
  font-weight: 400;
  src:  url(data:font/ttf;base64,d09GMgABAAAAAApIAAoAAAAAMCAAAAn8AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAABmAAhkQKulCoWAuDcAABNgIkA4NsBCAFlAUHIBuGJKOQbi5O1ihK9OQ72X85oIfY2gK+CyxFiCisUzncw9oyGDFOlihbz7T+bP393qOyeipby7N3hogwAsT53ornv9+P33qCS+J/z7hPlwyVSra7I5EGVVQSjQzTKYl0CIvF3CQ3PMIqlERZWoK2eakIH5I+IliapSjCwhZaWSnX76v7lGTHP1+W7J+79JrXlwLi2PmAsbgDz5147dwRcAKc1sK2LSK9aapt0zDbCW6Xny596331gUUkvpAfAoxETUPmIYX13Y4cPB0LAPyvaT97+1u9O6r6M6HfoBCuCYPHolDIu333spO87G8tv/FLC73sJpkhCb14UM3SXasS7dEIjfzaIZSEh/wbHySQ/2cJJG0t9CzQCNu6ylMLLJWSUNtEXW+XS1jp2iakRlWFq3N0xg8hP7tY45+qHy5xwwLXK+gVPTv8hhEQBiwFOH323BlHTU5ND4EhgikYMgSToMeA9Qahe2bsbmHepNHLx213PfDYU8+989FXP/2dzCe3TE5P7p98NjVdhUnIhu6zzWX7/tez/tV//dWvvte3+lrv6229qud1wX+7d2x96beg9txUSH4WAODmIYD/wC/SH9WvLq2VJ0Sd1Y2UwkUJjNKIkTTQKPakmQScM9osg+DpxEqb3uwROKmqRKMXXbu2YqlMA9ujItaqtzlrixCkLF0tt3luWDZzHGpxXpfWXitlKsKFSNjkrEeIZZsGV1ewZ5HvqBVp0TrX9Erp3OYPWueKgkXhzEr70fxii2u/z5blFklHYBhBoGP0lXzv4De4uMwpKrSntkcl33vjBAydMnpkNEFlgKUrxliAod3oQlA5KKW5oISyrb7PA2qrDSeHZ1xbwWQjBTBo4wYelA2Xe34eaZ+hrV2B22hETjC1fO0JUzQdQwfwIeUhx/MzOjGKG1USGnkMHWbpJBqPnSYlhrSGeTF3UA1tSUf5MmNKvB1wClimfQIyoGhdhYmI83J1QpwVzBB/4oQMrMvgul2trCZ4v2AyCGi8BYVa/eXEg4KLpKK2C8gy1tyTNprozSwSUZJONnDDU+qtKNTJVIZiLhoXIq3UjbI43QLzDupOhYS85rJZyxmeI8hRCyqIJq53GSExkli0k7h8YzCKYiOsyMibOr0DgtkTI+SzPcG1c5ngkQYE0KMkIlc16MfYCN4wim1dBO/IQpwbGnvKTCNwArqAGlOLFe9t55iHlwcrLaezYaNkjkbHAAgUxBZCiyztLtqz4HGidoZCzGf4ZZFx10JiW8W4mWHFVzc0i+QUJxjALjaBB0XFsYidYWQjj6RYoccX65Vsq6jTHkrpISdKTDuMEgv/BE/Iy4W5xfjVTLGMdpCwhWMoyresRQEzL9IniooRJgixM1BFoWWPxNIHertfRjNxNvcaM30xDMr1xqOCjPoqRHHBLOQNNoJ6ggcug0ntcgIwCQNSty9HTzooKEFleBK2hQ7rPcEHldQq8sQ2IszjIdZJaw7raTBve6yukbxRvGueCB1VKE8wCcobHUYakFoVS6xWzQQgQfkpDRsSZGpP2/zq1DO116ezZhlNIDuoB1NUNOEz9RQle0vUz86lo5YIWTsEV+O7KFGV7120bJh6qWGef0XfXvNY9x8vyx/l23+KHjz0608k7N96KYlEqiJaRRJRLUk1SZIEwahuZWrSYblVol2tTWBVE1Tp4qIy0tlU9grwpiTnIuc/dvBWHCdlrgjgHFkzO8LlLaK9tZBopTIhZhGZdjGJaGKNxJBJ0XF6NqWaclNtysr0ks4n2CoRs2YxnCs4yCOCV+aipBRgkc5QkrSTPgqGR7G0/YxIg591IBiPj04CnPx9AG+1IGs2UwwpQlj8mogXmdK6nFAJQm1Oo9Fjr4oSdbFIGAnMszMrA1RBgHIhLoG4hn48F1NVahIWx8FalGILaLISKIsQThjdzA+HSzVcSUKvubhK6LGCWB8WtRUjd/DPMFr1m7igjaqc5rZvZN1x2shNwmQJc1ffrH1Ta/BaD5faMiEhDPW+/JJqdRxqURWyZtfZ8N7eXQAuE1QhB+TxnkGpW18QVZBlJaNMNVgLBdfyutZ/C+mU6xZ3ko75yZBFXcG3eIoDbe4cq+46y2TB9yjiTFQdJSheCuXb7qfu5JNfp26ev7Dq4Hfgz/80uqyMFixW8KNDKoyBke7/lMsxjOh0PUqmzHpEIhEyMqpN6PFelSHpKnIOWPZliD+53pc5kvNrqdrWocg0OSxJv6PDZTutAOmk3diSWzpzCWaQKJGKPYz1DrNylyW8bo4YU3HBklSD16rUR5zG+0lc7BaqbJ9gf6+Xenv76gaCtN8MXhUAzvTfD6iYImE7GYd2nLVnQxINu8sp9lTFNd9IHbjDqjZcD+6zsRA3to468zwWtO9rqdf8GyUegQC19wfTdr7+V5TdG2YfsXTucLmE9YaYdiSysPOSJfzJEujjcdsuEbBoSsbVcE+mjXZqXry1g1bf6z5su+SHJY9ef9zBQr7ftM9WyImbQd/uGmJdK/HysGlVX+vY//Xo+Sdfn6pyzc2THc/Vd0M6AW+Fx+zCnfdkXOEsPF99QCabwwHegBFwwN7jsPba9mK+0VjdKQ42+sIeWLBNHrYDw46Ur9Y58RROMR2EkvLHvhz0JT6QQ7xUNCc+Yel6iw08+3fD28Dh3/ZC3o773ivbdMVjTMLGZ/j0B8Xmf3y1+meelLcyzwWT/D7Je9Xh7EyN3j7pu392dlDHHSjVp/fAlcq92DFHsNEeN5YfzUpXtVez7TM/pMl/xBDYjemNSzeGmhna1Eu4eue4OP3L5ez52f6L6XeGlQvJqMqIFwjwComMGB3wCBUdB+zatmPXMxIJJ7ISYoEd7xyv6KHsWhKJDyIrDAG4cEVJQHjkNydjpCkmd25sa7YVwv3vTBhAQGTIcgYo64BkBlz7cAfQFIQaBHdO3CyeF1n8GuqBGwPtViDE6JSizPBRZvAsG0YyUGJfVWwI8p1RgDnEgFaQnuSfnogAvPYmLjnZmPecDLIMM8Nk9MQ6bRiDCiQGHqTmxGCQCQUx0UMMEFlCkHdd+QCeywYJwuMgiyIot+cnpvjE0hSdrj3zRDU2cgvm2DjxIhdG6rkDHfiXBj36sYMVo/cQdPCZy5ibJWw6aJVguEFRcipupmfTXkGsjH6QdZBxPBio3SWHIBSASJBMkWVgsANZ1hNCd0AFkEgvBzAeNCjWyDR2ZMjEI/CGcFMVhHwqE0cSsCKSwUQNENhzFsiGBABoEQf3qzGJ8GALxtn7mcKCZE45dNR7un27lBj7qZ8cFzLH8fSXK124kAOZB85ItotoJfVhm2QI4iaxGu1lnooZZlgkd76vVil71c6wcs3A1Ugm748CI8cUji2XjoKaC1pJb97G2NxaaKaPtc6d2fdyvt+Owbr2pmb2AA==) format('woff2');
}
html { background: #111;
       padding: 1em;
       font-family: Nintendoid1;
       color: #eee;
       font-size: 1em;
       line-height: 1;
       text-shadow: 0.06rem 0 0.06rem #ea36af, -0.125rem 0 0.06rem #75fa69;
       letter-spacing: 0.125em;
       animation-duration: 0.01s;
       animation-name: textflicker;
       animation-iteration-count: infinite;
       animation-direction: alternate;
}
h1 { font-size: 5em; }

@keyframes textflicker {
  from {
    text-shadow: 1px 0 0 #ea36af, -2px 0 0 #75fa69;
  }
  to {
    text-shadow: 2px 0.5px 2px #ea36af, -1px -0.5px 2px #75fa69;
  }
}
```

## TEXTURES

### PIXEL ART STONE WALL BLOCK (GREAT OPTION AND WORLD ACCURATE)

> CAVIET, ONLY ONE VARIANT.

```html
<canvas id="canvas"></canvas>
```

```css
body {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #2D3741;
}

canvas {
  cursor: pointer;
}
```

> (Babel)

```js
(() => {
  function generateCrack({ deepness, segments } = {}) {
    function generateChild(segments, children, deepness) {
      const crackAt = Math.floor(Math.random() * segments / 2)
      return new Array(segments).join(' ').split(' ').map((segment, index) => {
        return children + 1 >= deepness ? [] :
          crackAt !== index ? [] :
            [generateChild(segments / 2, children + 1, deepness)]
      })
    }
    return generateChild(segments, 0, deepness)
  }

  function drawCrack(options) {
    const {
      crack,
      ctx, x, y,
      fillStyle, shadeStyle, tintStyle,
      segmentLength, segmentWidth,
      variation
    } = options

    const lineWidth = segmentWidth || 2
    ctx.lineWidth = lineWidth
    crack.forEach(segment => {
      const xVariation = (Math.random() >= .5 ? 1 : -1) * (
        Math.random() * variation
      )
      const newX = x + xVariation
      const newY = y + xVariation + segmentLength
      // Shade
      if (shadeStyle) {
        ctx.beginPath()
        ctx.strokeStyle = shadeStyle
        ctx.moveTo(
          x + Math.random() * lineWidth,
          y - Math.random() * lineWidth
        )
        ctx.lineTo(
          newX + Math.random() * lineWidth,
          newY - Math.random() * lineWidth
        )
        ctx.stroke()
      }
      // Tint
      if (tintStyle) {
        ctx.beginPath()
        ctx.strokeStyle = tintStyle
        ctx.moveTo(
          x - Math.random() * lineWidth,
          y + Math.random() * lineWidth
        )
        ctx.lineTo(
          newX - Math.random() * lineWidth,
          newY + Math.random() * lineWidth
        )
        ctx.stroke()
      }
      // segment
      ctx.beginPath()
      ctx.strokeStyle = fillStyle
      ctx.moveTo(x, y)
      ctx.lineTo(newX, newY)
      ctx.stroke()
      if (segment.length) {
        drawCrack({
          crack: segment,
          ctx, x: newX, y: newY,
          fillStyle, shadeStyle, tintStyle,
          segmentLength: segmentLength / 2,
          variation: variation * 1.6
        })
      }
    })
  }

  function isTileHere(x, y, tile) {
    const tileTop = tile.y
    const tileRight = tile.x + tile.width
    const tileBottom = tile.y + tile.height
    const tileLeft = tile.x
    return (
      (x >= tileLeft && x <= tileRight) &&
      (y >= tileTop && y <= tileBottom)
    )
  }

  function getEmptySpot(width = 1, height = 1, tiles = []) {
    let x = 0
    let y = 0
    let limit = width * height
    if (!tiles.length) {
      return [x, y]
    }
    while (limit > 0) {
      let tileIndex = 0
      let isBlocked = false
      o: while (tileIndex < tiles.length) {
        let tile = tiles[tileIndex]
        if (isTileHere(x, y, tile)) {
          isBlocked = true
          break o
        }
        tileIndex++
      }
      if (!isBlocked) {
        return [x, y]
      }
      limit--
      if (x < width) {
        x++
      } else {
        x = 0
        y++
      }
    }
    return null
  }

  function getLayout(options = {}) {
    const {
      variationFactor = .5,
      totalWidth = 512,
      totalHeight = 512,
      baseTileSize = 128
    } = options

    const baseSize = baseTileSize
    const variation = baseSize * variationFactor
    const minSize = baseSize - variation
    const maxSize = baseSize + variation
    const tiles = []
    
    let limit = 100

    while (true) {
      if (limit-- < 0) {
        alert('something went wrong')
        break
      }

      const emptySpot = getEmptySpot(
        totalWidth,
        totalHeight,
        tiles
      )

      if (!emptySpot) {
        break
      }

      const [ x, y ] = emptySpot

      const varyWidth = Math.random() >= .8 ? minSize :
        Math.random() >= .66 ? maxSize : baseSize

      let width = varyWidth
      let tileEndX = x + width

      if (tileEndX > totalWidth) {
        if (x + baseSize <= totalWidth) {
          width = x + baseSize
        } else if (x + minSize <= totalWidth) {
          width = x + minSize
        } else {
          width -= (tileEndX - totalWidth)
        }
      }

      if (totalWidth - tileEndX < minSize) {
        const gap = totalWidth - tileEndX
        width += gap
      }

      let neighbourIndex = 0
      let lim = 1000
      o: while (lim-- > 0 && neighbourIndex < tiles.length) {
        let neighbour = tiles[neighbourIndex]
        if (isTileHere(tileEndX, y, neighbour)) {
          width = neighbour.x - 1 - x
          break o
        }
        neighbourIndex++
      }

      const varyHeight = Math.random() >= .8 ? minSize :
        Math.random() >= .75 ? maxSize : baseSize

      let height = varyHeight
      let tileEndY = y + height

      const gap = totalHeight - tileEndY
      if (gap > 0 && gap < minSize) {
        height = gap
      }

      if (tileEndY > totalHeight) {
        const overflow = tileEndY - totalHeight
        height -= overflow
      }

      if (width < minSize) {
        height = Math.min(width, height)
      }

      let lastTile = tiles[tiles.length - 1]
      if (lastTile && y < lastTile.y && tileEndY > lastTile.y) {
        height = lastTile.y - y
      }

      tiles.push({
        x,
        y,
        width,
        height
      })
    }

    return tiles
  }

  const width = 480
  const height = 360
  const baseTileSize = 96
  const canvas = document.getElementById('canvas')
  canvas.width = width
  canvas.height = height
  canvas.addEventListener('click', generate)
  generate()

  function generate() {
    const ctx = canvas.getContext('2d')

    const tileOptions = {
      base: {
        color: '#575935'
      },
      shade: {
        color: '#484024',
        width: 5
      },
      darkerShade: {
        color: '#2F2419',
        width: 3
      },
      tint: {
        color: '#70744C',
        width: 5
      }
    }

    const layoutOptions = {
      totalWidth: width,
      totalHeight: height,
      baseTileSize,
      variationFactor: .25
    }

    const tiles = getLayout(layoutOptions)

    tiles.forEach((tile, index) => {
      // Base
      ctx.fillStyle = tileOptions.base.color
      ctx.fillRect(tile.x, tile.y, tile.width, tile.height)

      // Darker Shade
      ctx.beginPath()
      ctx.strokeStyle = tileOptions.darkerShade.color
      ctx.lineWidth = tileOptions.darkerShade.width
      ctx.moveTo(
        tile.x,
        tile.y
      )
      ctx.lineTo(
        tile.x,
        tile.y + tile.height
      )
      ctx.lineTo(
        tile.x + tile.width,
        tile.y + tile.height
      )
      ctx.stroke()

      let shadeWidth, tintWidth

      // Shade
      shadeWidth = tileOptions.shade.width
      ctx.beginPath()
      ctx.strokeStyle = tileOptions.shade.color
      ctx.lineWidth = tileOptions.shade.width
      ctx.moveTo(
        tile.x + shadeWidth,
        tile.y
      )
      ctx.lineTo(
        tile.x + shadeWidth,
        tile.y + tile.height - shadeWidth
      )
      ctx.lineTo(
        tile.x + tile.width,
        tile.y + tile.height - shadeWidth
      )
      ctx.stroke()

      // Lighting
      shadeWidth = shadeWidth + tileOptions.tint.width / 2
      tintWidth = tileOptions.tint.width / 2
      ctx.beginPath()
      ctx.strokeStyle = tileOptions.tint.color
      ctx.lineWidth = tileOptions.tint.width
      ctx.moveTo(
        tile.x + shadeWidth,
        tile.y + tintWidth
      )
      ctx.lineTo(
        tile.x + tile.width - tintWidth,
        tile.y + tintWidth
      )
      ctx.lineTo(
        tile.x + tile.width - tintWidth,
        tile.y + tile.height - shadeWidth
      )
      ctx.stroke()

      // Shade vertical
      noise.seed(Math.random())
      var noiseX = 0
      var noiseY = 500 + Math.round(Math.random() * 20500)
      var noiseYCopy = noiseY
      var distortionX = tile.x
      var distortionY = tile.y
      while (distortionY < tile.y + tile.height) {
        distortionY += 1
        distortionX = tile.x + tileOptions.shade.width - noise.simplex2(noiseX += .05, noiseY += .05) * tileOptions.shade.width
        if (Math.random() >= .5) {
          ctx.fillStyle = tileOptions.shade.color
          ctx.fillRect(
            distortionX,
            distortionY,
            tileOptions.shade.width / 1.25,
            tileOptions.shade.width / 1.25
          ) 
        }
      }

      // Darkershade vertical
      var noiseY = noiseYCopy
      var distortionX = tile.x
      var distortionY = tile.y
      while (distortionY < tile.y + tile.height) {
        distortionY += tileOptions.darkerShade.width / 2
        distortionX = tile.x + (tileOptions.darkerShade.width / 2) - noise.simplex2(noiseX += .05, noiseY += .05) * tileOptions.darkerShade.width / 2
        if (Math.random() >= .125) {
          if (Math.random() >= .5) {
            ctx.fillStyle = tileOptions.darkerShade.color
            ctx.fillRect(
              tile.x,
              distortionY,
              distortionX - tile.x,
              tileOptions.darkerShade.width
            )
          } else {
            ctx.fillStyle = tileOptions.shade.color
          }
          ctx.fillRect(
            distortionX,
            distortionY,
            tileOptions.darkerShade.width / 1.25,
            tileOptions.darkerShade.width / 1.25
          ) 
        }
      }

      // Tint horizontal
      noise.seed(Math.random())
      var noiseX = 0
      var noiseY = 500 + Math.round(Math.random() * 25000)
      var distortionX = tile.x
      var distortionY = tile.y
      while (distortionX < tile.x + tile.width) {
        distortionX += 1
        distortionY = tile.y + (tileOptions.tint.width / 2) - noise.simplex2(noiseX += .05, noiseY += .05) * tileOptions.tint.width
        if (Math.random() >= .5) {
          if (Math.random() >= .5) {
            ctx.fillStyle = tileOptions.tint.color
            ctx.fillRect(
              distortionX,
              distortionY,
              tileOptions.tint.width / 1.5,
              tileOptions.tint.width / 1.5
            ) 
          } else {
            ctx.fillStyle = tileOptions.base.color
            ctx.fillRect(
              distortionX,
              distortionY,
              tileOptions.base.width / 1.75,
              tileOptions.base.width / 1.75
            ) 
          }
        }
      }

      // Tint vertical
      noise.seed(Math.random())
      var noiseX = 0
      var noiseY = 500 + Math.round(Math.random() * 20500)
      var distortionX = tile.x + tile.width
      var distortionY = tile.y
      while (distortionY < tile.y + tile.height) {
        distortionY += 1
        distortionX = tile.x + tile.width - tileOptions.tint.width - noise.simplex2(noiseX += .05, noiseY += .05) * tileOptions.tint.width
        if (Math.random() >= .5) {
          ctx.fillStyle = tileOptions.tint.color
          ctx.fillRect(
            distortionX,
            distortionY,
            tileOptions.tint.width / 1.5,
            tileOptions.tint.width / 1.5
          ) 
        }
      }

      // Shade horizontal
      noise.seed(Math.random())
      var noiseX = 0
      var noiseY = 500 + Math.round(Math.random() * 25000)
      var noiseYCopy = noiseY
      var distortionX = tile.x
      var distortionY = tile.y + tile.height
      while (distortionX < tile.x + tile.width) {
        distortionX += 1
        distortionY = tile.y + tile.height - (tileOptions.shade.width * 2) - noise.simplex2(noiseX += .05, noiseY += .05) * tileOptions.shade.width
        if (Math.random() >= .5) {
          if (Math.random() >= .5) {
            ctx.fillStyle = tileOptions.shade.color
            ctx.fillRect(
              distortionX,
              distortionY,
              tileOptions.shade.width / 1.25,
              tileOptions.shade.width / 1.25
            ) 
          } else {
            ctx.fillStyle = tileOptions.base.color
            ctx.fillRect(
              distortionX,
              distortionY,
              tileOptions.shade.width / 1.5,
              tileOptions.shade.width / 1.5
            ) 
          }
        }
      }

      // Darkershade horizontal
      var noiseY = noiseYCopy
      var distortionX = tile.x
      var distortionY = tile.y + tile.height
      while (distortionX < tile.x + tile.width) {
        distortionX += tileOptions.darkerShade.width / 1.25
        distortionY = tile.y + tile.height - tileOptions.darkerShade.width - noise.simplex2(noiseX += .01, noiseY += .01) * tileOptions.darkerShade.width
        if (Math.random() >= .25) {
          if (Math.random() >= .4) {
            ctx.fillStyle = tileOptions.darkerShade.color
            if (Math.random() >= .5) {
              ctx.fillRect(
                distortionX,
                distortionY,
                tileOptions.darkerShade.width / 1.5,
                tile.y + tile.height - distortionY
              )
            }
          } else {
            ctx.fillStyle = tileOptions.shade.color
          }
          ctx.fillRect(
            distortionX,
            distortionY,
            tileOptions.darkerShade.width / 1.25,
            tileOptions.darkerShade.width / 1.25
          ) 
        }
      }

      // Cracks
      if (tile.width > width / 10 && Math.random() >= .5) {
        const showLighting = Math.random() >= .5
        drawCrack({
          ctx,
          x: tile.width / 5 + tile.x + Math.random() * (tile.width - tile.width / 5),
          y: Math.random() >= .5 ? tile.y : tile.y + tile.height - 40,
          fillStyle: tileOptions.shade.color,
          shadeStyle: showLighting ? tileOptions.darkerShade.color : null,
          tintStyle: showLighting ? tileOptions.tint.color : null,
          crack: generateCrack({
            deepness: 2,
            segments: 4
          }),
          segmentLength: 10,
          segmentWidth: 1,
          variation: 5
        })
      }

      if (tile.width > width / 20 && Math.random() >= .5) {
        drawCrack({
          ctx,
          x: tile.width / 5 + tile.x + Math.random() * (tile.width - tile.width / 5),
          y: tile.height / 5 + tile.y + Math.random() * (tile.height - tile.height / 5),
          fillStyle: tileOptions.shade.color,
          crack: generateCrack({
            deepness: 2,
            segments: 4
          }),
          segmentLength: 5,
          segmentWidth: 1,
          variation: 3
        })
      }

      if (tile.width > width / 20 && Math.random() >= .25) {
        var i = Math.round(Math.random() * 4)
        while (i-- > 0) {
          drawCrack({
            ctx,
            x: tile.width / 5 + tile.x + Math.random() * (tile.width - tile.width / 5),
            y: tile.y + Math.random() * tile.height,
            fillStyle: tileOptions.shade.color,
            shadeStyle: Math.random() >= .5 ? tileOptions.darkerShade.color : null,
            tintStyle: Math.random() >= .5 ? tileOptions.tint.color : null,
            crack: generateCrack({
              deepness: 1,
              segments: 3
            }),
            segmentLength: 1,
            segmentWidth: 3,
            variation: 2
          })
        }
      }
    })
  }
})()

### CHANCE ENCOUNTER DICE (REQUIRES STRIPPING OF BACKGROUND, WE ONLY REQUIRE THE DYE ASSET)

(index.pen.html)

<canvas id="bg"></canvas>

(style.css)

body {
  margin:0
}

(script.js)

/*global THREE*/

// Configuration
const Config = {
    pixelSize: 10,
    d20Radius: 55,
    labelScale: 12,
    lineWidth: 15,
    rollDuration: 2000,
    stopDuration: 3000,
    initialScale: 1.2,
    gravity: 0.002,
    groundLevel: 0,
    flashDuration: 500,
    flashColor: 0xff0000,
    labelCanvasSize: 8,
    labelFontSize: 8,
    labelFont: 'bold 8px monospace',
    labelTextColor: '#ffffff',
    backgroundColor: 0x1a1a1a,  // Changed to match CRT shader's grey
    faceNumbers: [9, 6, 16, 3, 19, 14, 11, 1, 17, 8, 18, 5, 15, 12, 2, 4, 13, 7, 10, 20],
    initialAngularVelocity: 1,
    angularVelocityDamping: 0.98,
    bounceSpeed: 0.05,
    bounceDamping: -0.6,
    pixelHeightRatio: 2.0
};

// Shaders
const CRTShader = {
    uniforms: {
        tDiffuse: { value: null },
        time: { value: 0.0 },
        resolution: { value: new THREE.Vector2() },
        curvature: { value: 4.0 },      // Increased curvature
        vignetteBoost: { value: 1.2 },
        vignetteDarkness: { value: 1.5 },
        scanlineIntensity: { value: 0.075 },
        scanlineCount: { value: 800.0 },
        flickerAmount: { value: 0.1 },
        bleedAmount: { value: 10.0 },
        horizontalBleed: { value: 0.4 }, // Adjusted for better bloom
        bloomStrength: { value: 0.4 },   // Adjusted for wider bloom
        bloomSpread: { value: 0.01 },    // Increased spread
        glowStrength: { value: 0.8 },    // Reduced strength for wider radius
        glowSpread: { value: 0.02 },     // Much larger spread
        glowThreshold: { value: 0.4 },   // Lower threshold to catch more bright areas
        colorBleedStrength: { value: 0.25 },    // New uniform for color bleeding, increased to 0.25
        colorBleedSpread: { value: 0.0004 },    // New uniform for bleed spread, adjusted to 0.0004
        chromaticAberration: { value: 0.004 }, // Chromatic aberration intensity
        gridIntensity: { value: 0.2 },      // Adjusted for better visibility
        gridScale: { value: 2 },         // Reduced scale for more visible grid
        backgroundColor: { value: new THREE.Vector3(0.1, 0.1, 0.1) },  // Grey background tint
        borderWidth: { value: 0.03 },    // Width of the border
        vignetteAmount: { value: 0.5 },  // Strength of the vignette
    },
    vertexShader: `
varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform float time;
        uniform vec2 resolution;
        uniform float curvature;
        uniform float vignetteBoost;
        uniform float vignetteDarkness;
        uniform float scanlineIntensity;
        uniform float scanlineCount;
        uniform float flickerAmount;
        uniform float bleedAmount;
        uniform float horizontalBleed;
        uniform float bloomStrength;
        uniform float bloomSpread;
        uniform float glowStrength;
        uniform float glowSpread;
        uniform float glowThreshold;
        uniform float colorBleedStrength;
        uniform float colorBleedSpread;
        uniform float chromaticAberration;
        uniform float gridIntensity;
        uniform float gridScale;
        uniform vec3 backgroundColor;
        uniform float borderWidth;
        uniform float vignetteAmount;
        varying vec2 vUv;

        vec2 curveRemapUV(vec2 uv) {
            // Convert to -1 to 1 range
            vec2 cuv = uv * 2.0 - 1.0;
            
            // Apply stronger curve towards edges
            vec2 offset = abs(cuv.yx) / vec2(curvature);
            cuv += cuv * offset * offset;
            
            // Add barrel distortion
            float barrelDistance = length(cuv);
            cuv *= 1.0 + barrelDistance * barrelDistance * 0.03;
            
            // Return to 0-1 range
            return cuv * 0.5 + 0.5;
        }

        // Improved brightness calculation that preserves color
        float getBrightness(vec3 color) {
            return dot(color, vec3(0.2, 0.7, 0.1)); // Weight green higher
        }

        float getVignette(vec2 uv) {
            uv = uv * 2.0 - 1.0;
            return smoothstep(1.0, 0.2, length(uv) * vignetteAmount);
        }

        void main() {
            vec2 uv = curveRemapUV(vUv);
            vec4 finalColor = vec4(backgroundColor, 1.0);
            float scanline = 1.0;
            float flicker = 1.0;
            
            // Improved border handling
            float border = 1.0;
            if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
                gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
                return;
            }
            
            // Smooth border transition
            if (uv.x < borderWidth) border *= smoothstep(0.0, borderWidth, uv.x);
            if (uv.x > 1.0 - borderWidth) border *= smoothstep(1.0, 1.0 - borderWidth, uv.x);
            if (uv.y < borderWidth) border *= smoothstep(0.0, borderWidth, uv.y);
            if (uv.y > 1.0 - borderWidth) border *= smoothstep(1.0, 1.0 - borderWidth, uv.y);

            // Sample with chromatic aberration
            float chromaticOffset = chromaticAberration;
            vec4 r = texture2D(tDiffuse, uv + vec2(chromaticOffset, 0.0));
            vec4 g = texture2D(tDiffuse, uv);
            vec4 b = texture2D(tDiffuse, uv - vec2(chromaticOffset, 0.0));
            vec4 baseColor = vec4(r.r, g.g, b.b, g.a);

            // Sample with color separation
            vec4 rColor = texture2D(tDiffuse, uv + vec2(colorBleedSpread, 0.0));
            vec4 bColor = texture2D(tDiffuse, uv - vec2(colorBleedSpread, 0.0));
            
            vec4 centerColor = mix(baseColor, vec4(rColor.r, baseColor.g, bColor.b, baseColor.a), colorBleedStrength);

            vec4 glow = vec4(0.0);
            float brightness = getBrightness(centerColor.rgb);
            
            // Enhanced glow calculation with wider radius
            if(brightness > glowThreshold) {
                float glowFactor = 0.0;
                
                // Sample more points with much wider spacing
                for(float i = 1.0; i <= 8.0; i++) {
                    float offset = i * glowSpread;
                    float weight = pow(0.85, i); // Reduced falloff for wider glow
                    
                    vec4 sampleL = texture2D(tDiffuse, uv - vec2(offset, 0.0));
                    vec4 sampleR = texture2D(tDiffuse, uv + vec2(offset, 0.0));
                    vec4 sampleU = texture2D(tDiffuse, uv - vec2(0.0, offset));
                    vec4 sampleD = texture2D(tDiffuse, uv + vec2(0.0, offset));
                    
                    // Add diagonal samples for better spread
                    vec4 sampleUL = texture2D(tDiffuse, uv + vec2(-offset, -offset) * 0.707);
                    vec4 sampleUR = texture2D(tDiffuse, uv + vec2(offset, -offset) * 0.707);
                    vec4 sampleDL = texture2D(tDiffuse, uv + vec2(-offset, offset) * 0.707);
                    vec4 sampleDR = texture2D(tDiffuse, uv + vec2(offset, offset) * 0.707);
                    
                    glowFactor += weight;
                    glow += (sampleL + sampleR + sampleU + sampleD + 
                            sampleUL + sampleUR + sampleDL + sampleDR) * weight * 0.5;
                }
                
                // Enhance the glow intensity
                glow *= centerColor / max(0.001, brightness);
                glow *= glowStrength * smoothstep(glowThreshold, 1.0, brightness);
            }

            // Enhance the final color mix
            finalColor = mix(centerColor, centerColor + glow, 0.7);
            finalColor += glow * bloomStrength; // Add additional bloom

            // Apply scanlines and flicker
            scanline = sin(uv.y * scanlineCount + time * 10.0) * 0.5 + 0.5;
            scanline = 1.0 - (scanlineIntensity * scanline);
            flicker = 1.0 + sin(time * 100.0) * flickerAmount;

            // Apply grid lines - new calculation
            float gridX = abs(sin(uv.x * resolution.x / gridScale));
            float gridY = abs(sin(uv.y * resolution.y / gridScale));
            
            // Make grid lines more pronounced
            gridX = smoothstep(0.95, 1.0, gridX);
            gridY = smoothstep(0.95, 1.0, gridY);
            float grid = max(gridX, gridY) * gridIntensity;

            // Apply grid as a multiplicative dark mask
            finalColor.rgb *= (1.0 - grid);

            // Adjust final color for CRT look
            finalColor.rgb = mix(backgroundColor, finalColor.rgb, 0.9); // Reduce mix to maintain grey tint
            finalColor.rgb += backgroundColor * 0.15; // Increased ambient grey

            // Apply vignette and border
            float vignette = getVignette(uv);
            finalColor.rgb *= vignette * border;
            
            // Add subtle bloom near edges
            float edgeGlow = (1.0 - border) * 0.5;
            finalColor.rgb += vec3(0.1, 0.1, 0.1) * edgeGlow;

            gl_FragColor = finalColor * scanline * flicker;
        }
    `
};

const pixelateVertexShader = `
varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
`;

const pixelateFragmentShader = `
    uniform sampler2D tDiffuse;
    uniform float pixelSize;
    uniform vec2 resolution;
    varying vec2 vUv;

    void main() {
        vec2 dxy = pixelSize / resolution;
        vec2 coord = dxy * floor(vUv / dxy);
        gl_FragColor = texture2D(tDiffuse, coord);
    }
`;

// D20 Module
const D20 = {
    d20: null,
    innerD20: null,
    labelGroup: null,
    labels: [],
    faceNumbers: Config.faceNumbers,
    init: function (scene) {
        const geometry = new THREE.IcosahedronGeometry(Config.d20Radius, 0);
        const innerGeometry = new THREE.IcosahedronGeometry(Config.d20Radius - 0.1, 0);
        geometry.computeVertexNormals();

        const innerMaterial = new THREE.MeshBasicMaterial({
            color: 0x222222,
            side: THREE.FrontSide
        });
        D20.innerD20 = new THREE.Mesh(innerGeometry, innerMaterial);

        const material = new THREE.LineMaterial({
            color: 0xffffff,
            linewidth: Config.lineWidth,
            resolution: new THREE.Vector2(window.innerWidth, window.innerHeight)
        });

        const edges = new THREE.EdgesGeometry(geometry);
        const lineGeometry = new THREE.LineSegmentsGeometry().setPositions(edges.attributes.position.array);
        D20.d20 = new THREE.LineSegments2(lineGeometry, material);

        D20.labelGroup = new THREE.Group();

        const positionAttribute = geometry.attributes.position;

        for (let i = 0; i < positionAttribute.count; i += 3) {
            const a = new THREE.Vector3();
            const b = new THREE.Vector3();
            const c = new THREE.Vector3();

            a.fromBufferAttribute(positionAttribute, i);
            b.fromBufferAttribute(positionAttribute, i + 1);
            c.fromBufferAttribute(positionAttribute, i + 2);

            const center = new THREE.Vector3()
                .add(a)
                .add(b)
                .add(c)
                .divideScalar(3);

            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = Config.labelCanvasSize;
            canvas.height = Config.labelCanvasSize;

            context.fillStyle = '#1a1a1a';
            context.fillRect(0, 0, canvas.width, canvas.height);

            context.font = Config.labelFont;
            context.textAlign = 'center';
            context.textBaseline = 'middle';
            context.fillStyle = Config.labelTextColor;
            context.fillText(D20.faceNumbers[i / 3].toString(), Config.labelCanvasSize / 2, Config.labelCanvasSize / 2 + 1);

            const texture = new THREE.CanvasTexture(canvas);
            texture.magFilter = THREE.NearestFilter;
            texture.minFilter = THREE.NearestFilter;

            const spriteMaterial = new THREE.SpriteMaterial({
                map: texture,
                sizeAttenuation: false,
                depthTest: true,
                depthWrite: false
            });

            const sprite = new THREE.Sprite(spriteMaterial);
            sprite.scale.set(Config.labelScale, Config.labelScale, 1);

            const labelParent = new THREE.Object3D();
            labelParent.position.copy(center.multiplyScalar(1.1));
            labelParent.add(sprite);

            D20.labels.push(labelParent);
            D20.labelGroup.add(labelParent);
        }

        scene.add(D20.d20);
        scene.add(D20.innerD20);
        scene.add(D20.labelGroup);
    }
};

// Rendering Module
const RendererModule = {
    renderer: null,
    d20RenderTarget: null,
    d20Composer: null,
    d20Scene: null,
    labelScene: null,
    camera: null,
    pixelateShader: null,
    crtPass: null, // Add CRT pass
    init: function () {
        const scene = new THREE.Scene();
        const aspect = window.innerWidth / window.innerHeight;
        const d = 100;
        RendererModule.camera = new THREE.OrthographicCamera(-d *aspect, d* aspect, d, -d, 1, 1000);
        RendererModule.camera.position.set(d, d, d);
        RendererModule.camera.lookAt(scene.position);

        RendererModule.renderer = new THREE.WebGLRenderer({
            canvas: document.querySelector('#bg'),
            depth: true,
            logarithmicDepthBuffer: true
        });

        RendererModule.renderer.setPixelRatio(window.devicePixelRatio);
        RendererModule.renderer.setSize(window.innerWidth, window.innerHeight);

        RendererModule.d20RenderTarget = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight);

        RendererModule.d20Scene = new THREE.Scene();
        RendererModule.labelScene = new THREE.Scene();
        RendererModule.labelScene.background = null;
        const ambientLight = new THREE.AmbientLight(0xffffff);
        RendererModule.labelScene.add(ambientLight);

        RendererModule.d20Scene.background = new THREE.Color(Config.backgroundColor);
        RendererModule.labelScene.background = null;

        RendererModule.pixelateShader = {
            uniforms: {
                tDiffuse: { value: null },
                pixelSize: { value: Config.pixelSize },
                resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
                pixelHeightRatio: { value: Config.pixelHeightRatio }
            },
            vertexShader: pixelateVertexShader,
            fragmentShader: `
              uniform sampler2D tDiffuse;
              uniform float pixelSize;
              uniform vec2 resolution;
              uniform float pixelHeightRatio;
              varying vec2 vUv;
        
              void main() {
                  vec2 uv = vUv;
                  float dx = (pixelSize / pixelHeightRatio) / resolution.x;
                  float dy = pixelSize / resolution.y;
                  vec2 coord = vec2(dx * floor(uv.x / dx), dy * floor(uv.y / dy));
                  gl_FragColor = texture2D(tDiffuse, coord) * vec4(0.3, 1.0, 0.3, 1.0);
              }
            `
        };

        // Setup render passes in correct order
        const renderPass = new THREE.RenderPass(RendererModule.d20Scene, RendererModule.camera);
        const pixelatePass = new THREE.ShaderPass(RendererModule.pixelateShader);
        const crtPass = new THREE.ShaderPass(CRTShader);
        const finalPass = new THREE.ShaderPass(THREE.CopyShader);
        finalPass.renderToScreen = true;

        // Configure CRT pass
        crtPass.uniforms['resolution'].value = new THREE.Vector2(window.innerWidth, window.innerHeight);
        crtPass.uniforms['scanlineIntensity'].value = 0.075;
        crtPass.uniforms['scanlineCount'].value = 800.0;
        crtPass.uniforms['flickerAmount'].value = 0.05;
        crtPass.uniforms['glowStrength'].value = 1.0;
        crtPass.uniforms['glowSpread'].value = 0.0015;

        // Setup composer with passes in order
        RendererModule.d20Composer = new THREE.EffectComposer(RendererModule.renderer);
        RendererModule.d20Composer.addPass(renderPass);
        RendererModule.d20Composer.addPass(pixelatePass);
        RendererModule.d20Composer.addPass(crtPass);
        RendererModule.d20Composer.addPass(finalPass);

        RendererModule.crtPass = crtPass;

        return { scene: scene, camera: RendererModule.camera, renderer: RendererModule.renderer };
    },
    render: function () {
        RendererModule.renderer.setRenderTarget(null);
        RendererModule.renderer.clear();

        // Update CRT shader time
        RendererModule.crtPass.uniforms['time'].value = performance.now() / 1000;

        RendererModule.d20Composer.render();

        RendererModule.renderer.autoClear = false;
        RendererModule.renderer.clearDepth();

        RendererModule.renderer.render(RendererModule.labelScene, RendererModule.camera);

        RendererModule.renderer.autoClear = true;
    },
    updateSize: function () {
        const aspect = window.innerWidth / window.innerHeight;
        RendererModule.camera.left = -100 * aspect;
        RendererModule.camera.right = 100 * aspect;
        RendererModule.camera.top = 100;
        RendererModule.camera.bottom = -100;
        RendererModule.camera.updateProjectionMatrix();
        RendererModule.renderer.setSize(window.innerWidth, window.innerHeight);
        RendererModule.pixelateShader.uniforms.resolution.value.set(window.innerWidth, window.innerHeight);
        D20.d20.material.resolution.set(window.innerWidth, window.innerHeight);
        RendererModule.d20Composer.setSize(window.innerWidth, window.innerHeight);
        RendererModule.d20RenderTarget.setSize(window.innerWidth, window.innerHeight);

        // Update CRT resolution
        RendererModule.crtPass.uniforms['resolution'].value.set(window.innerWidth, window.innerHeight);
    },
    addObjects: function (d20, innerD20, labelGroup) {
        RendererModule.d20Scene.add(d20);
        RendererModule.d20Scene.add(innerD20);
        RendererModule.labelScene.add(labelGroup);
    }
};

// Label Module
const LabelModule = {
    updateLabelVisibility: function (labels, camera) {
        const cameraPosition = new THREE.Vector3();
        camera.getWorldPosition(cameraPosition);

        for (const label of labels) {
            const labelPosition = new THREE.Vector3();
            label.getWorldPosition(labelPosition);

            const directionToCamera = cameraPosition.clone().sub(labelPosition).normalize();

            const normal = labelPosition.clone().normalize();

            label.children[0].visible = normal.dot(directionToCamera) > 0;
        }
    },
    quantizePosition: function (position, gridSize = 3) {
        return new THREE.Vector3(
            Math.round(position.x / gridSize) * gridSize,
            Math.round(position.y / gridSize) * gridSize,
            Math.round(position.z / gridSize) * gridSize
        );
    },
    currentFlashedSprite: null,
    originalColor: null,

    flashNumber: function (faceNumber, labels) {
        const faceIndex = Config.faceNumbers.indexOf(faceNumber);

        if (faceIndex >= 0 && faceIndex < labels.length) {
            const sprite = labels[faceIndex].children[0];

            if (sprite) {
                // Reset previous flash if exists
                if (LabelModule.currentFlashedSprite && LabelModule.originalColor) {
                    LabelModule.currentFlashedSprite.material.color.copy(LabelModule.originalColor);
                }

                // Store current sprite and its color
                LabelModule.currentFlashedSprite = sprite;
                LabelModule.originalColor = sprite.material.color.clone();
                
                // Apply flash color
                sprite.material.color.setHex(Config.flashColor);
            }
        }
    },

    resetFlash: function() {
        if (LabelModule.currentFlashedSprite && LabelModule.originalColor) {
            LabelModule.currentFlashedSprite.material.color.copy(LabelModule.originalColor);
            LabelModule.currentFlashedSprite = null;
            LabelModule.originalColor = null;
        }
    },

    getFaceFacingCamera: function (labels, camera) {
        const cameraPosition = new THREE.Vector3();
        camera.getWorldPosition(cameraPosition);

        let maxDot = -1;
        let facingFaceNumber = 1;

        for (let i = 0; i < labels.length; i++) {
            const label = labels[i];
            const labelPosition = new THREE.Vector3();
            label.getWorldPosition(labelPosition);

            const directionToCamera = cameraPosition.clone().sub(labelPosition).normalize();
            const normal = labelPosition.clone().normalize();
            const dot = normal.dot(directionToCamera);

            if (dot > maxDot) {
                maxDot = dot;
                facingFaceNumber = Config.faceNumbers[i];
            }
        }

        return facingFaceNumber;
    }
};

// Animation Module
const Animation = {
    isRolling: false,
    rollStartTime: 0,
    stopStartTime: 0,
    angularVelocityX: 0,
    angularVelocityY: 0,
    angularVelocityZ: 0,
    currentScale: 0,
    verticalSpeed: 0,
    rollD20: function (d20) {
        Animation.isRolling = true;
        Animation.rollStartTime = performance.now();

        // Reset the previous flash when starting new roll
        LabelModule.resetFlash();

        d20.rotation.set(
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2
        );
        D20.innerD20.rotation.copy(d20.rotation);
        D20.labelGroup.rotation.copy(d20.rotation);

        Animation.angularVelocityX = (Math.random() * 2 - 1) * Config.initialAngularVelocity;
        Animation.angularVelocityY = (Math.random() * 2 - 1) * Config.initialAngularVelocity;
        Animation.angularVelocityZ = (Math.random() * 2 - 1) * Config.initialAngularVelocity;

        Animation.currentScale = 0;
        Animation.verticalSpeed = Config.bounceSpeed;
    },
    animate: function (d20, labels, camera) {
        const currentTime = performance.now();
        const elapsedTime = currentTime - Animation.rollStartTime;

        if (Animation.isRolling) {
            const t = elapsedTime / Config.rollDuration;
            if (t < 1) {
                d20.rotation.x += Animation.angularVelocityX * (1 - t);
                d20.rotation.y += Animation.angularVelocityY * (1 - t);
                d20.rotation.z += Animation.angularVelocityZ * (1 - t);

                Animation.angularVelocityX *= Config.angularVelocityDamping;
                Animation.angularVelocityY *= Config.angularVelocityDamping;
                Animation.angularVelocityZ *= Config.angularVelocityDamping;

                Animation.verticalSpeed -= Config.gravity;
                Animation.currentScale += Animation.verticalSpeed;

                if (Animation.currentScale < Config.groundLevel) {
                    Animation.currentScale = Config.groundLevel;
                    Animation.verticalSpeed *= Config.bounceDamping;
                }

                d20.scale.set(Config.initialScale - Animation.currentScale, Config.initialScale - Animation.currentScale, Config.initialScale - Animation.currentScale);
                D20.innerD20.scale.copy(d20.scale);
                D20.labelGroup.scale.copy(d20.scale);

            } else {
                Animation.isRolling = false;
                Animation.stopStartTime = performance.now();
                const faceNumber = LabelModule.getFaceFacingCamera(labels, camera);
                LabelModule.flashNumber(faceNumber, labels);
            }
        } else {
            const stopElapsedTime = currentTime - Animation.stopStartTime;
            if (stopElapsedTime > Config.stopDuration) {
                d20.rotation.x += 0.01;
                d20.rotation.y += 0.005;
                d20.rotation.z += 0.007;
            }
        }

        D20.innerD20.rotation.copy(d20.rotation);

        D20.labelGroup.rotation.copy(d20.rotation);

        const matrix = new THREE.Matrix4();
        for (const label of labels) {
            const originalPos = new THREE.Vector3();
            label.getWorldPosition(originalPos);

            const quantizedPos = LabelModule.quantizePosition(originalPos);

            matrix.copy(label.matrixWorld).invert();
            quantizedPos.applyMatrix4(matrix);
            label.children[0].position.copy(quantizedPos);
        }

        LabelModule.updateLabelVisibility(labels, camera);
    }
};

// Event Handler Module
const EventHandler = {
    init: function (renderer) {
        renderer.domElement.addEventListener('click', () => {
            if (!Animation.isRolling) {
                Animation.rollD20(D20.d20);
            }
        });

        window.addEventListener('resize', () => {
            RendererModule.updateSize();
        });
    }
};

// Initialization
function init() {
    const { scene, camera, renderer } = RendererModule.init();
    D20.init(scene);
    RendererModule.addObjects(D20.d20, D20.innerD20, D20.labelGroup);

    for (const label of D20.labels) {
        const sprite = label.children[0];
        sprite.material.depthTest = true;
        sprite.material.depthWrite = false;
        sprite.renderOrder = 1;
    }

    EventHandler.init(renderer);

    // Start rolling immediately
    setTimeout(() => Animation.rollD20(D20.d20), 100);

    function animate() {
        requestAnimationFrame(animate);
        Animation.animate(D20.d20, D20.labels, camera);
        RendererModule.render();
    }

    animate();
}

init();
```

### PIXEL ART BLOCK TEXTURE GENERATOR

> (pug)

```html
.pixel-wrapper

- for (var x = 0; x < 256; x++)
    .pixel
```

> (scss)

```scss
$s: 20px;

body {
  padding: 0;
  margin: 0;
  height: 100vh;
  width: 100%;
  background: #9E9E9E;
  display: flex;
}
  
.pixel-wrapper {
  width: $s*16;
  height: $s*16;
  margin: auto;
}

.pixel {
  width: $s;
  height: $s;
  display: block;
  float: left;
}

$hue: random(360);
@for $i from 1 to 257 {
  .pixel:nth-child(#{$i}) {
    background-color: hsla($hue, 85, random(100), random(100));
  }
}
```

## PIXEL ART NIGHT TIME TRANSITION SCENE (REQUIRES COLOR TWEAKING TO NORMALIZE WITH OUR AESTHETIC)

```html
<canvas id="canvas" width="100" height="100"></canvas>
```

```css
body {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
}

# canvas {
  width: 100vmin;
  height: 100vmin;
  vertical-align: middle;
  image-rendering: pixelated;
  cursor: pointer;
}

const { min, max, round, floor, abs, sqrt } = Math
const random = (x = 1) => Math.random() * x
const rgb = (...values) => `rgb(${values.join(',')})`
const rgba = (...values) => `rgba(${values.join(',')})`
const distance = (x1, y1, x2, y2) => sqrt(
  abs(x1 - x2)**2 +
  abs(y1 - y2)**2
)

const Sky = (() => {
  const State = {
    pos: [0, 0],
    stars: [],
    moonPos: []
  }

  const speed = 0.05

  function updatePosition() {
    State.pos[0] -= speed
    State.pos[1] += speed
  }

  function reset() {
    State.pos = [0, 0]
    State.stars = []
    State.moonPos = []
  }

  function spaceColor(size) {
    const moonAltitude = size / 2 - State.pos[1] + moonSize
    return rgb(
      min(max(0, moonAltitude), 12.5),
      min(max(5, moonAltitude), 20),
      min(max(10, moonAltitude), 25)
    )
  }

  function drawSpace(ctx, size) {
    ctx.fillStyle = spaceColor(size)
    ctx.fillRect(0, 0, size, size / 2)
    let px = size *-1
    while (px++ < size* size) {
      let pxX = px % (size *2)
      let pxY = floor(px / (size* 2))
      const moonX = State.moonPos[0] + moonSize / 2 - 1
      const moonY = State.moonPos[1] + moonSize / 2
      const moonDistance = distance(moonX, moonY, pxX, pxY)
      if (moonDistance < moonSize * 1.75) {
        ctx.fillStyle = rgba(255, 255, 255, .05)
        ctx.fillRect(
          State.pos[0] + pxX,
          State.pos[1] + pxY,
          1,
          1
        )
      }
      if (moonDistance < moonSize) {
        ctx.fillStyle = rgba(255, 255, 255, .1)
        ctx.fillRect(
          State.pos[0] + pxX,
          State.pos[1] + pxY,
          1,
          1
        )
      }
    }
  }

  const starCount = () => 1000 + round(random(2000))
  const starColor = () => rgba(
    255,
    200 + round(random(55)),
    200 + round(random(20)),
    random()
  )

  function generateStars(size) {
    if (State.stars.length) {
      return
    }
    let count = starCount()
    while (count-- > 0) {
      State.stars.push([
        round(random(size *8)),
        round(random(size* 8)) * -1 + size
      ])
    }
  }

  function drawStars(ctx, size) {
    let star = State.stars.length
    while (star-- > 0) {
      ctx.fillStyle = starColor()
      ctx.fillRect(
        State.stars[star][0] + State.pos[0],
        State.stars[star][1] + State.pos[1],
        1,
        1
      )
    }
  }

  const moonSize = 10
  const moonColors = {
    0: 'transparent',
    1: rgb(210, 210, 210),
    2: rgb(255, 255, 255),
    3: rgb(120, 120, 120),
  }

  const moonBitmap = [
    0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 2, 1, 1, 1, 1, 0, 0,
    0, 1, 1, 1, 1, 3, 3, 3, 1, 0,
    0, 1, 3, 3, 1, 1, 3, 3, 1, 0,
    1, 3, 3, 3, 3, 2, 1, 3, 1, 1,
    1, 1, 3, 3, 3, 1, 1, 1, 1, 1,
    0, 1, 1, 3, 1, 2, 1, 1, 1, 0,
    0, 1, 1, 1, 2, 2, 2, 1, 1, 0,
    0, 0, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 0, 1, 1, 0, 0, 0, 0
  ]

  function placeMoon(size) {
    if (State.moonPos.length) {
      return
    }
    State.moonPos[0] = size / 3 + round(random(size / 2))
    State.moonPos[1] = moonSize + round(random(size / 10))
  }

  function drawMoon(ctx, size) {
    let bit = 0
    while (bit++ < moonBitmap.length - 1) {
      const bitPos = [
        State.moonPos[0] + State.pos[0] + bit % moonSize,
        State.moonPos[1] + State.pos[1] + floor(bit / moonSize)
      ]
      ctx.fillStyle = moonColors[moonBitmap[bit]]
      ctx.fillRect(bitPos[0], bitPos[1], 1, 1)
    }
  }

  return Object.freeze({
    draw(ctx, size) {
      generateStars(size)
      placeMoon(size)
      drawSpace(ctx, size)
      drawStars(ctx, size)
      drawMoon(ctx, size)
      updatePosition()
      return {
        x: State.pos[0],
        y: State.pos[1],
        moonPos: {
          x: State.pos[0] + State.moonPos[0] + moonSize / 2 - 1,
          y: State.pos[1] + State.moonPos[1] + moonSize / 2
        },
        moonSize
      }
    },
    reset
  })
})()

const Sea = (() => {
  function seaColor(size, moonAlt) {
    const alt = size / 2 - moonAlt
    const minGreen = 10 + round(random(10))
    const maxGreen = 10 + round(random(25))
    const minBlue = 20 + round(random(50))
    const maxBlue = 50 + round(random() > .9 ? random(120) : random(50))
    return rgb(
      0,
      max(maxGreen + min(alt *3, 0), minGreen),
      max(maxBlue + min(alt* 3, 0), minBlue)
    )
  }

  return Object.freeze({
    draw(ctx, size, { x: skyX, y: skyY, moonPos, moonSize, stars }) {
      let x = 0
      let y = 50
      while (x *y < size* size) {
        const xSize = round(random(5))
        ctx.fillStyle = seaColor(size, skyY + moonSize)
        ctx.fillRect(x, y, xSize, 1)
        const verticalShine = min(
          1.25,
          size / 2 - moonPos.y + moonSize / 2
        )
        if (moonPos.x + moonSize >= x && moonPos.x - moonSize <= x) {
          ctx.fillStyle = rgba(
            255,
            255,
            255,
            verticalShine / 10
          )
          ctx.fillRect(x, y, xSize, 1)
        }

        const verticalNarrowShine = min(
          0.75,
          size / 2 - moonPos.y + moonSize / 2
        )
        if (moonPos.x + moonSize / 2 >= x && moonPos.x - moonSize / 2 <= x) {
          ctx.fillStyle = rgba(
            255,
            255,
            255,
            verticalNarrowShine / 10
          )
          ctx.fillRect(x, y, xSize, 1)
        }

        const circularShine = min(
          2.5,
          size / 2 - moonPos.y + moonSize
        )
        const moonDistance = distance(
          moonPos.x,
          moonPos.y,
          x, y
        )
        if (moonDistance < moonSize * 2) {
          ctx.fillStyle = rgba(
            255,
            255,
            255,
            circularShine / 10
          )
          ctx.fillRect(x, y, xSize, 1)
        }

        x += xSize
        if (x >= size) {
          x = 0
          y++
        }
      }
    }
  })
})()

function draw() {
  ctx.clearRect(0, 0, size, size)
  const skyState = Sky.draw(ctx, size)
  Sea.draw(ctx, size, skyState)
  requestAnimationFrame(draw)
}

function reset() {
  Sky.reset()
}

canvas.addEventListener('click', reset)
const ctx = canvas.getContext('2d')
const size = canvas.width
draw()
```

## PIXEL ART METHODS

```html
%img.m{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/pixelTest.png'}>
.floor
.overlay

.options
    .options_sf
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/sfIcon.png'}>
    .options_bg
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/bgIcon.png'}>
.name_modal
    .pixelsTop
    .pixelsBottom
    .intro_modal__header
        %p Welcome
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/featuredHeader.png'}>
    %h3 Enter your name, developer
    %hr

    %input{:type => 'text', :placeholder => 'Your Name'}
    .next
        .pixelsTop
        .pixelsBottom
        Next
    
.intro_modal
    .pixelsTop
    .pixelsBottom
    .intro_modal__header
        %p Welcome
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/featuredHeader.png'}>
    %h3 Welcome to codepen simulator
    %hr

    %p.text Your aim is to see how many followers you can get in 1 year!

    %p.text Create pens by simply typing randomly. The pen will gain stats in html, css, js and design based on your skill level. Use your followers to unlock research which improves your skills!

    %p.text If good enough, your pen will be featured and that will boost your views.
    .go
        .pixelsTop
        .pixelsBottom
        Let's go
.endGame
    .pixelsTop
    .pixelsBottom
    .endGame__header
        %p Finished
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/featuredHeader.png'}>
    %h3 Congratulations! You've done 1 year on Codepen!
    %hr
    %h2 You managed to get
    %h1 100000
    %p Followers
    %p
        You released
        %span.pencount 1
        pen(s)
    %p
        Your most viewed pen was
        %span.mostName x
        which had
        %span.mostViews x
        views!
    %a{:href => '<http://www.codepen.io/jcoulterdesign>', :target => '_blank'}
        .restart
            .pixelsTop
            .pixelsBottom
            See more cool stuff
    .share
        .pixelsTop
        .pixelsBottom
        Share on twitter
.researchProgress
    %h2 Researching...
    .bar
        .bar_inner
    .pixelsTop
    .pixelsBottom
.featured_modal
    .pixelsTop
    .pixelsBottom
    .featured_modal__header
        %p Featured
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/featuredHeader.png'}>
    %h3 Your pen has been picked!
    %hr
    .featured_modal__image
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/cPreview.png'}>
    .featured_modal__text
        %p
            your pen '
            %span.name example pen
            '
        %p has been picked by
        %p.picker
        %p that should help boost your views!
    .awesome
        .pixelsTop
        .pixelsBottom
        awesome
.research_modal
    .research_modal__header
        %p research
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/researchHeader.png'}>
    %h3.hide Improve your skills
    %hr.hide
    .close.hide
        .pixelsTop
        .pixelsBottom
        x
    .pixelsTop
    .pixelsBottom
    .research_modal__list.hide
.complete_modal
    .pixelsTop
    .pixelsBottom
    .complete_modal__header
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/penCompleteHeader.png'}>
        %p pen complete
    %div.hide
        %img
        %h2 You completed a pen!
        %hr
        %h3 lets see how you did
    .complete_modal__stats.hide
        .html
            %h4 html
            %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gHtml.png'}>
            %span
                .swatch.html
                %span 103
        .css
            %h4 css
            %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gCSS.png'}>
            %span
                .swatch.css
                %span 103
        .js
            %h4 js
            %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gJS.png'}>
            %span
                .swatch.js
                %span 103
        .design
            %h4 Design
            %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gDesign.png'}>
            %span
                .swatch.design
                %span 103
    .scrap.hide
        .pixelsTop
        .pixelsBottom
        scrap pen
        %img.icon{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/scrapCross.png'}>
    .release.hide
        .pixelsTop
        .pixelsBottom
        release pen
        %img.icon{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/releaseArrow.png'}>
.pen
    .pixelsTop
    .pixelsBottom
    %h2 progress:
    .date
        %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gCalendar.png'}>
        %span

    .followers
        %img{:src => 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/followersIcon.png'}
        .pixelsTop
        .pixelsBottom
        FOLLOWERS:
        %span 0
    .pen_bar
        .pen_bar_progress
    .pen_html
        .pixelsTop
        .pixelsBottom
        .swatch
        %span HTML
        .sep
        %span.val 0
    .pen_css
        .pixelsTop
        .pixelsBottom
        .swatch
        %span CSS
        .sep
        %span.val 0
    .pen_js
        .pixelsTop
        .pixelsBottom
        .swatch
        %span JS
        .sep
        %span.val 0
    .pen_design
        .pixelsTop
        .pixelsBottom
        .swatch
        %span DESIGN
        .sep
        %span.val 0

.releasedHeader
    .pixelsTop
    .pixelsBottom
    %img.icon{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/codepenIcon.png'}>
    Released Pens
    %img.arrow{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/downArrow.png'}>
.releasedEmpty
    .pixelsTop
    .pixelsBottom
    %h2 You haven't released any pens yet
.released

.username
    .pixelsTop
    .pixelsBottom
    %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/userIcon.png'}>
    %h2 Developer
.mystats
    %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/skilsIcon.png'}>
    .pixelsTop
    .pixelsBottom
    %h2 skills
    .mystats_html
        .swatch
        HTML:
        %span lv
        %span.val 0
    .mystats_css
        .swatch
        CSS:
        %span lv
        %span.val 0
    .mystats_js
        .swatch
        JAVASCRIPT:
        %span lv
        %span.val 0
    .mystats_design
        .swatch
        DESIGN:
        %span lv
        %span.val 0
.research
.researchButton
    .pixelsTop
    .pixelsBottom
    .researchButton_counter
        %span 0
        .pixelsTop
        .pixelsBottom
    Research
    %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/buttonArrow.png'}>
.achievementsButton
    .pixelsTop
    .pixelsBottom
    Achievments
    %img{:src => '<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/buttonArrow.png'}>
%a{:href => '<http://www.codepen.io/jcoulterdesign>', :target => '_blank'}
    .followButton
        .pixelsTop
        .pixelsBottom
        Follow me on codepen
.startMashing
    .auto.off

        auto
        %img.cross{:src => 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/autoCross.png'}
        %img.tick{:src => 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/autoTick.png'}
        .pixelsTop
        .pixelsBottom
    .pixelsTop
    .pixelsBottom
    %h2 
        %span Start pressing keys
        %img{:src => 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gKey.png'}
%canvas.grain

@font-face {
    font-family: pixles;
    src: url(<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/04B_03__.TTF>);
}

// boxes
// Each elemenmt that has the pixel outline, needs the 2 divs inside called pixelsTop and pixlesBottom

$pixelWidth : 3px;
$pixelWidthAlt : -3px;
$pixelBorderColor : #b6a695;
$pixelHighlightColor : #e7e7e7;
$pixelShadowColor : rgba(0 , 0, 0, 0.1);

%pixelsTop {
    display: block;
    content: '';
    position: absolute;
    width: $pixelWidth;
    height: $pixelWidth;
    top: 0;
}

%pixelsBottom {
    display: block;
    content: '';
    position: absolute;
    width: $pixelWidth;
    height: $pixelWidth;
    top: 0;
}

@mixin make_box($bg, $borderColor, $highlightColor, $shadowColor) {
    background: $bg;
    box-shadow: 0px $pixelWidth $highlightColor, 0px $pixelWidthAlt $bg, $pixelWidth 0px $bg, $pixelWidthAlt 0px $bg, 0px $pixelWidthAlt *2 $borderColor, 0px $pixelWidth* 2 $borderColor, $pixelWidth *2 0px $borderColor, $pixelWidthAlt* 2 0px $borderColor, $pixelWidth *3 0px $shadowColor, 0px $pixelWidth* 3 $shadowColor;
    position: relative;
    padding: 12px;

    & .pixelsBottom {
        width: calc(100% + #{$pixelWidth * 4});
        position: absolute;
        left: -$pixelWidth * 2;
        bottom: 0;

        &::after {
            @extend %pixelsTop;

            right: $pixelWidth;
            top: -$pixelWidth;
            background: $highlightColor;
            box-shadow: 0px $pixelWidth $borderColor, 0px $pixelWidth * 2 $shadowColor, $pixelWidth $pixelWidth $shadowColor;
        }

        &::before {
            @extend %pixelsBottom;

            left: $pixelWidth;
            top: -$pixelWidth;
            background: $highlightColor;
            box-shadow: 0px $pixelWidth $borderColor, 0px $pixelWidth * 2 $shadowColor, $pixelWidthAlt $pixelWidth $shadowColor;
        }
    }

    & .pixelsTop {
        width: calc(100% + #{$pixelWidth * 4});
        position: absolute;
        left: -$pixelWidth * 2;
        top: -$pixelWidth;

        &::after {
            @extend %pixelsTop;

            right: $pixelWidth;
            background: $borderColor;
        }

        &::before {
            @extend %pixelsTop;

            left: 3px;
            background: $borderColor;  
        }
    }
}

%box {
    @include make_box(white, $pixelBorderColor, $pixelHighlightColor, $pixelShadowColor);
}

%box-orange {
    @include make_box(#fcab0b, #e8861c, #fdbc3d, $pixelShadowColor);
}

%box-green {
    @include make_box(#a5da60, #89b74c, #c4ed8e, $pixelShadowColor);
}

%box-red {
    @include make_box(#df644c, #ba513d, #ea7f6a, $pixelShadowColor);
}

%box-grey {
    @include make_box(#d1d1d1, #c4c4c4, #e0e0e0, $pixelShadowColor);
}

%box-purple {
    @include make_box(#c557e1, #a848c0, #d77ded, $pixelShadowColor);
}

%box-blue {
    @include make_box(#1e4b56, #16414c, #315962, $pixelShadowColor);
}

%box-twitter {
    @include make_box(#55c6e2,#439db3, #94e5f9, $pixelShadowColor);
}

%button {
    position: relative;
    // overflow: hidden;
    &:active {

        transform: translateY(2px)
    }

    &::after {
        content: '';
        display: block;
        width: 30px;
        -webkit-filter: blur(24px);
        height: 30px;
        background: rgba(255, 255, 255, 0.3);
        position: absolute;
        height: 50px;
        -webkit-transform: rotate(-30deg);
        transform: rotate(-30deg) skewy(31deg);
        color: white;
        top: -5px;
        right: 100%;
        transition: all .4s;
    }

    &:hover {
        &::after {
            right: 0px;
        }
    }
}

.magic {
    position: fixed;
    left: 0;
    right: 0;
    margin: auto;

    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    width: 100%;
    height: 100%;
    background: black;
    display: none;
    img {
        width: 100%;
    }
}
// -----------------------------------------------------------------------------------------------------------------
.grain {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 4;
    pointer-events: none;
}
.swatch {
    box-shadow: inset 3px 0 rgba(0, 0, 0, 0.1), inset -3px 0 rgba(255, 255, 255, 0.3) !important;
    width: 12px !important;
    height: 11px;

    &.html {
        background: #f1753f;

    }


    &.css {

        background: #2965f1;

    }

    &.js {
        background: #f3e273;

    }


    &.design {
        background: #9d28e0;

    }
}

/*Let's get this party started*/
::-webkit-scrollbar {
    width: 3px;
}

/*Track*/
::-webkit-scrollbar-track {

    background: transparent;
}

/*Handle*/
::-webkit-scrollbar-thumb {
    background: #cabcae;

}

.auto {
    @extend %box;
    text-align: left;
    position: absolute;
    bottom: -12px;
    height: 6px;
    z-index: 2;
    line-height: 7px;
    left: 0;
    right: -480px;
    margin: auto;
    cursor: pointer;
    width: 80px;

    img {
        width: 15px;
        position: absolute;
        right: 6px;
        top: 7px;
    }

    &.off {
        .tick {
            display: none;
        }

        .cross {
            display: block;
        }
    }

    &.on {
        .tick {
            display: block;
        }

        .cross {
            display: none;
        }
    }
}
.startMashing {
    @extend %box;
    text-align: center;

    position: absolute;
    bottom: 40px;
    height: 160px;    z-index: 2;
    line-height: 160px;
    left: 0;
    right: 0;
    margin: auto;
    width: 500px;

    h2 {
        position: relative;
        top: -13px;
        img {
            width: 20px;
            position: absolute;
            left: 0;
            right: 0;
            margin: auto;
            top: 100px;
            animation: key .3s linear infinite;
        }

        @keyframes key {
            from{top: 100px;}
            to{top: 102px;}
        }
    }
}

.researchButton {
    @extend %box-green;
    width: 203px;
    color: #476323;
    @extend %button;

    float: left;
    clear: left;
    margin-top: 27px;
    cursor: pointer;
    &_counter {
        @extend %box-green;

        @extend %button;
        right: -20px;
        width: 30px;
        color: #476323;
        float: left;
        text-align: center;
        clear: left;
        margin-top: 27px;
        top: -55px;
        height: 30px;
        line-height: 31px;
        cursor: pointer;
        padding: 0px;
        position: absolute;
        z-index: 1;
    }
    img {
        width: 4px * 3;
        position: absolute;
        top: 18px;
        right: 18px;
    }
}

.username {
    @extend %box;
    float: left;
    padding: 8px 12px 0px 10px;
    position: relative;
    top: 30px;

    img {
        width: 15px * 3;
        position: absolute;
        left: -24px;
        top: -36px;

    }
}
.achievementsButton {
    @extend %button;
    @extend %box-purple;
    width: 203px;
    display: none;
    color: #75168d;

    float: left;
    clear: left;
    margin-top: 27px;
    cursor: pointer;

    img {
        width: 4px * 3;
        position: absolute;
        top: 18px;
        right: 18px;
    }
}
.followButton {
    @extend %button;
    @extend %box-blue;
    width: 203px;
    color: #75168d;

    float: left;
    clear: left;
    margin-top: 27px;
    cursor: pointer;

    color: #c4ebfd;
}

.date {
    float: right;
    position: absolute;
    right: 40px;
    top: 10px;

    img {
        width: 21px;
        position: relative;
        top: 2px;

    }
}

.floor {
    background: #e1dac5;
    position: fixed;
    bottom: 0;
    height: 36%;
    width: 100%;
    left: 0;
    z-index: -1;
    border-top: 30px solid white;
}

.options{
    position: absolute;
    right: 34px;
    top: 81px;

    &_bg {
        img {
            width: 21px;
        }
    }

    &_sf {
        img {
            width: 18px;
            margin-right:10px;
        }
    }

    div 
    { float: left;
        transition: all 1s;
        cursor: pointer;
    }
}
.overlay {
    //display: none;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    cursor: pointer;
    height: 100%;
    background: #675a4c;
    z-index: 3;
    opacity: 0.89;
    // display: none;
}

.researchProgress {
    @extend %box;

    position: absolute;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    width: 200px;
    transform: translateY(-50%);
    display: none;

    .bar {
        width: 100%;
        height: 6px;
        border-bottom: 3px solid #d6c9bc;
        position: relative;

        &_inner {
            width: 0%;
            height: 6px;
            position: absolute;
            left: 0;
            background: #fcab0b;
            box-shadow: 0px 3px inset #fdbc3d;

            &.animate {
                animation: bar 2s linear;
            }

            @keyframes bar {
                from {
                    width: 0%;
                }

                to {
                    width: 100%
                }

            }
        }
    }
}

.endGame {
    display: none;
    @extend %box;

    .mostName,
    .mostViews {
        font-weight: bold;
    }
    
    hr {
        border: none;
        width: 95%;
        border-top: 3px solid #efedea;
        margin-bottom: 30px;
        box-shadow: 0 3px rgba(0, 0, 0, 0.02);
        z-index: 2;
        position: relative;
    }
    h3 {
        text-align: center;
        font-weight: normal;
        font-size: 16px;
        margin: 15px 24px 23px 24px;
    }

    h1 {
    font-size: 41px;
    margin-bottom: 15px;
    color: #f8ab12;
    margin-top: 19px;
    }
    //display: none;
    text-align: center;
    width: 600px;
    height: 250px;
    position : absolute !important;
    z-index: 3;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    transform: translateY(-50%);
    padding: 40px;
    text-align: ceter;

    .restart {


        @extend %box-green;
        color: #476323;
        position: absolute;
        bottom: -26px;
        width: 170px;
        @extend %button;
        text-align: center;
        margin: auto;
        left: 220px;
        cursor: pointer;
        right: 0;
    }

    .share {


        @extend %box-twitter;

        @extend %button;
        color: #1c3940;
        position: absolute;
        bottom: -26px;
        width: 170px;
        text-align: center;
        margin: auto;
        left: -240px;
        cursor: pointer;
        right: 0;
    }
    &__header{
        position: absolute;
        left: 0;
        right: 0;
        margin: auto;
        width: 282px;
        top: -87px;

        p {
            position: absolute;
            width: 100%;
            text-align: center;
            top: 71px;
            color: #c4ebfd;
            left: 4px;
        }
        img {
            width: 94px * 3
        }
    }
}
.name_modal {
    @extend %box;

    //display: none;
    text-align: center;
    width: 600px;
    transition: all 0.5s;
    height: 250px;

    hr {
        border: none;
        width: 95%;
        border-top: 3px solid #efedea;
        margin-bottom: -1px;
        box-shadow: 0 3px rgba(0, 0, 0, 0.02);
        z-index: 2;
        position: relative;
    }
    h3 {
        text-align: center;
        font-weight: normal;
        font-size: 16px;
        margin: 15px 24px 23px 24px;
    }
    .text {
        margin: 20px 0;
    }
    position : absolute !important;
    z-index: 3;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    transform: translateY(-50%);
    padding: 40px;
    text-align: center;

    input {

        font-family: pixles;
        font-size: 16px;
        font-weight: normal;
        outline: none;
        text-align: center;
        padding: 19px;
        width: 360px;
        border-radius: 5px;
        color: #352c22;
        margin-top: 67px;
        border: 3px solid #f0eeeb;
    }

    .next {


        @extend %box-green;
        color: #476323;
        position: absolute;
        bottom: -26px;
        width: 140px;
        @extend %button;
        text-align: center;
        margin: auto;
        left: 0;
        cursor: pointer;
        right: 0;
    }
    &__header{
        position: absolute;
        left: 0;
        right: 0;
        margin: auto;
        width: 282px;
        top: -87px;

        p {
            position: absolute;
            width: 100%;
            text-align: center;
            top: 71px;
            color: #c4ebfd;
            left: 4px;
        }
        img {
            width: 94px * 3
        }
    }
}
.intro_modal {
    @extend %box;

    left: 200%;
    text-align: center;
    width: 600px;
    height: 250px;

    hr {
        border: none;
        width: 95%;
        border-top: 3px solid #efedea;
        margin-bottom: -1px;
        box-shadow: 0 3px rgba(0, 0, 0, 0.02);
        z-index: 2;
        position: relative;
    }
    h3 {
        text-align: center;
        font-weight: normal;
        font-size: 16px;
        margin: 15px 24px 23px 24px;
    }
    .text {
        margin: 20px 0;
    }
    position : absolute !important;
    z-index: 3;
    transition: all 0.5s;
    right: 0;
    margin: auto;
    top: 50%;
    transform: translateY(-50%);
    padding: 40px;
    text-align: center;

    .go {


        @extend %box-green;
        color: #476323;
        position: absolute;
        bottom: -26px;
        width: 140px;
        @extend %button;
        text-align: center;
        margin: auto;
        left: 0;
        cursor: pointer;
        right: 0;
    }
    &__header{
        position: absolute;
        left: 0;
        right: 0;
        margin: auto;
        width: 282px;
        top: -87px;

        p {
            position: absolute;
            width: 100%;
            text-align: center;
            top: 71px;
            color: #c4ebfd;
            left: 4px;
        }
        img {
            width: 94px * 3
        }
    }
}
.featured_modal {
    @extend %box;

    display: none;
    text-align: center;
    width: 600px;
    height: 250px;
    position : absolute !important;
    z-index: 3;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    transform: translateY(-50%);
    padding: 40px;
    text-align: left;
    h3 {
        text-align: center;
        font-weight: normal;
        font-size: 16px;
        margin: 24px;

    }

    hr {
        border: none;
        border-top: 3px solid #efedea;
        margin-bottom: 40px;
    }
    &__header{
        position: absolute;
        left: 0;
        right: 0;
        margin: auto;
        width: 282px;
        top: -87px;

        p {
            position: absolute;
            width: 100%;
            text-align: center;
            top: 71px;
            color: #c4ebfd;
            left: 4px;
        }
        img {
            width: 94px * 3
        }
    }
    .name {
        color: #29241f;
    }

    .picker {
        color: orange;
    }
    &__text {
        padding-top: 15px;
    }
    .awesome {
        @extend %box-green;
        color: #476323;
        position: absolute;
        bottom: -26px;
        width: 140px;
        @extend %button;
        text-align: center;
        margin: auto;
        left: 0;
        cursor: pointer;
        right: 0;
    }

    &__image {
        float: left;
        margin-right: 30px;
        img {
            width: 66px * 3;
        }
    }
}
.research_modal {
    @extend %box;

    .hide {
        display: none;
    }
    transition: all .7s;
    width: 300px;
    height: 40px;
    display: none;
    text-align: center;
    position : absolute !important;
    z-index: 3;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    transform: translateY(-50%);

    h3 {
        text-align: center;
        font-weight: normal;
        font-size: 16px;
        margin: 40px 24px 24px 24px;

    }

    hr {
        border: none;
        width: 95%;
        border-top: 3px solid #efedea;
        margin-bottom: -1px;
        box-shadow: 0 3px rgba(0, 0, 0, 0.02);
        z-index: 2;
        position: relative;
    }
    &__header{
        position: absolute;
        left: 0;
        right: 0;
        margin: auto;
        width: 282px;
        top: -87px;

        p {
            position: absolute;
            width: 100%;
            text-align: center;
            top: 67px;
            color: #c4ebfd;
            left: 1px;
        }
        img {
            width: 94px * 3
        }
    }
    .close {
        @extend %box-red;@extend %button;
        color: #892e1f;
        cursor: pointer;
        position: absolute;
        right: -22px;
        top: -22px;
        width: 10px;
        height: 10px;
        z-index: 3;
        line-height: 11px;
    }
    &::after {
        position: fixed;
        bottom: 15px;
        left: 0;
        width: 98%;
        height: 40px;
        display: block;
        background: -webkit-linear-gradient(top, rgba(255,255,255,0) 0%,rgba(255,255,255,1) 100%);
        content: '';
    }
    &__list {
        padding: 1px 20px 20px 20px;
        overflow-y: scroll;
        height: 288px;
        position: relative;

    }

    & .item {
        float: left;
        clear: left;
        border-top: 3px solid #f2f2f2;
        padding: 24px 0px 21px 0px;
        width: 95%;
        position: relative;
        left: 11px;

        &:first-child {
            border: none;
        }


        &.unavailable {

            .research_button {
                @extend %box-red;

                color: #782e1f;
            }
        }

        &.researched {

            &::after {
                display: block;
                position: absolute;
                right: -16px;
                top: 6px;
                content: url(https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/rTick.png);
            }
            .name,
            .stat{
                opacity: 0.45;     


            }

            .research_button {
                @extend %box-grey;

                color: #959595;

            }
        }
    }

    .sep {
        margin: 0 6px; 
    }

    .name {
        float: left;
    }

    .green {
        color: #89b74c;
    }

    .stat {
        float: left;

        img {
            width: 6px;
            margin-left: 4px;
        }

    }



    .research_button {
        @extend %button;
        @extend %box-green;

        right: 0px;

        color: #476323;

        float: right;
        cursor: pointer;
        top: -6px;

        padding: 4px !important;


        float: right;
        position: absolute !important;
        top: 18px;
        width: 150px;



        img {
            width: 5px * 2;
            position: relative;
            left:-4px
        }

        .cost {
            color: white;
        }
    }

}

.complete_modal {
    .swatch {
        position: relative;
        left: 49px;
        top: 3px;
    }
    @extend %box;
    display: none;
    opacity: 0;
    text-align: center;
    transition: all .7s;
    width: 300px;
    height: 40px;
    position : absolute !important;
    z-index: 3;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    transform: translateY(-50%);

    h4 {
        font-weight: normal;
        font-size: 16px;
    }
    div.hide {
        display: none;
    }
    &__header {

        position: absolute;
        left: 0;
        right: 0;
        margin: auto;
        width: 282px;
        top: -87px;

        p {
            position: absolute;
            width: 100%;
            text-align: center;
            top: 68px;
            color: #c4ebfd;
            left: 1px;

        }
        img {
            width: 94px * 3
        }
    }
    .scrap {
        @extend %button;
        @extend %box-red;

        position: absolute;
        bottom: 0;
        text-align: left;
        width: 240px;
        bottom: -25px;
        color: #782e1f;
        cursor: pointer;
        left: 30px;

        img{
            width: 15px;
            float: right;
            position: relative;
            top: 1px;
        }
    }
    hr {
        border: none;
        border-top: 3px solid #efedea;
        margin-bottom: 20px;
        margin-top: 22px;
        width: 60%;
    }

    h2 {
        margin: 20px 0 6px 0;
    }
    .release {
        @extend %button;
        @extend %box-green;
        cursor: pointer;color: #476323;
        position: absolute;
        bottom: 0;
        width: 240px;
        right:30px;
        bottom: -25px;

        img{
            width: 18px;
            float: right;
            position: relative;
            top: 6px;
        }

    }
    h3 {
        font-size: 16px;
        font-weight: normal;
        margin: 30px 0;
    }
    &__stats {

        .html {
            img {
                width: 48px;
                margin-top: -5px;
            }
        }

        .css {
            img {
                width: 48px;
                margin-top: -5px;
            }
        }

        .js {
            img {
                width: 48px;
                margin-top: -5px;
            }
        }

        .design {
            img {
                width: 36px;
                margin-top: -5px;
            }
        }
        div {
            float: left;
            text-align: center;
            width: 25%;
            box-shadow: inset -3px 0px #f1ebe4;
            &:last-child {
                box-shadow: none;
            }
            span {
                display: block;
                margin-top: 17px;
                position: relative;
                left: 4px;
            }
        }
    }
}

.make {
    @extend %box;
    position: absolute !important;
    left: 0;
    right: 0;
    width: 200px;
    margin: auto;
    bottom: 40px;
    border: none;
    cursor: pointer;
    outline: none;
}
body {
    background: url('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gBg.png>');
    color: #594c3d;
    margin: 50px;
    // height: 100vh;
    overflow: hidden;
}
img {
    image-rendering: auto;
    image-rendering: crisp-edges;
    image-rendering: pixelated;
}
img.m {
    position: absolute;
    left: 0;
    right: 0;
    margin: auto;
    top: 50%;
    left: -40px;
    transform: translateY(-50%);
    width: 252px * 3;
}

.followers {
    @extend %box-orange;

    color: #9b5c19;
    float: right;
    transform: translateX(calc(100% + -3px));
    right: 0;
    z-index:3;
    bottom: 12px;
    position: absolute !important;
    padding: 13px 50px !important;

    span {
        color: #fff;
    }

    img {
        width: 42px;
        left: -25px;
        top: -18px;
        z-index: 2;
        position: absolute;
    }
}

h2 {
    font-weight: normal;
    margin:0 0 6px 0;
    font-size: 16px;
}
body,
button {
    font-family: pixles;
    text-transform: uppercase;
    font-size: 16px;
    line-height: 20px;

    -webkit-user-select: none;  /* Chrome all / Safari all */
    -moz-user-select: none;     /* Firefox all */
    -ms-user-select: none;      /* IE 10+ */
    user-select: none;          /* Likely future */ 
}

.pen {
    height: 52px;
    //display: none;
    @extend %box;

    &_bar {
        width: 100%;
        height: 6px;
        border-bottom: 3px solid #d6c9bc;
        position: relative;

        &_progress {
            width: 0%;
            height: 6px;
            position: absolute;
            left: 0;
            background: #fcab0b;
            box-shadow: 0px 3px inset #fdbc3d;
        }
    }
}

.mystats {
    @extend %box;  
    margin-top: 110px;
    float: left;
    padding: 30px;
    clear: left;

    img {
        width: 15px * 3;
        position: absolute;
        left: -24px;
        top: -24px;
        z-index: 1;
    }

    .pixelsBottom,
    .pixelsTop {
        width: calc(100% + -4px);
    }

    & .swatch {
        width: 12px;
        height: 11px;
        position: relative;
        top: 3px;
        left: -16px;
        margin-right: 6px;
        padding: 0;
        float: left;
        margin-right: -10px
    }

    div {
        padding-left: 16px;
    }

    &_html {
        clear: left;

        & .swatch {
            background: #f1753f;

        }
    }

    &_css {
        clear: left;

        & .swatch {
            background: #2965f1;

        }
    }

    &_js {
        clear: left;

        & .swatch {
            background: #f3e273;

        }
    }

    &_design {
        clear: left;

        & .swatch {
            background: #9d28e0;

        }
    }

    h2 {
        border-bottom: 3px solid #d6c9bc;
        float: left;
        margin-bottom: 16px;
    }

    span.val {
        display: inline-block;
        position: relative;
        left: -8px;
        color: #594c3d;
    }

    span {
        color: #d6c9bc;
    }
}

p {
    margin: 0;
}
.pip {

    @extend %box;
    background: white;
    position: absolute;
    left: 0;
    line-height: 0px;
    right: 0;
    margin: auto;
    text-align: center;
    width: 30px;
    padding: 11px 7px 2px 7px;
    height: 10px;
    top: 50%;

}
.sep {
    display: inline-block;
    width: 2px;
    height: 10px;
    background: #d6c9bc;
}

.releasedEmpty {
    @extend %box;
    clear: both;
    float: right;
    margin-top: 249px;
    height: 60px;
    line-height: 61px;
    position: absolute;
    right: 53px;
    width: 303px;

}
.pen {
    position: absolute;
    left: 0;
    right: 0;
    margin: auto;
    width: 728px;

    & .swatch {
        width: 12px;
        height: 11px;
        position: relative;
        top: 3px;
        margin-left: 2px;
        float: left;
        margin-right: -10px;
    }

    &_html {
        & .swatch {
            background: #f1753f;   
        }
    }

    &_css {
        & .swatch {
            background: #2965f1;   
        }
    }

    &_js {
        & .swatch {
            background: #f3e273;   
        }
    }

    &_design {
        & .swatch {
            background: #9d28e0;   
        }
    }

    &_html,
    &_css,
    &_js,
    &_design {

        @extend %box;



        float: left;
        position: relative;
        top: 18px;
        margin-right: 27px;
        padding: 3px;
        width: 149px;
        left: 13px;
        text-align: center;

    }
}

.releasedHeader {
    @extend %box-blue;

    float: right;
    color: #c4ebfd;
    position: absolute;
    margin-top: 195px;
    top: 15px;
    right: 194px;

    img.icon {
        width: 7px * 3;
        top: 4px;
        position: relative;
    }

    img.arrow {
        width: 2px * 3;
        top: 0px;
        position: relative;
    }

}

.released {
    clear: both;
    float: right;
    margin-top: 228px;
    height: 420px;
    overflow: scroll;
    padding: 0px 40px 20px 6px;
    position: relative;
    left: 20px;
    width: 310px;
    overflow-x: hidden;
    border-top: 3px solid #bfaf9d;

    &::after {
        display: block;
        content: '';
        position: fixed;
        right: 0;
        top: 641px;
        background: -webkit-linear-gradient(top, rgba(0, 0, 0, 0) 10%, rgba(225, 218, 197, 01) 100%);
        width: 390px;
        height: 80px;
        z-index: 2;
    }
    &_pen {
        transition: all 1s;

        float: left;
        clear: left;
        margin-top: 17px;
        height:0;

        &__top {
            @extend %box;

            z-index:2;
            height: 66px;
            padding: 10px;
        }
        &__bottom {
            @extend %box;
            height: 20px;
            top:-72px;
            transition: all 1s;
            padding-top:30px;
            width: calc(100% - 48px);
            left: 12px;

            .sep {
                margin: 0 9px;
            }

            img {
                margin-right: 6px;
                position: relative;
            }

            img.views {
                width: 7px * 3;
                top: 2px;
            }

            img.likes {
                width: 5px * 3;
                top: 3px;
            }

            img.comments {
                width: 6px * 3;
                top: 3px;
            }
        }

        .star{
            position: absolute;
            right: 10px;
            top: 9px;
            img {
                width: 15px;
            }
        }

        &__graph {
            height: 34px;
            position: relative;
            width: 300px;
            border-left: $pixelWidth solid #e7e7e7;
            border-bottom: $pixelWidth solid #e7e7e7;
            margin: 8px 0;

            & .line {
                width: 10px;
                height: 40px;
                max-height: 34px;
                float: left;
                //min-height: 4px;
                position: relative;
                bottom: 0;
                background: #ff992c;
            }
        }
    }
}

bg = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/bgG.mp3>');
buttonClick = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/Buttonclick.mp3>');
featured = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/featured.mp3>');
slideSlow = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/slideSlow.mp3>');
countStats = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/Countupstats.mp3>');
researchClick = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/researchClick.mp3>');
researchInactive = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/researchInactive.mp3>');
slideFast = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/slideFast.mp3>');
featuredModal = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/featuredModal.mp3>');
researchComplete = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/researchComplete.mp3>');

const penProgressEl = $('.pen');
const statAddSounds = []

for(i = 0; i < 10; i++) {
    let a  = new Audio('<https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/statAdd.mp3>');
    statAddSounds.push(a)
}

function twShare(url, title, winWidth, winHeight) {
    const winTop = 100;
    const winLeft = 100;
    window.open(`https://twitter.com/intent/tweet?text=${title}`, 'sharer', `top=${winTop},left=${winLeft},toolbar=0,status=0,width=${winWidth},height=${winHeight}`);
}

pen_id = $('._pen_id').text();

$('body').on('click', '.share', () => {
    twShare(`https://codepen.io/jcoulterdesign/full/a1b3ea524ead4700015153bb95b881c3`, `I managed to get ${developer.followers.toLocaleString()} followers on the Codepen Simulator Game by @jamiecoulter89. <https://bit.ly/2LyxS71> %23codepenSimGame`, 520, 350);
    return false;
});

function updateMyStatsUi() {
    $('.mystats_css span.val').html(developer.css.toLocaleString());
    $('.mystats_html span.val').html(developer.html.toLocaleString());
    $('.mystats_js span.val').html(developer.js.toLocaleString());
    $('.mystats_design span.val').html(developer.design.toLocaleString());
}

const globals = {
    'timerTick' : 120,
    'keyTick' : 110,
    'penStatAddChance' : 4,
    'typeIncrement' : 1.1,
    'makingPen' : true,
    'penInProgress' : false,
    'viewDecay' : 1.1,
    'maxBars' : 30,
    'followerFriction' : 50,
    'viewMultiplier' : 1.15,
    'researchTime' : 2000,
    'researching' : false,
    'featuredMinStats' : 500,
    'featuredBoost' : 3.1,
    'featureChance' : 10,
    'paused' : true,
    'gameLength' : 365,
    'audio' : true,
    'auto' : false
}

const penNames = [
    'Swanky text inputs',
    'Three.js Interactive Unicorn',
    'Overly animated login box',
    'Yet another CSS grid',
    'Pure CSS Widget',
    'Pure CSS illustration',
    'Persistant cookie policy modal',
    'Overly complex 3D menu',
    'I could not stop',
    'Music player widget',
    'Codepen Simulation game',
    'Gross color combinations',
    'JS scratch and sniff',
    'Canvas and audio api thingy',
    'Giant animated cat',
    'Password strength indicator',
    'One element RPG game',
    'Pure CSS MMORPG',
    'Something with Google Maps',
    'Responsive responsivity checker',
    'Kill the King',
    'Pure CSS backend',
    'Procedurally generated cupcakes',
    'Unsubmittable form',
    'Never ending loading bar',
    'Invisible check boxes',
    'HTML Scrolling marquee',
    'Directly injected CSS',
    'No element element',
    'Three.JS Shooter game',
    'SVG animations',
    'Codepen challenge',
    'Pass the pen',
    'Edible code',
    'React calendar widget',
    'Square div that look round',
    'Netscape compatible CSS game',
    'Another User Interface',
    'Self learning AI in CSS',
    'HTML alternative',
    'Codepenception'  
]

const research = [
    {
        'index' : 1,
        'name' : 'Learn basic HTML',
        'cost' : 10,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 10,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 2,
        'name' : 'Learn basic CSS',
        'cost' : 20,
        'increaseCss' : 10,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 3,
        'name' : 'Learn basic JS',
        'cost' : 30,
        'increaseCss' : 0,
        'increaseJs' : 10,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 4,
        'name' : 'Learn basic Design',
        'cost' : 50,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 10,
        'researched' : false
    },{
        'index' : 5,
        'name' : 'Find inspiration',
        'cost' : 100,
        'increaseCss' : 10,
        'increaseJs' : 10,
        'increaseHtml' :10,
        'increaseDesign' : 15,
        'researched' : false
    },{
        'index' : 6,
        'name' : 'Learn HAML',
        'cost' : 150,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 15,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 7,
        'name' : 'Learn CSS animation',
        'cost' : 200,
        'increaseCss' : 15,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 8,
        'name' : 'Learn jQuery',
        'cost' : 300,
        'increaseCss' : 0,
        'increaseJs' : 15,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 9,
        'name' : 'Learn color theory',
        'cost' : 400,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 15,
        'researched' : false
    },{
        'index' : 10,
        'name' : 'Learn how to refactor',
        'cost' : 600,
        'increaseCss' : 15,
        'increaseJs' : 20,
        'increaseHtml' : 10,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 11,
        'name' : 'Learn BEM',
        'cost' : 800,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 20,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 12,
        'name' : 'Read CSS Tricks articles',
        'cost' : 1150,
        'increaseCss' : 20,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 13,
        'name' : 'Learn ES6',
        'cost' : 1400,
        'increaseCss' : 0,
        'increaseJs' : 20,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 14,
        'name' : 'Memorise font names',
        'cost' : 1800,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 20,
        'researched' : false
    },
    {
        'index' : 15,
        'name' : 'Watch youtube tutorials',
        'cost' : 2200,
        'increaseCss' : 10,
        'increaseJs' : 10,
        'increaseHtml' : 10,
        'increaseDesign' : 10,
        'researched' : false
    },{
        'index' : 16,
        'name' : 'Learn HTML6',
        'cost' : 2700,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 25,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 17,
        'name' : 'Learn pre-processors',
        'cost' : 3200,
        'increaseCss' : 25,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 18,
        'name' : 'Learn react',
        'cost' : 3800,
        'increaseCss' : 0,
        'increaseJs' : 25,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 19,
        'name' : 'Photoshop course',
        'cost' : 4500,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 25,
        'researched' : false
    },{
        'index' : 20,
        'name' : 'Browse Awwwards',
        'cost' : 5200,
        'increaseCss' : 10,
        'increaseJs' : 10,
        'increaseHtml' : 10,
        'increaseDesign' : 25,
        'researched' : false
    },{
        'index' : 21,
        'name' : 'Browse stack overflow',
        'cost' : 6000,
        'increaseCss' : 15,
        'increaseJs' : 15,
        'increaseHtml' : 15,
        'increaseDesign' : 10,
        'researched' : false
    },{
        'index' : 22,
        'name' : 'Learn angular',
        'cost' : 6600,
        'increaseCss' : 0,
        'increaseJs' : 25,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 23,
        'name' : 'Learn VR technology',
        'cost' : 7500,
        'increaseCss' : 0,
        'increaseJs' : 30,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 24,
        'name' : 'Experiment with latest tech',
        'cost' : 9000,
        'increaseCss' : 20,
        'increaseJs' : 20,
        'increaseHtml' : 20,
        'increaseDesign' : 10,
        'researched' : false
    },{
        'index' : 25,
        'name' : 'take a html master class',
        'cost' : 11000,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 60,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 26,
        'name' : 'take a CSS master class',
        'cost' : 12000,
        'increaseCss' : 60,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 27,
        'name' : 'take a JS master class',
        'cost' : 13000,
        'increaseCss' : 0,
        'increaseJs' : 60,
        'increaseHtml' : 0,
        'increaseDesign' : 0,
        'researched' : false
    },{
        'index' : 28,
        'name' : 'take a DESIGN master class',
        'cost' : 14000,
        'increaseCss' : 0,
        'increaseJs' : 0,
        'increaseHtml' : 0,
        'increaseDesign' : 60,
        'researched' : false
    },{
        'index' : 29,
        'name' : 'dO SOME CODE ACADEMY',
        'cost' : 15000,
        'increaseCss' : 30,
        'increaseJs' : 30,
        'increaseHtml' : 30,
        'increaseDesign' : 20,
        'researched' : false
    }
]

research.forEach(function(r) {
    $('.research_modal__list').append(`
<div class="item">
<div class="name">${r.name}<div class="sep"></div></div>
<div class="stat">
${r.increaseHtml > 0 ? `html <span class="green">+ ${r.increaseHtml}<img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/arrowUpStat.png"/></span><div class="sep"></div>` : ''}
${r.increaseCss > 0 ? `css <span class="green">+ ${r.increaseCss}<img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/arrowUpStat.png"/></span><div class="sep"></div>` : ''}
${r.increaseJs > 0 ? `js <span class="green">+ ${r.increaseJs}<img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/arrowUpStat.png"/></span><div class="sep"></div>` : ''}
${r.increaseDesign > 0 ? `design <span class="green">+ ${r.increaseDesign}<img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/arrowUpStat.png"/></span><div class="sep"></div>` : ''}
<div class="research_button" data-index="${r.index}"><div class="pixelsTop"></div>
<div class="pixelsBottom"></div>Research <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/rCost.png" /><span class="cost">${r.cost.toLocaleString()}</div></div>
</div>`)
})

$('.auto').click(function(){
    playSound(buttonClick);
    if(globals.auto) {
        $(this).removeClass('on');
        $(this).addClass('off');
        globals.auto = false;
    } else {
        $(this).removeClass('off');
        $(this).addClass('on');
        globals.auto = true;
    }
})

$('.researchButton').click(function() {
    if(!globals.researching) {
        globals.paused = true;
        $('.overlay, .research_modal').show();
        playSound(buttonClick);
        playSound(slideFast);
        $('.research_modal').show();

        setTimeout(function() {
            $('.research_modal').css('opacity', '1');
        },300)

        $('.overlay').fadeIn(function() {
            setTimeout(function() {
                $('.research_modal').css('height' , '400px');
                $('.research_modal').css('width' , '920px');

                setTimeout(function() {
                    $('.research_modal .hide').fadeIn();
                }, 400)
            },100)
        });
    } else {
        playSound(researchInactive);
    }

    $('.research_modal .item').each(function() {
        let index = $(this).find('.research_button').data('index') - 1;
        if(developer.followers >= research[index].cost && research[index].researched == false) {
            $(this).addClass('available') 
            $(this).removeClass('unavailable')  
            $(this).removeClass('researched')  
        }

        if(developer.followers < research[index].cost && research[index].researched == false) {
            $(this).addClass('unavailable')   
            $(this).removeClass('available')  
            $(this).removeClass('researched')  
        }

        if(research[index].researched == true) {
            $(this).addClass('researched')   
            $(this).removeClass('available')  
            $(this).removeClass('unavailable')  
        }
    })
})

audioSwitch = 0;
sfxSwitch = 0;

$('.options_sf').click(function() {
    if(sfxSwitch == 0) {
        globals.audio = false;
        sfxSwitch = 1;
        $(this).css('opacity','0.4');
    } else {
        globals.audio = true;
        sfxSwitch = 0;
        $(this).css('opacity','1');
    }
});

$('.options_bg').click(function() {
    if(audioSwitch == 0) {
        $(bg).animate({volume: 0}, 600);
        audioSwitch = 1;
        $(this).css('opacity','0.4')
    } else {
        $(bg).animate({volume: 1}, 600);
        audioSwitch = 0;
        $(this).css('opacity','1')
    }
})

$('.research_modal .close').click(function() {
    playSound(buttonClick)
    $('.research_modal').css('opacity', '0');
    setTimeout(function(){
        $('.overlay').fadeOut();
    },450)

    setTimeout(function(){

        $('.research_modal').attr('style', '');
        $('.research_modal .hide').attr('style', '');
    },1000)

    globals.paused = false;
})

$('body').on('click', '.research_button', function() {
    globals.paused = false;
    let r = $(this).data('index') - 1;
    let stat = research[r].stat;
    let increaseCss = research[r].increaseCss;
    let increaseJs = research[r].increaseJs;
    let increaseHtml = research[r].increaseHtml;
    let increaseDesign = research[r].increaseDesign;

    if(developer.followers > research[r].cost && research[r].researched == false && !globals.researching) {
        globals.researching = true;
        $('.overlay, .research_modal').fadeOut();
        $('.researchProgress').show();
        $('.researchProgress').show()
        playSound(researchClick)
        rp = setInterval(function(){
            $('.bar_inner').addClass('animate')
        },1)

        setTimeout(function() {
            clearInterval(rp)
            developer.css += increaseCss
            developer.js += increaseJs
            developer.html += increaseHtml
            developer.design += increaseDesign
            research[r].researched = true;
            $('.researchProgress').hide()
            globals.researching = false;
            playSound(researchComplete)
            updateMyStatsUi(); 
        }, globals.researchTime)

    } else {
        playSound(researchInactive)
    }
})

const statColors = {
    'html' : '#f16529',
    'css' : '#2965f1',
    'js' : '#d87b17',
    'design' : '#9d28e0'
}

var developer = {
    'name'      : 'Jamie',
    'level'     : 1,
    'html'      : 3,
    'css'       : 3,
    'js'        : 3,
    'design'    : 3,
    'followers' : 0
}

var pen = {
    'name' : 'Pen',
    'css'  : 0,
    'html' : 0,
    'js'   : 0,
    'design': 0
}

var pens = [];
updateMyStatsUi()
document.addEventListener("keyup", keyPress, false);

var progress = 0;

kS = 0;

function keyPress() {
    if(progress > 0) {
        $('.startMashing h2 span').html("that's it, keep going")
    }

    if(progress > 20) {
        $('.startMashing h2 span').html("Now we are getting somewhere")
    }

    if(progress > 40) {
        $('.startMashing h2 span').html("iron out those bugs")
    }

    if(progress > 70) {
        $('.startMashing h2 span').html("Almost finished")
    }

    if(progress > 99) {
        $('.startMashing h2 span').html("done!")
    }
    if(globals.makingPen && progress < 100 ) {
        if(!globals.researching && !globals.paused) {
            progress += globals.typeIncrement

            $('.pen_bar_progress').width(progress + '%');

            // Create a random number between 0 and the penStatChance variable
            let add =  Math.floor(Math.random() * globals.penStatAddChance) + (globals.penStatAddChance - 2);

            if(add == globals.penStatAddChance) {

                // Each keystroke, IF random check passes, pick a number between 1 and 3
                let stat =  Math.floor(Math.random() * 4) + 1;

                if(kS < statAddSounds.length - 1) {
                    kS++
                } else {
                    kS = 0
                }

                playSound(statAddSounds[kS])

                // Assign a stat based on the integer
                if(stat == 1) {
                    let htmlStat = Math.floor(Math.random() * developer.html) + 1;
                    pen.html = pen.html + htmlStat;
                    makePip(statColors.html, htmlStat, 'html');
                }

                if(stat == 2) {
                    let cssStat = Math.floor(Math.random() * developer.css) + 1;
                    pen.css = pen.css + cssStat;
                    makePip(statColors.css, cssStat, 'css');
                }

                if(stat == 3) {
                    let jsStat = Math.floor(Math.random() * developer.js) + 1;
                    pen.js = pen.js + jsStat;
                    makePip(statColors.js, jsStat, 'js');
                }

                if(stat == 4) {
                    let designStat = Math.floor(Math.random() * developer.design) + 1;
                    pen.design = pen.design + designStat;
                    makePip(statColors.design, designStat, 'design');
                }
            }
            updateStatUi();
        }
    } else {

        $('.complete_modal').show();
        playSound(featured)
        setTimeout(function(){
            playSound(slideFast)
        },400)

        setTimeout(function(){
            $('.complete_modal').css('opacity', '1')
        },300)
        $('.overlay').fadeIn(function(){

            setTimeout(function(){
                $('.complete_modal').css('height' , '370px')
                $('.complete_modal').css('width' , '600px')
                setTimeout(function(){
                    $('.complete_modal div.hide').fadeIn();
                }, 300)
            },100)
        });
        $('.complete_modal .html span span').html(pen.html)
        $('.complete_modal .css span span').html(pen.css)
        $('.complete_modal .js span span').html(pen.js)
        $('.complete_modal .design span span').html(pen.design)
        globals.paused = true;

    }
}

function updateStatUi() {
    $('.pen_css span.val').html(pen.css.toLocaleString());
    $('.pen_html span.val').html(pen.html.toLocaleString());
    $('.pen_js span.val').html(pen.js.toLocaleString());
    $('.pen_design span.val').html(pen.design.toLocaleString());
}

$('.make').click(function() {
    globals.makingPen = true;
    penProgressEl.show();
    $('.make').hide();
});

function makePip(stat, int, type) {
    $('body').append(`<div class="pip" data-type="${type}"><div class="pixelsTop"></div><div class="pixelsBottom"></div><p style="color:${stat};">${int}</p></div>`);
}

$('.release').click(function() {
    playSound(buttonClick)
    release(pen)
    globals.paused = false;
    playSound(slideSlow)
})

$('.scrap').click(function(){
    playSound(buttonClick)
    globals.paused = false;
    $('.startMashing h2 span').html("start pressing keys")

    $('.complete_modal').fadeOut();

    setTimeout(function(){
        $('.overlay').fadeOut()
    }, 450)

    progress = 0;
    $('.pen_bar_progress').width(0);

    pen.css = 0;
    pen.html = 0;
    pen.js = 0;
    pen.design = 0;

    setTimeout(function(){
        $('.complete_modal').attr('style', '');
        $('.complete_modal div').attr('style', '');
    },2000)

    updateStatUi();
})

function release(p) {
    $('.startMashing h2 span').html("start pressing keys")
    progress = 0;
    $('.releasedEmpty').remove()
    $('.overlay').fadeOut();
    $('.complete_modal').css('height','61px')
    $('.complete_modal').css('width','299px')
    $('.complete_modal').css( 'top', '298px')
    $('.complete_modal').css( 'left', '100%')
    $('.complete_modal').css( 'transform', 'translateX(calc(-100% - 57px))')

    setTimeout(function(){
        $('.released_pen').css('height', '150px')
    },210)
    setTimeout(function(){
        $('.released_pen').css('opacity', '1');

        $('.released_pen__bottom').css('top','-10px')

    },510)

    setTimeout(function(){
        $('.complete_modal').css('opacity', '0');
    },850)

    setTimeout(function(){
        $('.complete_modal').attr('style', '');
        $('.complete_modal div').attr('style', '');
    },2000)

    $('.complete_modal div').css('opacity', '0')
    let name =  Math.floor(Math.random() * penNames.length);

    let newPen = {
        'name' : penNames[name],
        'css'  : p.css,
        'html' : p.html,
        'js'   : p.js, 
        'design' : p.design,
        'views' : 0,
        'maxViews' : ((Math.ceil((p.css + p.js + p.html + p.design) * globals.viewMultiplier) + 1) * (pens.length + 1 / 35)),
        'dailyViews' : ((Math.ceil((p.css + p.js + p.html + p.design) * globals.viewMultiplier) + 1) * (pens.length + 1/ 35)),
        'comments' : 0,
        'likes' : 0,
        'featured' : false,
        'featuredBoosted' : false,
        'featuredCheck' : false,
        'featuredCheckCount' : 0
    }

    pens.push(newPen);

    $('.pen_bar_progress').width(0);

    pen.css = 0;
    pen.html = 0;
    pen.js = 0;
    pen.design = 0;
    updateStatUi();
    setTimeout(function(){
        $('.released').prepend(`<div class="released_pen" style="opacity:0"><div class="released_pen__top"><div class="pixelsTop"></div><div class="pixelsBottom"></div><span class="name">${pens[pens.length - 1].name}</span><div class="star"></div><div class="released_pen__graph"></div></div><div class="released_pen__bottom"><div class="pixelsTop"></div><div class="pixelsBottom"></div><img class="views" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/codepenViews.png" /><span class="view_count">${pens[pens.length - 1].views}</span><div class="sep"></div><img class="likes" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/codepenLikes.png" /><span class="like_count"> ${pens[pens.length - 1].likes}</span><div class="sep"></div><img class="comments" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/codepenComments.png" /><span class="comment_count"> ${pens[pens.length - 1].comments}</span></div></div>`)

    }, 1)
}
const monthNames = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                   ];
var time = 0;

const rootStatElementPosition = {
    'design' : '550px',
    'html' : '-550px',
    'css' : '-176px',
    'js' : '180px'
}

const pickers = [
    'marie mosely',
    'tim holman',
    'chris coyier',
    'codepen',
    'jamie coulter',
    'stephen shaw'
]

d = 0;

$('.awesome').click(function(){
    playSound(buttonClick)
    $('.overlay, .featured_modal').fadeOut();
    globals.paused = false;
})
function feature(penName) {
    globals.paused = true;
    $('.overlay, .featured_modal').show();

    let p =  Math.floor(Math.random() * pickers.length);

    $('.featured_modal .picker').html(pickers[p])
    $('.featured_modal .name').html(penName)
}

function gameLoop() {
    if(d == globals.gameLength) {
        globals.paused = true;
        $('.endGame, .overlay').show()
        $('.pencount').html(pens.length + ' ')
        let bestPen = '';

        if(pens.length > 1) {
            for(let i = 0; i < pens.length; i++) {
                if(pens[i + 1]) {
                    if(pens[i + 1].views > pens[i].views) {
                        bestPen = pens[i + 1]
                    }
                }
            }
        } else {
            bestPen = pens[0]
        }

        $('.mostName').html(bestPen.name)
        $('.mostViews').html(Math.ceil(bestPen.views).toLocaleString())
        globals.paused = true;
    }

    if(!globals.paused){
        time++;
        $('.researchButton_counter span').html($('.available').length)
        $('.pip').each(function() {

            if($(this).data('type') == 'html') {
                $(this).animate({ left: rootStatElementPosition.html, top: '140px' }, 2000, function(){
                    $(this).remove();
                });
            }

            if($(this).data('type') == 'css') {
                $(this).animate({ left: rootStatElementPosition.css, top: '140px' }, 1000, function(){
                    $(this).remove();
                });
            }

            if($(this).data('type') == 'js') {
                $(this).animate({ left: rootStatElementPosition.js, top: '140px' }, 1000, function(){
                    $(this).remove();
                });
            }

            if($(this).data('type') == 'design') {
                $(this).animate({ left: rootStatElementPosition.design, top: '140px' }, 1000, function(){
                    $(this).remove();
                });
            }

        })
        if(globals.auto && !globals.researching && !globals.paused) {
            if(time > globals.keyTick) {
                keyPress()
            }
        }
        if(time > globals.timerTick) {

            time = 0;
            d++;
            var day = new Date();
            var nextDay = new Date(day);
            nextDay.setDate(day.getDate() + d);
            let month = nextDay.getUTCMonth();
            let days = nextDay.getDate();
            let year = nextDay.getFullYear();
            $('.date span').html(`${monthNames[month]} ${days}, ${year}`) 
            $('.research_modal .item').each(function() {
                let index = $(this).find('.research_button').data('index') - 1;
                if(developer.followers > research[index].cost && research[index].researched == false) {
                    $(this).addClass('available') 
                    $(this).removeClass('unavailable')  
                    $(this).removeClass('researched')  
                }

                if(developer.followers < research[index].cost && research[index].researched == false) {
                    $(this).addClass('unavailable')   
                    $(this).removeClass('available')  
                    $(this).removeClass('researched')  
                }

                if(research[index].researched == true) {
                    $(this).addClass('researched')   
                    $(this).removeClass('available')  
                    $(this).removeClass('unavailable')  
                }
            })

            $('.released_pen').each(function() {
                let index = pens.length - $(this).index() - 1;
                let height = Math.ceil(pens[index].dailyViews / pens[index].maxViews * 100);

                if(pens[index].featured) {
                    $(this).find('.star').html('<img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/gStar.png" />')   
                }
                if(height > 100) {
                    $(this).find('.released_pen__graph').append(`<div class="line" style="height:${height}%; top:${0}%"></div>`);
                } else {
                    $(this).find('.released_pen__graph').append(`<div class="line" style="height:${height}%; top:${100 - height}%"></div>`);
                }

                let el = $(this);


                if(el.find('.line').length > globals.maxBars) {
                    el.find('.line:first-child').remove();
                }

                let final = Math.ceil(pens[index].views).toLocaleString();
                $(this).find('.view_count').html(final);

                let comment = Math.ceil(pens[index].comments).toLocaleString();
                $(this).find('.comment_count').html(comment);

                let like = Math.ceil(pens[index].likes).toLocaleString();
                $(this).find('.like_count').html(like);
            });

            var dailyFollowers = 0;

            pens.forEach(function(p) {
                if(p.css + p.html + p.css + p.design > globals.featuredMinStats) {
                    let f = Math.floor(Math.random() * globals.featureChance);
                    if(f == 0 && !p.featuredCheck){

                        if(p.featuredCheckCount < 14) {
                            p.featured = true;
                        }
                    } else {
                        p.featuredCheckCount++; 
                    }

                }
                if(p.featured && !p.featuredBoosted) {
                    p.dailyViews = p.dailyViews * globals.featuredBoost;
                    p.featuredBoosted = true;
                    feature(p.name)
                    playSound(featuredModal)
                }

                p.dailyViews = (p.dailyViews / globals.viewDecay);
                p.likes += Math.floor((p.dailyViews / globals.viewDecay) / 40);
                p.comments += Math.floor((p.dailyViews / globals.viewDecay) / 2000);
                p.views += p.dailyViews;
                dailyFollowers += p.dailyViews
            });

            developer.followers += Math.floor((dailyFollowers / globals.followerFriction) / ((developer.html + developer.css +developer.js + developer.design) / 10) );

            $('.followers span').html(developer.followers.toLocaleString());
            $('.endGame h1').html(developer.followers.toLocaleString());
        }
    }
    window.requestAnimationFrame(gameLoop);
}

$('.go').click(function(){
    playSound(buttonClick)
    $('.intro_modal').fadeOut(function(){
        $('.overlay').fadeOut();
        globals.paused = false
    })
})

window.requestAnimationFrame(gameLoop);

class Grain {
    constructor (el) {
        this.patternSize = 150;
        this.patternScaleX = 1;
        this.patternScaleY = 1;
        this.patternRefreshInterval = 3; // 8
        this.patternAlpha = 12; // int between 0 and 255,
        this.canvas = el;
        this.ctx = this.canvas.getContext('2d');
        this.ctx.scale(this.patternScaleX, this.patternScaleY);
        this.patternCanvas = document.createElement('canvas');
        this.patternCanvas.width = this.patternSize;
        this.patternCanvas.height = this.patternSize;
        this.patternCtx = this.patternCanvas.getContext('2d');
        this.patternData = this.patternCtx.createImageData(this.patternSize, this.patternSize);
        this.patternPixelDataLength = this.patternSize *this.patternSize* 4; // rgba = 4
        this.resize = this.resize.bind(this);
        this.loop = this.loop.bind(this);
        this.frame = 0;
        window.addEventListener('resize', this.resize);
        this.resize();
        window.requestAnimationFrame(this.loop);
    }

    resize () {
        this.canvas.width = window.innerWidth * devicePixelRatio;
        this.canvas.height = window.innerHeight * devicePixelRatio;
    }

    update () {
        const {patternPixelDataLength, patternData, patternAlpha, patternCtx} = this;

        // put a random shade of gray into every pixel of the pattern
        for (let i = 0; i < patternPixelDataLength; i += 4) {
            // const value = (Math.random() * 255) | 0;
            const value = Math.random() * 255;

            patternData.data[i] = value;
            patternData.data[i + 1] = value;
            patternData.data[i + 2] = value;
            patternData.data[i + 3] = patternAlpha;
        }

        patternCtx.putImageData(patternData, 0, 0);
    }

    draw () {
        const {ctx, patternCanvas, canvas, viewHeight} = this;
        const {width, height} = canvas;

        // clear canvas
        ctx.clearRect(0, 0, width, height);

        // fill the canvas using the pattern
        ctx.fillStyle = ctx.createPattern(patternCanvas, 'repeat');
        ctx.fillRect(0, 0, width, height);
    }

    loop () {
        // only update grain every n frames
        const shouldDraw = ++this.frame % this.patternRefreshInterval === 0;
        if (shouldDraw) {
            this.update();
            this.draw();
        }

        window.requestAnimationFrame(this.loop);
    }
}

const el = document.querySelector('.grain');
const grain = new Grain(el);

$('input').keydown(function(e){
    if (!e) e = window.event;
    var keyCode = e.keyCode || e.which;
    if (keyCode == '13'){
        if($('input').val() != '') {
            playSound(buttonClick)
            $('.name_modal').css('left','-200%');
            $('.intro_modal').css('left','0%');
            $('.username h2').html($('input').val())
            playAudio(bg)
        } else {
            $('input').css('border-color', '#f16059')
        }
        return false;
    }
})

$('.next').click(function() {
    if($('input').val() != '') {
        playSound(buttonClick)
        $('.name_modal').css('left','-200%');
        $('.intro_modal').css('left','0%');
        $('.username h2').html($('input').val())
        playAudio(bg)
    } else {
        $('input').css('border-color', '#f16059')
    }
})

function animateValue(c, start, end, duration) {
    var range = end - start;
    var current = start;
    var increment = end > start? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = $('.' + c)
    var timer = setInterval(function() {
        current += increment;
        obj.innerHTML = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}

// ## Create a function to play our sounds
function playSound(sound) {
    if (globals.audio) {
        sound.play(); // Play sound
    }
}

function playAudio(sound) {
    sound.loop = true;
    sound.volume = 0.5;
    sound.play(); // Play sound
}
```
