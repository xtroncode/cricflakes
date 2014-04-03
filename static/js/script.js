$(document).ready(
      function(){
        var updatepage =function(){ 
          
          $.getJSON($SCRIPT_ROOT + '/_get_scores',function(data){
          //var matches=data.mchdata.match
          $('ul.grid').html("<li class='card'></li>");
           
          $.each(data.details,function(index,element){
            $('ul.grid').append(element);
            
          });
        });
                                  };
      updatepage();
      setInterval(updatepage,5000)
        
      });