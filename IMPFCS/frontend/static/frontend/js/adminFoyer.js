
function requestListResources() {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/api/resources/list",
        success: function(data) 
        {
            var list = $('#resources');
            $.each(data.resources, function(i, n) 
                { 
                    $.each(n, function(j, res)
                        {
                            list.append('');
                        }
                    );
                }
            );
        }
    });
}


requestListResources()
$('#addResourceBtn').click(addResource);