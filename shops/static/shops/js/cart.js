var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action

		addCookieItem(productId, action)
	})
}

function addCookieItem(productId, action){
	if (action == 'add'){
		if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}
	
		}else{
			cart[productId]['quantity'] += 1
		}
	}
	else if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			delete cart[productId];
		}
	}
	else if (action == 'delete'){
		cart[productId]['quantity'] = 0

		if (cart[productId]['quantity'] <= 0){
			delete cart[productId];
		}

	}
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}