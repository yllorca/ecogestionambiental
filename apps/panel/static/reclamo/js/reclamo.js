$(document).ready(function(){

    //form-edit-datos-reclamo
    $('#div-errores').hide();

    $("#form-edit-reclamo").on("submit", function(){
        let csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $('#btn-form-edit-reclamo').html('Guardando...');
        $.ajax({
            url: $("#form-edit-reclamo").attr('data-url'),
            type: 'POST',
            data: $("#form-edit-reclamo").serialize(),
            headers:{
                "X-CSRFToken": csrftoken
            },
            success:function(data){
                if(data.respuesta=='ok'){
                    $('#btn-form-edit-reclamo').html('Guardado');
                    $('#modal_reclamo').hide();
                    location.reload();
                    $('#div-errores').hide();
                }
                else{//data.respuesta=='error'
                    $('#id_error').html('');
                    $('#id_error').html(data.mensaje);
                    $('#btn-form-edit-reclamo').html('Guardado');
                    $('#div-errores').show();
                }
            }
        });
        return false;
    });

    $("#form-respuesta-reclamo").on("submit", function(){
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $('#btn-form-respuesta-reclamo').html('Guardando...');
    $.ajax({
      url: $("#form-respuesta-reclamo").attr('data-url'),
      type: 'POST',
      data: $("#form-respuesta-reclamo").serialize(),
      headers:{
        "X-CSRFToken": csrftoken
      },
      success:function(data){
        if(data.respuesta=='ok'){
          $('#btn-form-respuesta-reclamo').html('Guardado');
          $('#modal_respuesta').hide();
          location.reload();
          $('#div-errores').hide();
        }
        else{//data.respuesta=='error'
          $('#id_error').html('');
          $('#id_error').html(data.mensaje);
          $('#btn-form-respuesta-reclamo').html('Guardado');
          $('#div-errores').show();
        }
      }
    });
    return false;
  });

});