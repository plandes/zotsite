function ZoteroManager(levels, meta) {
    this.levels = levels;
    this.meta = meta;

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
	    if (key == 'url') {
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
	btn.appendChild(document.createTextNode('View'));
	topElem = document.createElement('div');
	topElem.appendChild(btn);
	topElem.classList.add('nav-item');
	topPanel.appendChild(topElem);

	// header element
	topPanel.classList.add('d-flex');
	topPanel.classList.add('justify-content-between');
	topPanel.classList.add('content-head-pane');

	// add the pdf/html attachemnt if it exists, otherwise direct the user via
	// add tool tip if no attachement
	btn.action = node.resource;
	if (!node.resource) {
	    btn.classList.add('disabled');
	    btn.setAttribute('data-toggle', 'tooltip');
	    btn.setAttribute('data-placement', 'left');
	    btn.setAttribute('data-html', 'true');
	    btn.setAttribute('title', 'Not an attachment,<br/>try child node');
	    // there's got to be a better way...
	    $(function () {
    		$('[data-toggle="tooltip"]').tooltip()
	    })
	} else {
	    btn.onClick = node.resource;
	    btn.setAttribute('onClick', "location.href='" + node.resource + "'");
	}

	root.appendChild(topPanel);
    }

    // create the main (right) content pane in the main top level table
    // params:
    // node: the node currently selected in the left nav
    function createMain(node) {
	var meta = node.metadata;
	var cont = document.getElementById("zotero-main-content");
	var sel = node.state.selected;
	var nodeType;
	var hasContent;

	console.log('node: ' + node.text);

	// determine the type of node in the tree we're visiting
	if (node.resource != null) {
	    nodeType = 'attachment';
	} else if (node.item_type == 'note') {
	    nodeType = 'note';
	} else if (meta != null) {
	    nodeType = 'meta';
	}
	hasNote = ((nodeType == 'note') && sel);
	hasContent = (((nodeType == 'attachment') && sel) ||
		      (nodeType == 'meta'));

	while (cont.firstChild) {
	    cont.removeChild(cont.firstChild);
	}
	cont.className = '';

	// add the header pane
	if (hasContent) {
	    headerPane(node, cont);
	} else if (!hasNote) {
	    var noc = document.createElement('div');

	    cont.classList.add('center-cell');
	    noc.classList.add('disabled-text');
	    noc.appendChild(document.createTextNode('No Content'));
	    cont.appendChild(noc);
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
	    var objElem = document.createElement('object');

	    aelem.classList.add('embed-responsive');
	    aelem.classList.add('border');
	    aelem.classList.add('rounded');
	    aelem.classList.add('pdf-pane');

	    objElem.setAttribute('data', node.resource);
	    objElem.setAttribute('type', 'application/pdf');
	    objElem.appendChild(document.createTextNode('No PDF plugin'));

	    aelem.appendChild(objElem);
	    cont.appendChild(aelem);
	}
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

    // show the nodes given by the search and hid all others
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
	createMain(node);
    }

    function insertVersion() {
	var verTextElem = $('#project-text-version a');
	var verAnch = $('#project-link-version a')[0];
	var verText = 'v' + meta.version;
	verAnch.href = verAnch.href + verText;
	verTextElem.text(verText);
    }

    // initialization called on page load
    this.init = function() {
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

	$(function () {
	    $('[data-toggle="tooltip"]').tooltip()
	})

	insertVersion();
    }
}

window.onload = function() {
    var url = new URL(window.location.href);
    var treeLevels = url.searchParams.get('levels') || 1;
    var zot = new ZoteroManager(treeLevels, zoteroMeta);
    zot.init();
}
