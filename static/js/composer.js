let currentScore = {};

$(function(){
  function toneLabel(v){
    if(v<25) return "Formal";
    if(v<60) return "Friendly";
    return "Witty";
  }
  $("#tone").on("input", function(){
    $("#tone-label").text(toneLabel($(this).val()));
  });
  $("#compose-btn").click(function(){
    const payload = {
      purpose: $("#purpose").val(),
      audience: $("#audience").val(),
      tone_label: toneLabel($("#tone").val()),
      tone: Number($("#tone").val()),
      keywords: $("#keywords").val(),
      freeform: $("#freeform").val()
    };
    $.ajax({
      url: "/compose",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(payload),
      success: function(res){
        $("#preview").val(res.prompt);
        currentScore = res.score;
        const d = res.score.details;
        $("#score-details").html(
          `Score: ${res.score.total}<br><span>Clarity: ${d.clarity}</span><span>Specificity: ${d.specificity}</span><span>Tone: ${d.tone_match}</span>`
        );
      }
    });
  });
  $("#save-btn").click(function(){
    const payload = {
      purpose: $("#purpose").val(),
      audience: $("#audience").val(),
      tone_label: toneLabel($("#tone").val()),
      tone: Number($("#tone").val()),
      keywords: $("#keywords").val(),
      freeform: $("#freeform").val(),
      prompt: $("#preview").val(),
      score: currentScore
    };
    $.ajax({
      url: "/save",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(payload),
      success: function(){ alert("Saved!"); }
    });
  });
  // Manual Recalculate button
  $("#recalc-btn").click(function(){
    const newText = $("#preview").val();
    $.ajax({
      url: "/recalculate_score",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ prompt: newText }),
      success: function(score) {
        currentScore = score;
        const d = score.details;
        $("#score-details").html(
          `Score: ${score.total}<br>
           <span>Clarity: ${d.clarity}</span>
           <span>Specificity: ${d.specificity}</span>
           <span>Tone: ${d.tone_match}</span>`
        );
      }
    });
  });
});
