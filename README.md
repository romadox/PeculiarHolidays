# Peculiar Holidays Calendar
<i>An eternity of procedurally-generated holidays, in case you get tired of the usual ones.</i>

The Peculiar Holidays are a set of quirky alternative holidays, generated algorithmically to provide both variety & reptition as time goes along.

The official calendar of holidays can be found here: <a href="https://www.nashhigh.com/misc/peculiar-holiday-calendar">nashhigh.com/misc/peculiar-holiday-calendar</a>. It's entirely scripted, so you can explore all future (and even past) holidays. The embedded calendar HTML code is also in this repository as <a href="https://github.com/romadox/PeculiarHolidays/blob/master/cal.html">cal.html</a>.

I've also generated an <a href="https://github.com/romadox/PeculiarHolidays/blob/master/PeculiarHolidays-2019-1-1-to-2042-11-19.ics">iCalendar</a> and a <a href="https://calendar.google.com/calendar/b/1?cid=bGpxMTZqMjBrOWFhZW85Z29xbHJxbGk0Y3NAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ">Google Calendar</a> with the next ~20 years of Peculiar Holidays, if you want to import it to you phone/digital calendar program.

<h3>FAQ</h3>
<ul>
  <li><h4>Why celebrate computer-generated holidays?</h4><br>
    For fun! Part of the reason we like holidays is because they give us a reason to get together with friends & family and do something out of the ordinary. The goal of Peculiar Holidays is to give us the same excuse, but with a little extra variety & creativity.</li>
  <li><h4>How do I celebrate a Peculiar Holiday?</h4><br>
    However you want! The calendar script intentionally gives you only holiday names to work with. The rest is up to you!</li>
  <li><h4>Does everyone's calendar look different?</h4><br>
    No--the holidays are the same for everyone. Each holiday is created based on the date it falls on, so 5/10/2020 will always be Miniature Squirrelmas. The goal for Peculiar Holidays was to create new, fun holiday ideas for people to celebrate together, so it was important that everyone would see the same holidays!</li>
  <li><h4>Do holidays repeat each year?</h4><br>
    Not exactly. If the holidays always repeated, we'd either be stuck with the same ~40-50 holidays, or we'd have an ever-accumulating mass of holidays. Plus, we might get stuck with a boring holiday for all of time! Instead, holidays can repeat <i>for a few years</i>. Some holidays might not repeat at all, others might repeat for up to 6 years. That way each year should have a few repeats and plenty of brand new holidays.</li>
  <li><h4>What are the colors for?</h4><br>
    The font/banner color of a holiday indicates its rarity. Holidays can either be: Regular (Green), Special (Blue), Rare (Purple), or Legendary (Orange). You'll also notice that rarer holidays have more words in their title!
    Each month should have a few regular holidays, and possibly a special holiday. Rare holidays might only occur a couple times a year, and legendary holidays are even more sparse! (2020 has a Legendary holiday on 7/30, "Entreprenurial Fest of the Party Shorts Sun"; but after that there isn't one until the 2030's!)</li>
  <li><h4>What if I don't want to use these holidays? Can I generate my own?</h4><br>
    Sure! If you don't want to use the official set of holidays, just fork this code! In the function "initRolls(date)" there is a master seed value--changing it is the simplest way to get an entirely different set of holidays. Alternately, you can modify the various word tables to create your own possibilities or even set a specific theme.</li>
</ul>
