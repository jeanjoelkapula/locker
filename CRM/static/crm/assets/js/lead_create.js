added_products = [];
added_people = [];

$(function() {

    $('#lead-name').on('keyup', function(){
        $('#lead-name-error').hide();
    });

    $('#date-closed').on('keyup', function(){
        $('#date-error').hide();
    });
    
    $('#company-selection').on('change', function(){
        company = company_list.find(company=> company.id == this.value);
        $('#person-selection').empty();
        company.members.forEach(member => {
            var newOption = new Option(member.first_name + " " + member.last_name, member.id, false, false);
            $('#person-selection').append(newOption).trigger('change');
        });
    });

    $('#company-selection').change();
   
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

function validate() {
    lead_name = document.querySelector('#lead-name');
    lead_name_error = document.querySelector('#lead-name-error');
    closed_date = document.querySelector('#closed-date');
    date_error = document.querySelector('#date-error');
    list = "";
    message = "";
    valid = true;
    people = $('#person-selection').select2('data');

    //check lead name
    if (lead_name.value.trim() == '') {
        lead_name_error.style.display = 'block';
    }
    else {
        lead_name_error.style.display = 'none';
    }

    //check expected closed date
    if (closed_date.value.trim() == '') {
        date_error.style.display = 'block';
    }
    else {
        date_error.style.display = 'none';
    }

    //check added product list
    if (added_products.length == 0) {
        list += "<li>Please select at least one product</li>";
        valid = false;
    }

    if (people.length == 0) {
        list += "<li>Please add at least one person</li>";
        valid = false;
    }
    
    message = `${list}`;

    if (valid) {
       
    }
    else {
        Swal.fire(
            'Invalid Lead',
             message,                
            'error'
        );
    }
    
    return valid;
}

function add_product () {
    selection = $('#product-selection').find(':selected');
    quantity = $('#product-quantity');
    products_container = document.querySelector('#products-container');

    list = "";
    message = "";
    valid = true;

    if (selection[0].value == "") {
        list += "<li>Please select a product</li>";
        valid = false;
    }

    if (quantity.val().trim() == '') {
        list += "<li>Please enter the quantity</li>";
        valid = false;
    }

    if (valid) {
        product = product_list.find(product => product.id == selection[0].value);
        result = added_products.find(product => product.id == selection[0].value);
        
        if (result) {
            Swal.fire(
                'Product',
                'This product has already been added',                
                'error'
            );
        }
        else {
            added_products.push({'id': product.id, 'quantity': parseInt(quantity.val())});

            div = document.createElement('div');
            div.className = "product-item";
            div.id = "product-" + product.id;

            div.innerHTML = `
                <div class="person-icon"> 
                    <i class="fas fa-box-open d-block"></i>
                </div>
                <div class="product-name">
                    ${product.name} (x${quantity.val()})
                </div>
                <div class="product-remove">
                    <a href="javascript:void(0)" data-product="${product.id}" onclick="remove_prodcut(this);">
                    <i class="fas fa-minus d-block"></i>
                    </a>
                </div>  
            `;

            products_container.append(div);
            $('#product-selection').val(null).trigger('change');
            quantity.val('');
        }
    }
    else {
        message = `${list}`;

        Swal.fire(
            'Product',
            message,                
            'error'
        );
    }
}

function remove_prodcut(element) {

    added_products = added_products.filter(function(value, index, arr){ 
        return value.id != element.dataset.product;
    });

    document.querySelector(`#product-${element.dataset.product}`).remove();
    $('#product-selection').val(null).trigger('change');
}

function save_lead(){
    if (validate()) {
        lead_name = document.querySelector('#lead-name').value;
        closed_date = document.querySelector('#closed-date').value;
        pipeline = parseInt(document.querySelector('#pipeline-selection').value);
        confidence = parseInt(document.querySelector('#confidence').value);
        is_lead_hot = document.querySelector('#is-lead-hot').checked;
        company = parseInt(document.querySelector('#company-selection').value);
        source = parseInt(document.querySelector('#source-selection').value);
    
        people = [];

        $('#person-selection').select2('data').forEach((element)=>{
            people.push({'id': parseInt(element.id), 'name': element.text})
        });
        data = {
            'lead_name': lead_name,
            'closed_date': closed_date,
            'pipeline': pipeline,
            'confidence': confidence,
            'priority': is_lead_hot,
            'company': company,
            'source': source,
            'products': added_products,
            'people': people

        }

        json_data = JSON.stringify(data);

        const request = new Request(
            '/lead/save',
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
                Swal.fire({
                    title: 'Invalid Lead',
                    text: data.error,                
                    type: 'error'
                });
            }
            
            if (data.success) {
                 Swal.fire({
                        title: 'Lead Created',
                        text: data.success,
                        type: 'success',
                        onClose: ()=>{
                            $('input').val('');
                            $('select').empty();
                            window.location.reload();
                        }
                        
                    });
            }
        })
        .catch(error => {
            console.log( error);
        });
    }

}