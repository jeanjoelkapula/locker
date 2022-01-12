steps = [
    {
        'step': 1,
        'stage_name': 'Pitch',
        'tasks': []
    }
]

current_step = 1;

$(function() {

    $('#stage-name').on('keyup', function(){
        $('#stage-name-error').hide();
    });

    $('#add-stage').on('click', function(){
        $('#stage-name').val('');
        $('#stage-name-error').hide();
    });

});


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


function show_tab(element) {
    $('.lead-tab-pane').hide();
    id = '#' + element.dataset.target;
    stage = steps.find(stage => stage.step == element.dataset.step);
    current_step = stage.step;
    $(id).show();
    
    //set current
    $('.step').removeClass('current');
    $(element).addClass('current');

}

function delete_stage(element){
    error = document.querySelector('#stage-edit-error');

    if (steps.length == 1) {
        error.innerHTML = 'The pipeline needs at least one stage';
        error.style.display = 'block';
    }
    else {
        error.style.display = 'none';

        document.querySelector(`#stage-${element.dataset.step}`).remove();
        step = steps.find(stage => stage.step == element.dataset.step);
        document.querySelector(`#tab-${step.step}`).remove();

        steps = steps.filter(function(value, index, arr){ 
            return value.step != element.dataset.step;
        });

        for(i=0; i < steps.length; ++i) {
            $($(`[data-step="${steps[i].step}"]`)[0]).data('step', i+1);
            $($(`[data-step="${steps[i].step}"]`)[1]).data('step', i+1);
            steps[i].step = i + 1;
        }
        $('.step').removeClass('current');
        $($('.step')[$('.step').length - 2]).addClass('current');
        current_step = steps[steps.length - 1].step;
        $(`#tab-${steps[steps.length - 1].step}`).show();
        $('#edit-dismiss').click();
    }
    
}

function edit_stage(element) {
    stage = steps.find(stage => stage.step == element.dataset.step);
    $('#stage-name-edit').val(stage.stage_name);
    document.querySelector('#edit_stage_button').dataset.step = element.dataset.step;
    document.querySelector('#edit-delete').dataset.step = element.dataset.step;
    $('#stage-edit-error').hide();
    $('#show-modal').click();
}

function save_stage_edit(button){
    stage = steps.find(stage => stage.step == button.dataset.step);

    //document.querySelector(`#tab-${stage.step}`).id = $('#stage-name-edit').val();
    //document.querySelector(`#tasks-${stage.step}`).id = 'tasks-' + $('#stage-name-edit').val();

    stage.stage_name = $('#stage-name-edit').val();
    document.querySelector(`#step-span-${button.dataset.step}`).innerHTML = $('#stage-name-edit').val();
    document.querySelector(`#step-span-${button.dataset.step}`).parentNode.dataset.target = 'tab-' + stage.step;
    document.querySelector(`#tab-step-${button.dataset.step}`).innerHTML = stage.stage_name;
    $('#stage-name-edit').val('');
    $('#edit-dismiss').click();
}

function new_task(element) {
    document.querySelector('#save-task').dataset.step = element.dataset.step;
}

function delete_task(element){
    stage = steps.find(stage => stage.step == element.dataset.step);
    document.querySelector(`#task-${element.dataset.task}`).remove();
    stage.tasks = stage.tasks.filter(function(value, index, arr){ 
        return value.id != element.dataset.task;
    });
}

function add_task(element){
    task_name = document.querySelector('#task-name').value;

    if (task_name.trim().length == 0) {
        error.innerHTML = 'Please enter a task name';
        error.style.display = 'block';
    }
    else {
        stage = steps.find(stage => stage.step == current_step);
        error = document.querySelector('#task-name-error');
        list_container = document.querySelector(`#tasks-${stage.step}`);
        
        task = document.createElement('div');
        task.id = `task-${stage.tasks.length + 1}`;
        task.innerHTML = `
            <div class="d-flex  w-100">
                <div class="col-9">
                    <label class="custom-control custom-checkbox m-0">
                        <input type="checkbox" class="custom-control-input" onclick="oncheck(this);">
                        <span class="custom-control-label">${task_name}</span>
                    </label>
                </div>
                <div style="margin-left: 20px;
                    height: 15px; ">
                    <button type="button" class="btn btn-default" data-step="${current_step}" data-task="${stage.tasks.length + 1}" onclick="delete_task(this);"><i class="fas fa-minus d-block"></i></button>
                </div>
            </div>
        `;

        stage.tasks.push({
            'id': stage.tasks.length + 1,
            'task_name': task_name
        });

        list_container.append(task);

        error.style.display = 'none';
        document.querySelector('#task-name').value = "";
        $('#dismiss-task-modal').click();
    }
    

}

function save_stage(){
    stage_name = document.querySelector('#stage-name').value;
    error = document.querySelector('#stage-name-error');
    lead_tab = document.querySelector('#lead-tab');

    steps_container = document.querySelector('#steps-container');

    if (stage_name.trim() != '') {

        if (steps.find(stage => stage.stage_name == stage_name)) {
            error.innerHTML = 'This stage name is already used';
            error.style.display = 'block';
        }
        else {
            error.style.display = 'none';
            $('#dismiss-stage-modal').click();

            stage_step = document.createElement('div');
            stage_step.id = `stage-${steps.length + 1}`;
            stage_tab = document.createElement('div');
            stage_tab.id = `tab-${steps.length + 1}`;
            stage_tab.style.display = 'none';
            stage_step.className = 'step-container';
            stage_step.innerHTML = `  
                <div class="step pipeline-stage" data-target="tab-${steps.length + 1}" data-step="${steps.length + 1}" onclick="show_tab(this);"> <span id='step-span-${steps.length + 1}'>${stage_name}</span> </div>
                <div class="step-edit"><a href="javascript:void(0)" data-step="${steps.length + 1}" data-target="tab-${steps.length + 1}" onclick="edit_stage(this);">Edit</a></div>
                `;

            steps_container.append(stage_step);
            stage_tab.className = 'lead-body lead-tab-pane';
            stage_name.id = stage_name;

            stage_tab.innerHTML = `
                <div class="lead-body-item ">
                    <div class="lead-body-item-header">
                        <h6>
                            Goal: <span id = "tab-step-${steps.length + 1}">${stage_name}</span>
                        </h6>
                    </div>
                    <div class="lead-body-item-content">
                        <div class="form-group row" style="width: 100%;">
                            <label class="col-form-label col-sm-1 text-sm-right">Stage Guidance</label>
                            <div class="col-sm-11">
                            <textarea id="guidance-${steps.length + 1}" class="form-control" placeholder="Textarea"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="lead-body-item ">
                    <div class="lead-body-item-header" style="display: flex; align-items: center;">
                        <h6 style="margin-top: 26px;">
                            Tasks
                        </h6>
                        <div style="margin-left: 20px;
                        height: 15px; ">
                          <button type="button" class="btn btn-default" data-toggle="modal" data-target="#modals-new-task" data-step="${steps.length + 1}"><i class="fas fa-plus d-block"></i></button>
                        </div>
                    </div>
                    <div class="lead-body-item-content">
                        <div class="content-div w-100" id="tasks-${steps.length + 1}">
                        
                        </div>
                    </div>
                </div>
            `;

            lead_tab.append(stage_tab);
            steps.push({
               'step': steps.length + 1,
               'stage_name': stage_name, 
               'tasks':[]
            });
        }
        
    }
    else {
        error.innerHTML = 'Please enter a stage name';
        error.style.display = 'block';
    }

}

function save_pipeline(element) {
    pipeline_name = document.querySelector('#pipeline-name').value;
    is_save = false;

    if (element.dataset.pipeline){
        url = `/pipeline/${element.dataset.pipeline}/edit`;
        is_save = true;
    }
    else{
        url = '/pipeline/save';
    }
   
    if (pipeline_name.trim().length == 0) {
        Swal.fire(
            'Missing pipeline name',
            'Please the enter the pipeline name',
            'error'
        );
    }
    else {
        is_guidance_missing = false;
        is_task_missing = false;

        guidance_message = "";
        task_message = "";

        steps.forEach(stage => {
            stage_guidance = document.querySelector(`#guidance-${stage.step}`).value.trim();
            message = "";

            div = document.createElement('div');
            list = "";

            if (stage_guidance.length== 0) {
                is_guidance_missing = true;
            }

            if (stage.tasks.length == 0) {
                is_task_missing = true;
            }

            if(is_guidance_missing) {
                list += "<li>Please ensure you enter some guidance for each stage</li>";
      
            }
            else {
                stage.guidance = stage_guidance;
            }

            if(is_task_missing) {
                list += "<li>Please ensure each pipeline stage has at least one task </li>";
               
            }


            if (is_guidance_missing || is_task_missing) {
                
                message =`
                    <ul>
                        ${list}
                    </u>
                `;

                Swal.fire(
                    'Invalid Pipeline',
                    message,                
                    'error'
                );

                return false;
            }
            
        });


        if (!is_guidance_missing && !is_task_missing) {
            json_data = JSON.stringify({
                'pipeline_name': pipeline_name,
                'steps': steps
            });

            const request = new Request(
                url,
                {headers: {'X-CSRFToken': csrftoken}}
            );

            fetch(request, {
                method: 'POST',
                body: json_data,
                "mode": "same-origin"
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Pipeline',
                        text: data.success,
                        type: 'success',
                        onClose: ()=>{
                            if (!is_save) {
                                $('input').val('');
                                $('textarea').val('');    
                            }
                            window.location.reload();
                        }
                        
                    });
                }
            })
            .catch(error => {
                console.error( error);
            });
        }
        
    }
}