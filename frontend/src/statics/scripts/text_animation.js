// init
printText( document.getElementById( 'my-text' ) );

function printText( el ){

  let letterTimeout =  30

  let text = el.innerHTML
  let i = 1

  print__fn() // init

  function print__fn(){

    if( i <= text.length){
      el.innerHTML = text.substr( 0, i );
      setTimeout( arguments.callee, letterTimeout );
    }

    i++;
  }

}