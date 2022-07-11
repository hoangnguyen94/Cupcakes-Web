function list_cupcakes() {
    listCupcakes()
}

async function listCupcakes() {
    resp = await axios.get('/api/cupcakes');
    for (i = 0; i < resp.data.cupcakes.length; i++) {
        addCupcake = generateCupcake(resp.data.cupcakes[i]);
        $('.list-cupcakes').append(addCupcake);
    }
}

function generateCupcake(cupcake) {
    return `
        <div id="${cupcake.id}"> 
            <li>
                ${cupcake.flavor} / ${cupcake.rating} / ${cupcake.size}
            </li>
            <img src="${cupcake.image}" alt="(no image provided)" width="200" height="200">
            <button class="delete_cupcake" data-id="${cupcake.id}">X</button>
        </div>`;
}

$('button').click(addCupcake)

async function addCupcake(e) {
    e.preventDefault()
    if (!validateForm()) {
        console.log('Form did not validate');
        return;
    }

    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();
    res = await axios.post('/api/cupcakes', {flavor: flavor, 
        size: size,
        rating: rating,
        image: image});

    addCupcake = generateCupcake(res.data.cupcake);
    $('.list-cupcakes').append(addCupcake);
    $('#flavor').val('');
    $('#size').val('');
    $('#rating').val('');
    $('#image').val('');
}

function validateForm() {

    if ($('#flavor').val() == "") {
        alert('Please provide a flavor!');
        $('#flavor').focus();
        return false;
    }

    if ($('#size').val() == "") {
        alert('Please provide a size!');
        $('#size').focus();
        return false;
    }

    if ($('#rating').val() == "") {
        alert('Please provide a rating!');
        $('#rating').focus();
        return false;
    }

    const rating = $('#rating').val();
    const floatRating = parseFloat(rating);

    if (isNaN(floatRating)) {
        alert('Please provide a rating between 0 and 10!');
        $('#rating').focus();
        return false;
    }

    if (floatRating < 0 || floatRating > 10) {
        alert('Please provide a rating between 0 and 10!');
        $('#rating').focus();
        return false;
    }

    return true;
}

$('.list-cupcakes').on('click', '.delete_cupcake', async function(e) {
    e.preventDefault();
    const id = $(this).data('id');
    await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().remove()

})
