// search.js

$ (function () {
  $ ('#rarity-filter').change (function () {
    var rarity = $ (this).val ();
    if (rarity) {
      window.location.href = '?rarity=' + rarity;
    } else {
      window.location.href = '.';
    }
  });
});
