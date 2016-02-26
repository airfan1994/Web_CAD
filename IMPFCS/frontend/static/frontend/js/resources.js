var days = new Array("一", "二", "三", "四", "五", "六", "日");

function resetTimelinr() {
  $().timelinr({
    orientation: 'vertical',
    issuesSpeed: 400,
    datesSpeed: 100,
    arrowKeys: 'true',
    startAt: 1,
    mousewheel: 'false'
  });
}

function requestListMyApplies() {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/resources/apply/list",
    success: function(msg) {
      if (msg.applies) {
        $.each(msg.applies, function(i, n) {
          var time = n.resource_one.year + "-" + n.resource_one.month + "-" + n.resource_one.day;
          var state = "<span class=\"label ";
          if (n.state == "accepted") {
            state += "label-success";
          } else if (n.state == "denied") {
            state += "label-important";
          } else {
            state += "";
          }
          state += "\">" + n.state + "</span>"
          $("#myApplies").append("<tr><td>" + n.resource.name + "</td><td>" + time + "</td><td>" + state + "</td><td>" + n.ctime + "</td></tr>");
        });
      }
    }
  });
}

function requestListApplies() {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/resources/manage/apply/list",
    success: function(msg) {
      if (msg.applies) {
        $.each(msg.applies, function(i, n) {
          var time = n.resource_one.year + "-" + n.resource_one.month + "-" + n.resource_one.day;
          $("#applies").append("<tr><td>" + n.resource.name +
              "</td><td>" + time +
              "</td><td>" + n.user.name +
              "</td><td>" + n.user.department +
              "</td><td>" + n.user.student_class +
              "</td><td>" + n.contact_info +
              "</td><td>" + n.reason +
              "</td><td>" + n.ctime +
              "</td><td><a class=\"btn green\" href=\"javascript:void(0)\" onclick=\"acceptApply('" + n.apply_id + "')\">接受</a>" +
              "</td><td><a class=\"btn red\" href=\"javascript:void(0)\" onclick=\"denyApply('" + n.apply_id + "')\">拒绝</a></td></tr>");
        });
      }
    }
  });
}

function requestListResources() {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/resources/list",
    success: function(msg) {
      if (msg.resources) {
        fillTable(msg);
      }
    }
  })
}

function fillTable(msg) {
  //$("#year").text(msg.year);
  //$("#month").text(msg.month);
  var day = msg.first_day;
  $("#dates").empty();
  $("#issues").empty();
  $.each(msg.resources, function(i, n) {
    if (n != undefined && n != "" && n != []) {
      var r = "";
      $.each(n, function(j, m) {
        r += "<p><a href=\"javascript:void(0)\" onclick=\"viewResource('" + m.resource_id + "', '" + m.resource_one_id +"')\">" + m.name + "</a></p>";
      });
      $("#dates").append("<li><a href=\"#day_" + (i+1) + "\">" + (i+1) + "日 星期" + days[day-1] + "</a></li>");
      $("#issues").append("<li id=\"day_" + (i+1) + "\"><h1>" + msg.month + "月" + (i+1) + "日</h1>" + r + "</li>");
      day ++;
      if (day > 7) {
        day = 1;
      }
    }
  });
  resetTimelinr();
}

function viewResource(rid, roid) {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/resources/view?resource_id=" + rid,
    success: function(msg) {
      $("#resourceName").text(msg.name);
      $("#resourceDescription").text(msg.description);
      $.each(msg.resource_ones, function(i, n) {
        if (n.resource_one_id == roid) {
          $("#resourceDate").text(n.year + "年" + n.month + "月" + n.day + "日");
          $("#resource_one_id").val(roid);
        }
      })
      $("#contact_info").val("");
      $("#reason").val("");
      $("#viewResourceModal").modal();
    }
  })
}

function submitApply() {
  $.ajax({
    type: "POST",
    url: "/api/resources/apply/",
    data: $('#applyForm').serialize(),
    success: function(data) {
      if (data.success == 1) {
        alert("申请信息已发送!");
        location.reload();
      } else {
        alert("申请失败！" + data.error);
      }
    }
  });
}

function addResource() {
  $.ajax({
    type: "POST",
    url: "/api/resources/manage/add/",
    data: $('#addForm').serialize(),
    success: function(data) {
      if (data.success == 1) {
        alert("添加资源成功!");
        location.reload();
      } else {
        alert("添加失败！" + data.error);
      }
    }
  });
}

function acceptApply(apply_id) {
  $.ajax({
    type: "GET",
    url: "/api/resources/manage/apply/reply?accept=true&apply_id=" + apply_id,
    success: function(data) {
      if (data.success == 1) {
        alert("回复成功!");
        location.reload();
      } else {
        alert("回复失败！" + data.error);
      }
    }
  });
}

function denyApply(apply_id) {
  $.ajax({
    type: "GET",
    url: "/api/resources/manage/apply/reply?accept=false&apply_id=" + apply_id,
    success: function(data) {
      if (data.success == 1) {
        alert("回复成功!");
        location.reload();
      } else {
        alert("回复失败！" + data.error);
      }
    }
  });
}

