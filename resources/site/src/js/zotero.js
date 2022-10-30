function ZoteroManager(levels, meta, isView) {
    this.levels = levels;
    this.meta = meta;
    this.isView = isView;

    // create the metadata table, which is the key/value pairs given from a zotero
    // collection (sub folder) or attachment
    function createMetaTable(meta) {
	var tbl = document.createElement('table');
	var tbdy = document.createElement('tbody');
	var thead = document.createElement('thead');
	var tr = document.createElement('tr');
	var mlen = meta.length;

	tbl.classList.add('table');
	tbl.classList.add('meta-table');
	tbl.classList.add('border');
	thead.classList.add('meta-thead');

	var th = document.createElement('th');
	th.appendChild(document.createTextNode('Description'));
	tr.appendChild(th);

	th = document.createElement('th');
	th.appendChild(document.createTextNode('Value'));
	tr.appendChild(th);
	thead.appendChild(tr);

	// add metadata key/value pairs as rows in the table
	for (var i = 0; i < mlen; i++) {
            var td = document.createElement('td');
	    var tval = document.createElement('div');
	    var key = meta[i][0];
	    var val = meta[i][1];

            tr = document.createElement('tr');

            td.appendChild(document.createTextNode(key));
	    td.classList.add('meta-table-key');
            tr.appendChild(td)

            td = document.createElement('td');
	    td.appendChild(tval);
	    if (key == 'URL') {
		var anch = document.createElement('a');
		anch.setAttribute('href', val);
		anch.appendChild(document.createTextNode(anch));
		tval.appendChild(anch);
	    } else {
		tval.appendChild(document.createTextNode(val));
	    }
	    tval.classList.add('meta-table-val');
	    td.appendChild(tval);

            tr.appendChild(td)
            tbdy.appendChild(tr);
	}

	tbl.appendChild(thead);
	tbl.appendChild(tbdy);

	return tbl;
    }

    // create the header pane containing title of attachment, collection or note
    // params:
    // node: the node currently selected in the left nav
    // root: root element to append to, which is the table td element from the main
    // table
    function headerPane(node, root) {
	var topPanel = document.createElement('div');
	var head = document.createElement('h1');
	var btn = document.createElement('button');
	var topElem;

	root.classList.add('max-cell');

	// title of content at top
	head.classList.add('bd-title')
	head.appendChild(document.createTextNode(node.item_title));

	// header element
	topElem = document.createElement('div');
	topElem.appendChild(head);
	topElem.classList.add('nav-item');
	topPanel.appendChild(topElem);

	// view/download button
	btn.classList.add('btn');
	btn.classList.add('btn-primary');
	btn.classList.add('btn-sm');
	btn.classList.add('content-head-pane-btn');
	btn.setAttribute('type', 'button');
	btn.id = "view-button";
	btn.appendChild(document.createTextNode('View'));
	topElem = document.createElement('div');
	topElem.appendChild(btn);
	topElem.classList.add('nav-item');
	topPanel.appendChild(topElem);

	// header element
	topPanel.classList.add('d-flex');
	topPanel.classList.add('justify-content-between');
	topPanel.classList.add('content-head-pane');

	// add the pdf/html attachemnt if it exists, otherwise direct the user
	// via; add tool tip if no attachement
	btn.action = node.resource;
	if (node.resource) {
	    btn.onClick = node.resource;
	    btn.setAttribute('onClick', "location.href='" +
			     node.resource + "'");
	} else {
	    btn.classList.add('disabled');
	    btn.setAttribute('data-toggle', 'tooltip');
	    btn.setAttribute('data-placement', 'left');
	    btn.setAttribute('data-html', 'true');
	    btn.setAttribute('title', 'Not an attachment,<br/>try child node');
	    // there's got to be a better way...
	    $(function () {
    		$('[data-toggle="tooltip"]').tooltip()
	    });
	}

	root.appendChild(topPanel);
    }

    // populate the link button and update main screen link
    function updateLink(node) {
	var itemDocLinkButton = document.getElementById(
	    "item-document-link-button");
	var link = null;
	if (node) {
	    link = createDocumentLink(node);
	}
	if (link) {
	    itemDocLinkButton.setAttribute('data-original-title', link);
	    itemDocLinkButton.classList.remove('disabled');
	} else {
	    itemDocLinkButton.removeAttribute('data-original-title');
	    itemDocLinkButton.classList.add('disabled');
	}
    }

    // create a link that points to the current document
    function createDocumentLink(node) {
	type = 'item';
	if (node['node_type'] == 'item') {
	    var link;
	    if (type == 'doc') {
		var link = document.location.href;
		var idx = link.lastIndexOf('/');
		link = link.substring(0, idx);
		link = link + '/' + node.resource;
	    } else {
		var proto = window.location.protocol;
		var host = window.location.host;
		var path = window.location.pathname;
		link = proto + "//" + host + path + '?id=' + node['item-id'];
	    }
	    return link;
	}
    }

    // show an alert message on the screen for 2s
    function showAlert(message, subMessage, type) {
	var alertClass = 'alert-' + type;
	$("#alert-box").html('<strong>' + message + '</strong>: ' + subMessage);
	$("#alert-box").removeClass(alertClass).addClass(alertClass);
	$('#alert-box').slideDown("fast");
	setTimeout(function() {
	    $('#alert-box').slideUp("fast");
	}, 2000);
    }

    // when clicking the link button to copy the link
    function itemDocLinkClicked(node) {
	console.log('item document link clicked: ' + node);
	link = createDocumentLink(node);
	if (link) {
	    console.log('copying link : ' + link);
	    setClipboardText(link);
	    linkButton = document.getElementById("item-document-link-button");
	    showAlert('Link copied', link, 'success');
	}
    }

    // create the table with the collection information of children paper node
    function createCollectionTable(node) {
	function createTable(cols, rows) {
	    var tab = document.createElement('table');
	    var thead = document.createElement('thead');
	    var tbody = document.createElement('tbody');
	    var tr = document.createElement('tr');
	    var tabItemToJs = mapItemToJs();

	    function addHeaderCols(cols) {
		for (var i = 0; i < cols.length; i++) {
		    var th = document.createElement('th');
		    th.appendChild(document.createTextNode(cols[i]));
		    tr.appendChild(th);
		}
	    }

	    function addRow(cells) {
		var tr = document.createElement('tr');
		for (var i = 0; i < cells.length; i++) {
		    var cell = cells[i];
		    var itemId = cell[0];
		    var cellText = cell[1];
		    var td = document.createElement('td');
		    var tnode = document.createTextNode(cellText);
		    td.classList.add(['word-wrap', 'break-word', 'meta-table-val']);
		    tr.appendChild(td);
		    if (i == 0) {
			var link = document.createElement('a');
			link.href = itemId;
			link.onclick = function(e) {
			    e.preventDefault();
			    showItem(itemId, tabItemToJs);
			}
			link.appendChild(tnode);
			td.appendChild(link);
		    } else {
			td.appendChild(tnode);
		    }
		}
		tbody.appendChild(tr);
	    }	    

	    tab.id = 'collections-table';
	    tab.cellspaceing = 0;
	    tab.width = '100%';
	    thead.classList.add('meta-thead');
	    tab.appendChild(thead);
	    tab.appendChild(tbody);
	    thead.appendChild(tr);

	    addHeaderCols(cols);
	    for (var rix = 0; rix < rows.length; rix++) {
		addRow(rows[rix]);
	    }
	    return tab;
	}

	var cols = ['Title', 'Creators', 'Date'];
	var childs = node.nodes;
	var rows = [];
	var tab = null;

	for (var i = 0; i < childs.length; i++) {
	    var c = childs[i];
	    var meta = c.metadata;
	    if (meta != null) {
		var metaByCol = {};
		var row = [];
		for (var mix = 0; mix < meta.length; mix++) {
		    var mpair = meta[mix];
		    metaByCol[mpair[0]] = mpair[1];
		}
		for (var cix = 0; cix < cols.length; cix++) {
		    var col = cols[cix];
		    var cval = metaByCol[col];
		    if (cval == null) cval = '';
		    row.push([c['item-id'], cval]);
		}
		rows.push(row);
	    }
	}

	if (rows.length > 0) tab = createTable(cols, rows);
	return tab
    }

    // create the main (right) content pane in the main top level table
    // params:
    // node: the node currently selected in the left nav
    function createMain(node) {
	console.log('create main: ' + node);
	var cont = document.getElementById("zotero-main-content");

	while (cont.firstChild) {
	    cont.removeChild(cont.firstChild);
	}

	if (node) {
	    var meta = node.metadata;
	    var sel = node.state.selected;
	    var nodeType;
	    var hasContent;

	    // determine the type of node in the tree we're visiting
	    if (node.item_type == 'attachment') {
		nodeType = 'attachment';
	    } else if (node.item_type == 'note') {
		nodeType = 'note';
	    } else if (meta != null) {
		nodeType = 'meta';
	    }
	    hasNote = ((nodeType == 'note') && sel);
	    hasContent = (((nodeType == 'attachment') && sel) ||
			  (nodeType == 'meta'));

	    cont.className = '';
	} else {
	    hasContent = false;
	    hasNote = false;
	    nodeType = null;
	}

	var initCollectionsTable = false;
	// add the header pane
	if (hasContent) {
	    headerPane(node, cont);
	} else if (!hasNote) {
	    // add collection table if we find the metadata level node;
	    // otherwise give the "No Content" message
	    var noc = document.createElement('div');
	    var ctab = createCollectionTable(node);
	    if (ctab != null) {
		console.log('adding collection table');
		var root = document.createElement('div');
		var title = document.createElement('div');
		var header = document.createElement('h1');
		header.classList.add('bd-title');
		header.appendChild(document.createTextNode(node.item_title));
		root.classList.add('nav-item');
		ctab.classList.add('table', 'border', 'meta-table');
		title.appendChild(header);
		root.appendChild(title);
		root.appendChild(ctab);
		noc.appendChild(root);
		initCollectionsTable = true;
	    } else {
		console.log('no data collection data found');
		cont.classList.add('center-cell');
		noc.classList.add('disabled-text');
		noc.appendChild(document.createTextNode('No Content'));
	    }
	    cont.appendChild(noc);
	}

	if (initCollectionsTable) {
	    if (!$.fn.DataTable.isDataTable('#collections-table')) {
		$('#collections-table').DataTable({
		    // https://datatables.net/examples/basic_init/dom.html
		    dom: '<tp>',
		    'pageLength': 50,
		});
	    }
	}

	// add metadata if there is any
	if (meta &&
	    (((nodeType == 'attachment') && sel) || !(nodeType == 'attachment'))) {
	    var metaTable = createMetaTable(meta);
	    cont.appendChild(metaTable);
	}

	// add notes if there are any
	if (hasNote) {
	    console.log('adding note: ' + node.resource);
	    var card = document.createElement('div');
	    var cardBlock = document.createElement('div');
	    var h = document.createElement('h3');

	    card.classList.add('card');
	    card.classList.add('center-pane');
	    card.classList.add('note-pane');

	    h.classList.add('card-header');
	    h.appendChild(document.createTextNode(node.item_title));
	    card.appendChild(h);

	    cardBlock.classList.add('card-block');
	    var p = document.createElement('p');
	    p.classList.add('card-text');
	    var divElem = document.createElement('div');
	    var text = node.item_note;
	    divElem.innerHTML = text;
	    p.appendChild(divElem);
	    cardBlock.appendChild(p);
	    card.appendChild(cardBlock);

	    cont.classList.add('content-note');
	    cont.appendChild(card);
	}

	// add the (usually PDF orsnapshot site) attachemnt
	if ((nodeType == 'attachment') && sel) {
	    console.log('adding resource: ' + node.resource);
	    var aelem = document.createElement('div');
	    if (node.resource.endsWith('.html')) {
		$.ajax({
		    url: node.resource,
		    type: 'GET',
		    dataType: 'html',
		    success: function(data) {              
			aelem.innerHTML = data;
		    }});
	    } else {
		var objElem = document.createElement('object');

		aelem.classList.add('embed-responsive');
		aelem.classList.add('border');
		aelem.classList.add('rounded');
		aelem.classList.add('pdf-pane');

		objElem.setAttribute('data', node.resource);
		objElem.setAttribute('type', 'application/pdf');
		objElem.appendChild(document.createTextNode('No PDF plugin'));

		aelem.appendChild(objElem);
	    }
	    cont.appendChild(aelem);
	}

	updateLink(node);
    }

    // called when the user types in the search box and narrows the tree search
    function onSearchChange(text) {
	console.log('search updated: ' + text);
	var tree = $('#tree').treeview(true);
	if (text.length == 0) {
	    tree.clearSearch();
	} else {
	    var options = {ignoreCase: true,
			   exactMatch: false,
			   revealResults: true}
	    nodes = tree.search(text, options);
	}
    }

    // map item zotero IDs to tree node IDs
    function mapItemToJsNodes(itemToJs, nodes) {
	for (var i = 0; i < nodes.length; i++) {
	    node = nodes[i]
	    key = node['item-id'];
	    itemToJs[key] = node.nodeId;
	    if (typeof node.nodes != 'undefined') {
		mapItemToJsNodes(itemToJs, node.nodes);
	    }
	}
	return itemToJs;
    }

    function mapItemToJs() {
	var tree = $('#tree').treeview(true);
	var itemToJs = {};
	var sibs = tree.getSiblings(0);
	mapItemToJsNodes(itemToJs, [tree.getNode(0)]);
	mapItemToJsNodes(itemToJs, tree.getSiblings(0));
	return itemToJs;
    }

    function showItem(itemId, itemToJs) {
	console.log('show item by id: ' + itemId);
	var tree = $('#tree').treeview(true);
	if (itemToJs[itemId] == undefined) {
	    console.log(' no such item ID: ' + itemId);
	} else {
	    var nodeId = itemToJs[itemId];
	    tree.revealNode(nodeId);
	    tree.selectNode(nodeId);
	}
    }

    // show the nodes given by the search and hidw all others
    // used when the user uses the search button or presses enter
    function searchNarrow() {
	var tree = $('#tree').treeview(true);
	var field = document.getElementById("termSearch");
	var text = field.value;

	if (text.length > 0) {
	    console.log('searching on text: ' + text);
	    var options = {ignoreCase: true,
			   exactMatch: false,
			   revealResults: false}
	    var nodes = tree.getExpanded();
	    var nlen = nodes.length;
	    for (var i = 0; i < nlen; i++) {
		var node = nodes[i];
		console.log('collapsing: ' + node);
		tree.collapseNode(node.nodeId, {levels: 1});
	    }
	    nodes = tree.search(text, options);
	    nlen = nodes.length;
	    tree.collapseAll({silent: true});
	    for (var i = 0; i < nlen; i++) {
		var node = nodes[i];
		console.log('expanding (' + node.nodeId + '), ' + node.text);
		tree.revealNode(node.nodeId, {levels: 1});
	    }

	    if (nlen == 1) {
		tree.selectNode(node.nodeId);
	    }
	}
    }

    function updateMain(event, node) {
	console.log('updating: ' + node.nodeId + '( ' + node['item-id'] + ')');
	console.log(node);
	createMain(node);
	lastNode = node;
    }

    function insertVersion() {
	var verTextElem = $('#project-link-version a');
	var verAnch = $('#project-link-version a')[0];
	var verText = 'v' + meta.version;
	verAnch.href = verAnch.href + verText;
	verTextElem.text(verText);
    }

    this.reset = function() {
	console.log('resetting');
	var tree = $('#tree').treeview(true);
	tree.collapseAll();
	createMain(null);
	updateLink(null);
	lastNode = null;
    }

    // initialization called on page load
    this.init = function(itemId) {
	console.log('version: ' + meta.version);

	$('#tree').treeview({
	    data: tree,
	    levels: levels,
	    onNodeSelected: updateMain,
	    onNodeUnselected: updateMain,
	    onNodeExpanded: updateMain,
	    onNodeCollapsed: updateMain,
	    nodeDisabled: updateMain,
	    nodeEnabled: updateMain,
	});

	$('#termSearch').on('keyup', function(e) {
	    if (e.keyCode == 13) {
		searchNarrow();
	    } else {
		onSearchChange(this.value);
	    }
	});

	$('#item-document-link-button').click(function() {
	    if (typeof lastNode != 'undefined') {
		itemDocLinkClicked(lastNode);
	    }
	});

	linkButton = document.getElementById("item-document-link-button");
	btn = linkButton;
	btn.setAttribute('link-data-toggle', 'tooltip');
	btn.setAttribute('link-data-placement', 'right');
	btn.setAttribute('link-data-html', 'true');
	$(function () {
	    $('[link-data-toggle="tooltip"]').tooltip()
	});

	insertVersion();

	var itemToJs = mapItemToJs()
	console.log(itemToJs);
	if (itemId) {
	    showItem(itemId, itemToJs);
	}

	console.log('isView: ' + isView);
	if (isView) {
	    $('#view-button').click();
	}
    }
}
