The elements in source pages of each linkedin jon listing varies massively.

basically we are looking for the following elements

1 -
```html
    <script type="application/ld+json">
    </script>
```

if it's included you basically hit the jackpot everything is there in one place and no need to do anything else except parsing it


some other important class is

2 -
```html

    <div class="salary compensation__salary">
      $126,000.00/yr - $180,000.00/yr
    </div>
```

which is basically free statistics on a gold plate
and lastly something that always exists is

3 -
```html
    <section class="show-more-less-html" data-max-lines="5">
        <div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5
            relative overflow-hidden">
        </div>
```

not here I kept everything without thew data inside the class since it's TOO long, if you want to see the output yourself please check [Ex](Ex_of_imp_elements.html)