$(function () {
  //Năm tự động điền vào select
  var seYear = $("#year");
  var date = new Date();
  var cur = date.getFullYear();

  seYear.append('<option value=""> Year </option>');
  for (i = cur; i >= 1900; i--) {
    seYear.append('<option value="' + i + '">' + i + "</option>");
  }

  //Tháng tự động điền vào select
  var seMonth = $("#month");
  var date = new Date();

  var month = new Array();
  month[1] = "1";
  month[2] = "2";
  month[3] = "3";
  month[4] = "4";
  month[5] = "5";
  month[6] = "6";
  month[7] = "7";
  month[8] = "8";
  month[9] = "9";
  month[10] = "10";
  month[11] = "11";
  month[12] = "12";

  seMonth.append('<option value=""> Month </option>');
  for (i = 12; i > 0; i--) {
    seMonth.append('<option value="' + i + '">' + month[i] + "</option>");
  }

  //Ngày tự động điền vào select
  function dayList(month, year) {
    var day = new Date(year, month, 0);
    return day.getDate();
  }

  $("#year, #month").change(function () {
    //Đoạn code lấy id không viết bằng jQuery để phù hợp với đoạn code bên dưới
    var y = document.getElementById("year");
    var m = document.getElementById("month");
    var d = document.getElementById("day");

    var year = y.options[y.selectedIndex].value;
    var month = m.options[m.selectedIndex].value;
    var day = d.options[d.selectedIndex].value;
    if (day == " ") {
      var days = year == " " || month == " " ? 31 : dayList(month, year);
      d.options.length = 0;
      d.options[d.options.length] = new Option("-- Day --", " ");
      for (var i = 1; i <= days; i++) d.options[d.options.length] = new Option(i, i);
    }
  });
});
