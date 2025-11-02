$(function(){
  function loadLibrary(){
    $.get("/library", function(res){ renderList(res); });
  }
  function renderList(list){
    const $lib = $("#library-list");
    $lib.empty();
    if(!list.length){ $lib.text("No prompts yet."); return; }
    list.slice().reverse().forEach(it=>{
      const card = $(`<div class='border rounded p-2 mb-2 library-item' style='cursor:pointer;'><strong>${it.purpose}</strong> (${it.tone_label})<div class='small text-muted'>${it.keywords}</div><div class='small'>Score: ${(it.score?.total)||'—'}</div><div class='mt-1 small text-secondary'>${it.prompt.slice(0,100)}...</div></div>`);
      card.click(function(){
        $("#purpose").val(it.purpose);
        $("#audience").val(it.audience);
        $("#tone").val(it.tone);
        $("#tone-label").text(it.tone_label);
        $("#keywords").val(it.keywords);
        $("#freeform").val(it.freeform || "");
        $("#preview").val(it.prompt);
        if (it.score) {
          const d = it.score.details || {};
          $("#score-details").html(
            `Score: ${it.score.total}<br>
             <span>Clarity: ${d.clarity||0}</span>
             <span>Specificity: ${d.specificity||0}</span>
             <span>Tone: ${d.tone_match||0}</span>`
          );
        } else {
          $("#score-details").text("No score data");
        }
        $('html, body').animate({ scrollTop: $("#compose-btn").offset().top - 100 }, 400);
      });
      $lib.append(card);
    });
  }
  $("#search-btn").click(function(){
    const kw = $("#search-key").val();
    $.ajax({
      url: "/library/search",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({keyword: kw}),
      success: renderList
    });
  });
  loadLibrary();
});