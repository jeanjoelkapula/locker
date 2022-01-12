/**/
//csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function advance_to_stage (element) {
    json_data = JSON.stringify({'stage': parseInt(element.dataset.stage)});

    const request = new Request(
        `/lead/${lead.id}/advance`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: 'POST',
        body: json_data,
        "mode": "same-origin"
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.log(data.error);
        }

        if (data.success) {
            var	steps = jQuery(".step");

            steps.each((index, stage) => {
        
                if ((stage.dataset.step) <= parseInt(element.dataset.step)) {
                    jQuery(stage).addClass('current');
                    jQuery(stage).addClass('done');

                    pipeline_stage = lead.pipeline_stages.find(item => item.step == stage.dataset.step);
                    stage.dataset.complete = "True";

                    pipeline_stage.tasks.forEach(element => {
                        document.querySelector(`#task-input-${element.id}`).checked = true;
                    });
                }
            });

            lead.status = data.status;
            if (data.status.name == "Won") {
                document.querySelector('#lead-status').innerHTML = data.status.name;

            }

            $('.advance-link').hide();
        }
        
    })
    .catch(error => {
        console.log( error);
    });
}

function complete_task(element) {
    if (lead.status.name == "Open") {
        list = document.querySelectorAll('.step');
        item = Array.from(list).find(x => x.dataset.step == element.dataset.step);
        if (element.checked) {
            is_complete = true;
        }
        else {
            is_complete = false;
        }


        if (item.dataset.complete == "False") {
            json_data = JSON.stringify({'is_complete': is_complete, 'lead': lead.id});

            const request = new Request(
                `/task/${element.dataset.task}/complete`,
                {headers: {'X-CSRFToken': csrftoken}}
            );

            fetch(request, {
                method: 'POST',
                body: json_data,
                "mode": "same-origin"
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.log(data.error);
                }

                if (data.success) {
                    var	steps = jQuery(".step");

                    steps.each((index, stage) => {
                
                        if ((stage.dataset.step) <= parseInt(element.dataset.step)) {
                        }
                    });

                    
                    if (data.is_stage_complete) {
                        var	steps = jQuery(".step");
                        item.dataset.complete = "True";
                        steps.each((index, stage) => {
                    
                            if ((stage.dataset.step) <= parseInt(item.dataset.step)) {
                                jQuery(stage).addClass('current');
                                jQuery(stage).addClass('done');
            
                                pipeline_stage = lead.pipeline_stages.find(item => item.step == stage.dataset.step);
                                stage.dataset.complete = "True";
                                pipeline_stage.tasks.forEach(element => {
                                    document.querySelector(`#task-input-${element.id}`).checked = true;
                                });
                            }
                        });

                        $('.advance-link').hide();
                    }
                    else {
                        item.dataset.complete= "False";
                    }
                }
                
            })
            .catch(error => {
                console.log( error);
            });
        }
        else {
            element.checked = true;


        }
    }

    if (lead.status.name == "Won") {
        element.checked = true;
    }
}

function save_status(element) {
    $('#reason').val('');
    $('#reason-error').hide();
}

function update_lead_status(element) {
    reason = document.querySelector('#reason');
    reason_error = document.querySelector('#reason-error');
    status_value = $('#status-selection').val();

    if ($( "#status-selection option:selected" ).text() == "Lost") {
        if (reason.value.trim() == '') {
            reason_error.innerHTML = "Please the reason why this lead was lost";
            $(reason_error).show();
            $('#show-modal').click();
            return false;
        }
        else{
            json_data = JSON.stringify({'status': status_value, 'reason': reason.value});
        }
    }
    else {
        json_data = JSON.stringify({'status': status_value});
    }


        const request = new Request(
            `/lead/${element.dataset.lead}/status`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request, {
            method: 'POST',
            body: json_data,
            "mode": "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log(data.error);
                Swal.fire(
                    'Lead Status Update',
                    data.error,                
                    'error'
                );
            }

            if (data.success) {
                lead.status = data.status;

                var	steps = jQuery(".step");

                if ((data.status.name == "Lost") || (data.status.name == "Cancelled")) {
                    steps.each((index, stage) => {
            
                        if (stage.dataset.complete == "True") {
                            $(stage).removeClass('current');
                            $(stage).addClass('step-disabled');
                        }
                        else {
                            $(stage).addClass('step-list-item');
                        }
                    });

                    $('input[type=checkbox]').attr('disabled', true);
                }

                if ((data.status.name == "Open") || (data.status.name == "Won")) {
                    steps.each((index, stage) => {
            
                        if (stage.classList.contains('step-disabled')) {
                            $(stage).removeClass('step-disabled');
                        }
                        
                        if(stage.classList.contains('done')){
                            $(stage).addClass('current');

                        }
                        else {
                            $(stage).addClass('step-list-item');

                        }
                    });

                    
                }

                if (data.status.name == "Open") {
                    $('input[type=checkbox]').attr('disabled', false);
                }
                
                Swal.fire(
                    'Lead Status Update',
                    data.success,                
                    'success'
                );
            }
            $('#reason').val('');
            $('#reason-error').hide();
            $('.close').click();
        })
        .catch(error => {
            console.log( error);
        });

}

jQuery( document ).ready(function() {
		
    var back =jQuery(".prev");
    var	next = jQuery(".next");
    var	steps = jQuery(".step");

    $(steps).on('click', function (){
        current_stage=this;
        current = parseInt(this.dataset.step);
        $('.advance-link').hide();

        steps.each((index, element) => {

            if ((element.dataset.complete == "False") && (parseInt(element.dataset.step) > 1)) {
                jQuery(element).removeClass('pipeline-stage');  
                jQuery(element).addClass('step-list-item');    
            }

            if ((parseInt(element.dataset.step) == current) && (element.dataset.complete === "False")) {
                jQuery(element).addClass('pipeline-stage');
                jQuery(element).removeClass('step-list-item');
                $(`#advance-link-${current}`).show();

            }
        });
    });

})