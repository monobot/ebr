const csrftoken_name = 'csrftoken'
const rootUrl = 'http://localhost/api/'

function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {

    if(response.status === 204)
      return {data: null, success: true}

    return response.json().then((data) => {
      return {data: data, success: true, status: response.status}
    })
  } else {
    return response.json().then((data) => {
    return {data: data, success: false, status: response.status}
    })
  }
}

const apicall = {
  get: (endpoint) => {
    return fetch(rootUrl + endpoint, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie(csrftoken_name),
      },
      credentials: 'include',
    })
    .then(checkStatus)
    .catch((error) => {console.log(error)})
  },

  post: (endpoint, payload) => {
    return fetch(rootUrl + endpoint, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie(csrftoken_name),
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    .then(checkStatus)
    .catch((error) => {console.log(error)})
  },

  put: (endpoint, payload) => {
    return fetch(rootUrl + endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie(csrftoken_name),
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    .then(checkStatus)
    .catch((error) => {console.log(error)})
  },

  patch: (endpoint, payload) => {
    return fetch(rootUrl + endpoint, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie(csrftoken_name),
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    .then(checkStatus)
    .catch((error) => {console.log(error)})
  },

  delete: (endpoint) => {
    return fetch(rootUrl + endpoint, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie(csrftoken_name),
      },
      credentials: 'include'
    })
    .then(checkStatus)
    .catch((error) => {console.log(error)})
  },
}

const external_api = {
  get: (endpoint) => {
    return fetch(endpoint, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie(csrftoken_name),
      },
    })
      .then(checkStatus)
      .catch((error) => {console.log(error)})
  },
}

function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const cookie = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (cookie.length === 0) {
    return null;
  }

  return decodeURIComponent(cookie[0].split('=')[1]);
};

const vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    trades: [],
    formstatus: 'hidden',
    sell_currency: '',
    sell_amount: 0,
    rate: 'pending',
    buy_currency: '',
    buy_amount: 0,
    currencies: [
      { text: '[EUR] Euro', value: 'EUR'},
      { text: '[USD] United States Dollar', value: 'USD'},
      { text: '[GBP] United Kingdom Pound', value: 'GBP'},
      { text: '[AUD] Australia Dollar', value: 'AUD'},
      { text: '[BGN] Bulgaria Lev', value: 'BGN'},
      { text: '[BRL] Brazil Real', value: 'BRL'},
      { text: '[CAD] Canada Dollar', value: 'CAD'},
      { text: '[CHF] Switzerland Franc', value: 'CHF'},
      { text: '[CNY] China Yuan Renminbi', value: 'CNY'},
      { text: '[CZK] Czech Republic Koruna', value: 'CZK'},
      { text: '[DKK] Denmark Krone', value: 'DKK'},
      { text: '[HKD] Hong Kong Dollar', value: 'HKD'},
      { text: '[HRK] Croatia Kuna', value: 'HRK'},
      { text: '[HUF] Hungary Forint', value: 'HUF'},
      { text: '[IDR] Indonesia Rupiah', value: 'IDR'},
      { text: '[ILS] Israel Shekel', value: 'ILS'},
      { text: '[INR] India Rupee', value: 'INR'},
      { text: '[JPY] Japan Yen', value: 'JPY'},
      { text: '[KRW] Korea (South) Won', value: 'KRW'},
      { text: '[MXN] Mexico Peso', value: 'MXN'},
      { text: '[MYR] Malaysia Ringgit', value: 'MYR'},
      { text: '[NOK] Norway Krone', value: 'NOK'},
      { text: '[NZD] New Zealand Dollar', value: 'NZD'},
      { text: '[PHP] Philippines Peso', value: 'PHP'},
      { text: '[PLN] Poland Zloty', value: 'PLN'},
      { text: '[RON] Romania New Leu', value: 'RON'},
      { text: '[RUB] Russia Ruble', value: 'RUB'},
      { text: '[SEK] Sweden Krona', value: 'SEK'},
      { text: '[SGD] Singapore Dollar', value: 'SGD'},
      { text: '[THB] Thailand Baht', value: 'THB'},
      { text: '[TRY] Turkey Lira', value: 'TRY'},
      { text: '[ZAR] South Africa Rand', value: 'ZAR'},
    ]
  },

  mounted() {
    apicall.get('trades/')
      .then(response => {this.trades = response.data})
  },

  methods: {
    formtoggle: function (event) {
      // `this` inside methods points to the Vue instance
      if (this.formstatus === 'show') {
        this.formstatus = 'hidden'
      } else {
        this.formstatus = 'show'
      }
    },

    calc_buyamount: function() {
      if (this.rate == 'pending' || this.sell_amount == 0) {
        this.buy_amount = 'pending'
        return
      };
      this.buy_amount = this.rate * this.sell_amount;
    },

    get_rate: function() {
      if (this.sell_currency == '' || this.buy_currency == '') {
        this.rate = 'pending'
        return
      };
      this.rate = exchanges_cache[this.sell_currency][this.buy_currency];

      url = 'http://api.fixer.io/latest?base=' + this.sell_currency + '&symbols=' + this.buy_currency

      external_api.get(url).then(result => {
        this.rate = result.data['rates'][this.buy_currency]
      })
      this.calc_buyamount()
    },

    clear_form: function() {
      this.sell_currency = ''
      this.buy_currency = ''
      this.rate = 'pending'
      this.buy_amount = 0
      this.sell_amount = 0
    },

    place_trade: function() {
      if (this.buy_amount == 0 || this.buy_amount == 'pending') {
        return
      }

      let url = 'trades/'
      let data = {
        'sell_currency': this.sell_currency,
        'buy_currency': this.buy_currency,
        'sell_amount': this.sell_amount,
      }

      apicall.post(url, data).then((response) => {
        if(!response.success) {
          console.log('error creating trade')
          return
        }
        console.log(response.data)
        this.trades.push(response.data)
      })

      this.clear_form()
      this.formtoggle()
    }

  }
})
