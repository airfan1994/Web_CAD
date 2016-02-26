

function getTeamMemberApplications() {
  $.get('/api/users/manage/apply/list',
      function(msg) 
      {
        if (msg.applications) 
        {
          $.each(msg.applications, function(i, n) {
            $("#applies").append("<tr><td>" + n.studentNum +
                "</td><td>" + n.name +
                "</td><td>" + n.department +
                "</td><td>" + n.studentClass +
                "</td><td>" + n.teamCategory +
                "</td><td>" + n.teamName +
                "</td><td>" + n.teamRole +
                "</td><td>" + n.coach +
                "</td><td>" + n.ctime +
                "</td><td><a class=\"btn green\" href=\"javascript:void(0)\" onclick=\"acceptTeamMemberApplication('" + n.studentNum + "')\">接受</a>" +
                "</td><td><a class=\"btn red\" href=\"javascript:void(0)\" onclick=\"rejectTeamMemberApplication('" + n.studentNum + "')\">拒绝</a></td></tr>");
          });
      }
  });
}


function acceptTeamMemberApplication(studentNum) {
    $.post('/api/users/manage/teamMember/accept',
        {'studentNum': studentNum},
        function(data)
        {
            if (data.success == 1) 
            {
                alert("回复成功!");
                location.reload();
            } else 
            {
                alert("回复失败！" + data.error);
            }
        }
    );
}


function rejectTeamMemberApplication(studentNum) {
    $.post("/api/users/manage/teamMember/reject",
        {'studentNum': studentNum},
        function(data)
        {
            if (data.success == 1) 
            {
                alert("回复成功!");
                location.reload();
            } else 
            {
                alert("回复失败！" + data.error);
            }
        }
    );
}
