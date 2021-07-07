//const frappe = require('frappejs');
//Read from ../translations/pt.csv
const frappelerficheiro = require('fs'); // require('frappejs/server/utils'); //HELKYD 26-03-2021
const fs = require('fs');

function __(txt, replace) {
  //Carregar o file das traducoes...
  //Vendo que ja carregou no Server POSTSTART e no Transaction... NO NEED TO DO AGAIN...

  if (!frappe._traducao) {
    frappe._messages = {};
    //console.log(frappelerficheiro.readFile('./fixtures/verified/pt.csv'));
    //Verifica se consegue abrir o pt.csv ou le from TEMP if windows app
    const traducaofile = './fixtures/verified/pt.csv';
    console.log('Dir da APP ', process.env.PORTABLE_EXECUTABLE_DIR);
    if (fs.existsSync(traducaofile, 'utf-8')) {
      frappe._messages = frappelerficheiro.readFile(traducaofile);
    } else if (fs.existsSync('c://temp//pt.csv', 'utf-8')) {
      frappe._messages = frappelerficheiro.readFile('c://temp//pt.csv');
    }

    if (!frappe._messages) {
      return txt;
    }
    //frappe._messages = frappelerficheiro.readFile('./fixtures/verified/pt.csv');
    //console.log(frappe._messages.replace(/\n/g, "::").split('::'));

    //console.log(frappe._messages.replace(/\n/g, "::").split('::')[8]);
    //for (var ff in frappe._messages){
    //  console.log(frappe._messages[ff]);
    //};

    //let tradu = JSON.parse(frappe._messages.replace(/\n/g,"").replace('""', '&quot;'));
    //let tradu = JSON.stringify(frappe._messages);
    //let tradu1 = JSON.parse(JSON.stringify(frappe._messages.replace('",',':')));
    let tradu2 = JSON.parse(
      JSON.stringify(frappe._messages.replace(/\n/g, '::').split('::'))
    );

    //convert "," to dict
    frappe._traducao = {};
    //let trad = '';
    for (var xx in tradu2) {
      //console.log('aaaa');
      //console.log(tradu2[xx]);
      //console.log(tradu2[xx] == "");

      if (tradu2[xx] !== '') {
        //console.log(tradu2[xx].indexOf('","'));
        if (tradu2[xx].indexOf('","') != -1) {
          //trad = tradu2[xx].split('","');
          frappe._traducao[tradu2[xx].split('","')[0]] = tradu2[xx].split(
            '","'
          )[1];
        } else {
          //trad = tradu2[xx].split(',');
          frappe._traducao[tradu2[xx].split(',')[0]] = tradu2[xx].split(',')[1];
        }
        //console.log(trad);
      } else {
        break;
      }
    }
  }

  //Somente traduz se for PT-PT

  //console.log(frappe.AccountingSettings.linguasistema);
  if (frappe.AccountingSettings) {
    //console.log('lingua ', frappe.AccountingSettings.linguasistema);
    if (frappe.AccountingSettings.linguasistema == 'EN') {
      console.log('para traduzir ', txt);
    }
    if (frappe.AccountingSettings.linguasistema != 'PT-PT') return txt;
  } else {
    let ficheirolingua = '';
    if (fs.existsSync('c://temp//lang.txt', 'utf-8')) {
      ficheirolingua = fs.readFileSync('c://temp//lang.txt', 'utf-8');
      //console.log('C ', ficheirolingua);
    } else if (fs.existsSync('/tmp/lang.txt', 'utf-8')) {
      ficheirolingua = fs.readFileSync('/tmp/lang.txt', 'utf-8');
      //console.log('U ', ficheirolingua);
    } else {
      console.log('frappe.db');
      console.log(frappe.db);
      if (frappe.db == undefined) {
        ficheirolingua = 'PT-PT';
      } else {
        let ficheirolang =
          frappe.db.dbPath.substring(0, frappe.db.dbPath.lastIndexOf('/')) +
          '/lang.txt';
        if (fs.existsSync(ficheirolang, 'utf-8')) {
          ficheirolingua = fs.readFileSync(ficheirolang, 'utf-8');
          console.log(ficheirolingua);
        }
      }
    }
    //if (ficheirolingua == 'EN') {
    //  console.log('para traduzir ', txt);
    //} else if (ficheirolingua != 'PT-PT') {
    if (ficheirolingua != 'PT-PT') {
      return txt;
    }
  }
  //if (frappe.AccountingSettings.linguasistema != 'PT-PT') return txt;
  //console.log('frappe._traducao ', frappe._traducao);

  if (!txt) return txt;
  if (typeof txt != 'string') return txt;
  var ret = frappe._traducao[txt.replace(/\n/g, '')] || txt;
  if (replace && typeof replace === 'object') {
    //ret = $.format(ret, replace);
    console.log('por verificar');
  }
  console.log('traducaao ', ret);
  return ret;
}

function _t(txt, replace) {
  //Carregar o file das traducoes...
  console.log('Carregar o file das traducoes...');
  frappe._messages = {};
  //console.log(frappelerficheiro.readFile('./fixtures/verified/pt.csv'));
  frappe._messages = frappelerficheiro.readFile('../translations/pt.csv');
  //console.log(frappe._messages.replace(/\n/g, "::").split('::'));

  //console.log(frappe._messages.replace(/\n/g, "::").split('::')[8]);
  //for (var ff in frappe._messages){
  //  console.log(frappe._messages[ff]);
  //};

  //let tradu = JSON.parse(frappe._messages.replace(/\n/g,"").replace('""', '&quot;'));
  //let tradu = JSON.stringify(frappe._messages);
  //let tradu1 = JSON.parse(JSON.stringify(frappe._messages.replace('",',':')));
  let tradu2 = JSON.parse(
    JSON.stringify(frappe._messages.replace(/\n/g, '::').split('::'))
  );

  //convert "," to dict
  frappe._traducao = {};
  //let trad = '';
  for (var xx in tradu2) {
    //console.log('aaaa');
    //console.log(tradu2[xx]);
    //console.log(tradu2[xx] == "");

    if (tradu2[xx] !== '') {
      //console.log(tradu2[xx].indexOf('","'));
      if (tradu2[xx].indexOf('","') != -1) {
        //trad = tradu2[xx].split('","');
        frappe._traducao[tradu2[xx].split('","')[0]] = tradu2[xx].split(
          '","'
        )[1];
      } else {
        //trad = tradu2[xx].split(',');
        frappe._traducao[tradu2[xx].split(',')[0]] = tradu2[xx].split(',')[1];
      }
      //console.log(trad);
    } else {
      break;
    }
  }
  //console.log('frappe traducao');
  //console.log(frappe._traducao);

  if (!txt) return txt;
  if (typeof txt != 'string') return txt;
  var ret = frappe._traducao[txt.replace(/\n/g, '')] || txt;
  if (replace && typeof replace === 'object') {
    //ret = $.format(ret, replace);
    console.log('por verificar');
  }
  console.log('Traduzido para');
  console.log(ret);

  return ret;
}

module.exports = {
  __,
  _t
};