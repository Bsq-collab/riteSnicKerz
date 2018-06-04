var electives = document.getElementsByClassName("elective");
var elective_json = {};

var get_electives = function() {
  elective_json = {};
  for (var i = 0; i < electives.length; i++) {
    elective_json[electives[i].getAttribute("name")] = electives[i].value;
  };
  console.log(elective_json);
};
