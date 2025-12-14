/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const N = globalThis, q = N.ShadowRoot && (N.ShadyCSS === void 0 || N.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Z = Symbol(), J = /* @__PURE__ */ new WeakMap();
let oe = class {
  constructor(e, t, i) {
    if (this._$cssResult$ = !0, i !== Z) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = e, this.t = t;
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (q && e === void 0) {
      const i = t !== void 0 && t.length === 1;
      i && (e = J.get(t)), e === void 0 && ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText), i && J.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const pe = (s) => new oe(typeof s == "string" ? s : s + "", void 0, Z), ue = (s, ...e) => {
  const t = s.length === 1 ? s[0] : e.reduce((i, r, a) => i + ((n) => {
    if (n._$cssResult$ === !0) return n.cssText;
    if (typeof n == "number") return n;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + n + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(r) + s[a + 1], s[0]);
  return new oe(t, s, Z);
}, ge = (s, e) => {
  if (q) s.adoptedStyleSheets = e.map((t) => t instanceof CSSStyleSheet ? t : t.styleSheet);
  else for (const t of e) {
    const i = document.createElement("style"), r = N.litNonce;
    r !== void 0 && i.setAttribute("nonce", r), i.textContent = t.cssText, s.appendChild(i);
  }
}, Q = q ? (s) => s : (s) => s instanceof CSSStyleSheet ? ((e) => {
  let t = "";
  for (const i of e.cssRules) t += i.cssText;
  return pe(t);
})(s) : s;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { is: ve, defineProperty: _e, getOwnPropertyDescriptor: me, getOwnPropertyNames: $e, getOwnPropertySymbols: fe, getPrototypeOf: ye } = Object, y = globalThis, X = y.trustedTypes, we = X ? X.emptyScript : "", D = y.reactiveElementPolyfillSupport, V = (s, e) => s, W = { toAttribute(s, e) {
  switch (e) {
    case Boolean:
      s = s ? we : null;
      break;
    case Object:
    case Array:
      s = s == null ? s : JSON.stringify(s);
  }
  return s;
}, fromAttribute(s, e) {
  let t = s;
  switch (e) {
    case Boolean:
      t = s !== null;
      break;
    case Number:
      t = s === null ? null : Number(s);
      break;
    case Object:
    case Array:
      try {
        t = JSON.parse(s);
      } catch {
        t = null;
      }
  }
  return t;
} }, G = (s, e) => !ve(s, e), Y = { attribute: !0, type: String, converter: W, reflect: !1, useDefault: !1, hasChanged: G };
Symbol.metadata ?? (Symbol.metadata = Symbol("metadata")), y.litPropertyMetadata ?? (y.litPropertyMetadata = /* @__PURE__ */ new WeakMap());
let E = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ?? (this.l = [])).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = Y) {
    if (t.state && (t.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(e) && ((t = Object.create(t)).wrapped = !0), this.elementProperties.set(e, t), !t.noAccessor) {
      const i = Symbol(), r = this.getPropertyDescriptor(e, i, t);
      r !== void 0 && _e(this.prototype, e, r);
    }
  }
  static getPropertyDescriptor(e, t, i) {
    const { get: r, set: a } = me(this.prototype, e) ?? { get() {
      return this[t];
    }, set(n) {
      this[t] = n;
    } };
    return { get: r, set(n) {
      const d = r == null ? void 0 : r.call(this);
      a == null || a.call(this, n), this.requestUpdate(e, d, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? Y;
  }
  static _$Ei() {
    if (this.hasOwnProperty(V("elementProperties"))) return;
    const e = ye(this);
    e.finalize(), e.l !== void 0 && (this.l = [...e.l]), this.elementProperties = new Map(e.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(V("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(V("properties"))) {
      const t = this.properties, i = [...$e(t), ...fe(t)];
      for (const r of i) this.createProperty(r, t[r]);
    }
    const e = this[Symbol.metadata];
    if (e !== null) {
      const t = litPropertyMetadata.get(e);
      if (t !== void 0) for (const [i, r] of t) this.elementProperties.set(i, r);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [t, i] of this.elementProperties) {
      const r = this._$Eu(t, i);
      r !== void 0 && this._$Eh.set(r, t);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(e) {
    const t = [];
    if (Array.isArray(e)) {
      const i = new Set(e.flat(1 / 0).reverse());
      for (const r of i) t.unshift(Q(r));
    } else e !== void 0 && t.push(Q(e));
    return t;
  }
  static _$Eu(e, t) {
    const i = t.attribute;
    return i === !1 ? void 0 : typeof i == "string" ? i : typeof e == "string" ? e.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    var e;
    this._$ES = new Promise((t) => this.enableUpdating = t), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), (e = this.constructor.l) == null || e.forEach((t) => t(this));
  }
  addController(e) {
    var t;
    (this._$EO ?? (this._$EO = /* @__PURE__ */ new Set())).add(e), this.renderRoot !== void 0 && this.isConnected && ((t = e.hostConnected) == null || t.call(e));
  }
  removeController(e) {
    var t;
    (t = this._$EO) == null || t.delete(e);
  }
  _$E_() {
    const e = /* @__PURE__ */ new Map(), t = this.constructor.elementProperties;
    for (const i of t.keys()) this.hasOwnProperty(i) && (e.set(i, this[i]), delete this[i]);
    e.size > 0 && (this._$Ep = e);
  }
  createRenderRoot() {
    const e = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return ge(e, this.constructor.elementStyles), e;
  }
  connectedCallback() {
    var e;
    this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (e = this._$EO) == null || e.forEach((t) => {
      var i;
      return (i = t.hostConnected) == null ? void 0 : i.call(t);
    });
  }
  enableUpdating(e) {
  }
  disconnectedCallback() {
    var e;
    (e = this._$EO) == null || e.forEach((t) => {
      var i;
      return (i = t.hostDisconnected) == null ? void 0 : i.call(t);
    });
  }
  attributeChangedCallback(e, t, i) {
    this._$AK(e, i);
  }
  _$ET(e, t) {
    var a;
    const i = this.constructor.elementProperties.get(e), r = this.constructor._$Eu(e, i);
    if (r !== void 0 && i.reflect === !0) {
      const n = (((a = i.converter) == null ? void 0 : a.toAttribute) !== void 0 ? i.converter : W).toAttribute(t, i.type);
      this._$Em = e, n == null ? this.removeAttribute(r) : this.setAttribute(r, n), this._$Em = null;
    }
  }
  _$AK(e, t) {
    var a, n;
    const i = this.constructor, r = i._$Eh.get(e);
    if (r !== void 0 && this._$Em !== r) {
      const d = i.getPropertyOptions(r), o = typeof d.converter == "function" ? { fromAttribute: d.converter } : ((a = d.converter) == null ? void 0 : a.fromAttribute) !== void 0 ? d.converter : W;
      this._$Em = r;
      const c = o.fromAttribute(t, d.type);
      this[r] = c ?? ((n = this._$Ej) == null ? void 0 : n.get(r)) ?? c, this._$Em = null;
    }
  }
  requestUpdate(e, t, i) {
    var r;
    if (e !== void 0) {
      const a = this.constructor, n = this[e];
      if (i ?? (i = a.getPropertyOptions(e)), !((i.hasChanged ?? G)(n, t) || i.useDefault && i.reflect && n === ((r = this._$Ej) == null ? void 0 : r.get(e)) && !this.hasAttribute(a._$Eu(e, i)))) return;
      this.C(e, t, i);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: i, reflect: r, wrapped: a }, n) {
    i && !(this._$Ej ?? (this._$Ej = /* @__PURE__ */ new Map())).has(e) && (this._$Ej.set(e, n ?? t ?? this[e]), a !== !0 || n !== void 0) || (this._$AL.has(e) || (this.hasUpdated || i || (t = void 0), this._$AL.set(e, t)), r === !0 && this._$Em !== e && (this._$Eq ?? (this._$Eq = /* @__PURE__ */ new Set())).add(e));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (t) {
      Promise.reject(t);
    }
    const e = this.scheduleUpdate();
    return e != null && await e, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    var i;
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ?? (this.renderRoot = this.createRenderRoot()), this._$Ep) {
        for (const [a, n] of this._$Ep) this[a] = n;
        this._$Ep = void 0;
      }
      const r = this.constructor.elementProperties;
      if (r.size > 0) for (const [a, n] of r) {
        const { wrapped: d } = n, o = this[a];
        d !== !0 || this._$AL.has(a) || o === void 0 || this.C(a, void 0, n, o);
      }
    }
    let e = !1;
    const t = this._$AL;
    try {
      e = this.shouldUpdate(t), e ? (this.willUpdate(t), (i = this._$EO) == null || i.forEach((r) => {
        var a;
        return (a = r.hostUpdate) == null ? void 0 : a.call(r);
      }), this.update(t)) : this._$EM();
    } catch (r) {
      throw e = !1, this._$EM(), r;
    }
    e && this._$AE(t);
  }
  willUpdate(e) {
  }
  _$AE(e) {
    var t;
    (t = this._$EO) == null || t.forEach((i) => {
      var r;
      return (r = i.hostUpdated) == null ? void 0 : r.call(i);
    }), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(e)), this.updated(e);
  }
  _$EM() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(e) {
    return !0;
  }
  update(e) {
    this._$Eq && (this._$Eq = this._$Eq.forEach((t) => this._$ET(t, this[t]))), this._$EM();
  }
  updated(e) {
  }
  firstUpdated(e) {
  }
};
E.elementStyles = [], E.shadowRootOptions = { mode: "open" }, E[V("elementProperties")] = /* @__PURE__ */ new Map(), E[V("finalized")] = /* @__PURE__ */ new Map(), D == null || D({ ReactiveElement: E }), (y.reactiveElementVersions ?? (y.reactiveElementVersions = [])).push("2.1.1");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const O = globalThis, j = O.trustedTypes, ee = j ? j.createPolicy("lit-html", { createHTML: (s) => s }) : void 0, de = "$lit$", f = `lit$${Math.random().toFixed(9).slice(2)}$`, le = "?" + f, be = `<${le}>`, A = document, C = () => A.createComment(""), I = (s) => s === null || typeof s != "object" && typeof s != "function", K = Array.isArray, xe = (s) => K(s) || typeof (s == null ? void 0 : s[Symbol.iterator]) == "function", z = `[ 	
\f\r]`, S = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, te = /-->/g, ie = />/g, w = RegExp(`>|${z}(?:([^\\s"'>=/]+)(${z}*=${z}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), se = /'/g, re = /"/g, ce = /^(?:script|style|textarea|title)$/i, Ae = (s) => (e, ...t) => ({ _$litType$: s, strings: e, values: t }), l = Ae(1), P = Symbol.for("lit-noChange"), p = Symbol.for("lit-nothing"), ae = /* @__PURE__ */ new WeakMap(), b = A.createTreeWalker(A, 129);
function he(s, e) {
  if (!K(s) || !s.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return ee !== void 0 ? ee.createHTML(e) : e;
}
const Ee = (s, e) => {
  const t = s.length - 1, i = [];
  let r, a = e === 2 ? "<svg>" : e === 3 ? "<math>" : "", n = S;
  for (let d = 0; d < t; d++) {
    const o = s[d];
    let c, u, h = -1, m = 0;
    for (; m < o.length && (n.lastIndex = m, u = n.exec(o), u !== null); ) m = n.lastIndex, n === S ? u[1] === "!--" ? n = te : u[1] !== void 0 ? n = ie : u[2] !== void 0 ? (ce.test(u[2]) && (r = RegExp("</" + u[2], "g")), n = w) : u[3] !== void 0 && (n = w) : n === w ? u[0] === ">" ? (n = r ?? S, h = -1) : u[1] === void 0 ? h = -2 : (h = n.lastIndex - u[2].length, c = u[1], n = u[3] === void 0 ? w : u[3] === '"' ? re : se) : n === re || n === se ? n = w : n === te || n === ie ? n = S : (n = w, r = void 0);
    const $ = n === w && s[d + 1].startsWith("/>") ? " " : "";
    a += n === S ? o + be : h >= 0 ? (i.push(c), o.slice(0, h) + de + o.slice(h) + f + $) : o + f + (h === -2 ? d : $);
  }
  return [he(s, a + (s[t] || "<?>") + (e === 2 ? "</svg>" : e === 3 ? "</math>" : "")), i];
};
class H {
  constructor({ strings: e, _$litType$: t }, i) {
    let r;
    this.parts = [];
    let a = 0, n = 0;
    const d = e.length - 1, o = this.parts, [c, u] = Ee(e, t);
    if (this.el = H.createElement(c, i), b.currentNode = this.el.content, t === 2 || t === 3) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (r = b.nextNode()) !== null && o.length < d; ) {
      if (r.nodeType === 1) {
        if (r.hasAttributes()) for (const h of r.getAttributeNames()) if (h.endsWith(de)) {
          const m = u[n++], $ = r.getAttribute(h).split(f), T = /([.?@])?(.*)/.exec(m);
          o.push({ type: 1, index: a, name: T[2], strings: $, ctor: T[1] === "." ? ke : T[1] === "?" ? Se : T[1] === "@" ? Ve : R }), r.removeAttribute(h);
        } else h.startsWith(f) && (o.push({ type: 6, index: a }), r.removeAttribute(h));
        if (ce.test(r.tagName)) {
          const h = r.textContent.split(f), m = h.length - 1;
          if (m > 0) {
            r.textContent = j ? j.emptyScript : "";
            for (let $ = 0; $ < m; $++) r.append(h[$], C()), b.nextNode(), o.push({ type: 2, index: ++a });
            r.append(h[m], C());
          }
        }
      } else if (r.nodeType === 8) if (r.data === le) o.push({ type: 2, index: a });
      else {
        let h = -1;
        for (; (h = r.data.indexOf(f, h + 1)) !== -1; ) o.push({ type: 7, index: a }), h += f.length - 1;
      }
      a++;
    }
  }
  static createElement(e, t) {
    const i = A.createElement("template");
    return i.innerHTML = e, i;
  }
}
function k(s, e, t = s, i) {
  var n, d;
  if (e === P) return e;
  let r = i !== void 0 ? (n = t._$Co) == null ? void 0 : n[i] : t._$Cl;
  const a = I(e) ? void 0 : e._$litDirective$;
  return (r == null ? void 0 : r.constructor) !== a && ((d = r == null ? void 0 : r._$AO) == null || d.call(r, !1), a === void 0 ? r = void 0 : (r = new a(s), r._$AT(s, t, i)), i !== void 0 ? (t._$Co ?? (t._$Co = []))[i] = r : t._$Cl = r), r !== void 0 && (e = k(s, r._$AS(s, e.values), r, i)), e;
}
class Pe {
  constructor(e, t) {
    this._$AV = [], this._$AN = void 0, this._$AD = e, this._$AM = t;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(e) {
    const { el: { content: t }, parts: i } = this._$AD, r = ((e == null ? void 0 : e.creationScope) ?? A).importNode(t, !0);
    b.currentNode = r;
    let a = b.nextNode(), n = 0, d = 0, o = i[0];
    for (; o !== void 0; ) {
      if (n === o.index) {
        let c;
        o.type === 2 ? c = new M(a, a.nextSibling, this, e) : o.type === 1 ? c = new o.ctor(a, o.name, o.strings, this, e) : o.type === 6 && (c = new Oe(a, this, e)), this._$AV.push(c), o = i[++d];
      }
      n !== (o == null ? void 0 : o.index) && (a = b.nextNode(), n++);
    }
    return b.currentNode = A, r;
  }
  p(e) {
    let t = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(e, i, t), t += i.strings.length - 2) : i._$AI(e[t])), t++;
  }
}
class M {
  get _$AU() {
    var e;
    return ((e = this._$AM) == null ? void 0 : e._$AU) ?? this._$Cv;
  }
  constructor(e, t, i, r) {
    this.type = 2, this._$AH = p, this._$AN = void 0, this._$AA = e, this._$AB = t, this._$AM = i, this.options = r, this._$Cv = (r == null ? void 0 : r.isConnected) ?? !0;
  }
  get parentNode() {
    let e = this._$AA.parentNode;
    const t = this._$AM;
    return t !== void 0 && (e == null ? void 0 : e.nodeType) === 11 && (e = t.parentNode), e;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(e, t = this) {
    e = k(this, e, t), I(e) ? e === p || e == null || e === "" ? (this._$AH !== p && this._$AR(), this._$AH = p) : e !== this._$AH && e !== P && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : xe(e) ? this.k(e) : this._(e);
  }
  O(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), this._$AH = this.O(e));
  }
  _(e) {
    this._$AH !== p && I(this._$AH) ? this._$AA.nextSibling.data = e : this.T(A.createTextNode(e)), this._$AH = e;
  }
  $(e) {
    var a;
    const { values: t, _$litType$: i } = e, r = typeof i == "number" ? this._$AC(e) : (i.el === void 0 && (i.el = H.createElement(he(i.h, i.h[0]), this.options)), i);
    if (((a = this._$AH) == null ? void 0 : a._$AD) === r) this._$AH.p(t);
    else {
      const n = new Pe(r, this), d = n.u(this.options);
      n.p(t), this.T(d), this._$AH = n;
    }
  }
  _$AC(e) {
    let t = ae.get(e.strings);
    return t === void 0 && ae.set(e.strings, t = new H(e)), t;
  }
  k(e) {
    K(this._$AH) || (this._$AH = [], this._$AR());
    const t = this._$AH;
    let i, r = 0;
    for (const a of e) r === t.length ? t.push(i = new M(this.O(C()), this.O(C()), this, this.options)) : i = t[r], i._$AI(a), r++;
    r < t.length && (this._$AR(i && i._$AB.nextSibling, r), t.length = r);
  }
  _$AR(e = this._$AA.nextSibling, t) {
    var i;
    for ((i = this._$AP) == null ? void 0 : i.call(this, !1, !0, t); e !== this._$AB; ) {
      const r = e.nextSibling;
      e.remove(), e = r;
    }
  }
  setConnected(e) {
    var t;
    this._$AM === void 0 && (this._$Cv = e, (t = this._$AP) == null || t.call(this, e));
  }
}
class R {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, t, i, r, a) {
    this.type = 1, this._$AH = p, this._$AN = void 0, this.element = e, this.name = t, this._$AM = r, this.options = a, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = p;
  }
  _$AI(e, t = this, i, r) {
    const a = this.strings;
    let n = !1;
    if (a === void 0) e = k(this, e, t, 0), n = !I(e) || e !== this._$AH && e !== P, n && (this._$AH = e);
    else {
      const d = e;
      let o, c;
      for (e = a[0], o = 0; o < a.length - 1; o++) c = k(this, d[i + o], t, o), c === P && (c = this._$AH[o]), n || (n = !I(c) || c !== this._$AH[o]), c === p ? e = p : e !== p && (e += (c ?? "") + a[o + 1]), this._$AH[o] = c;
    }
    n && !r && this.j(e);
  }
  j(e) {
    e === p ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class ke extends R {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === p ? void 0 : e;
  }
}
class Se extends R {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== p);
  }
}
class Ve extends R {
  constructor(e, t, i, r, a) {
    super(e, t, i, r, a), this.type = 5;
  }
  _$AI(e, t = this) {
    if ((e = k(this, e, t, 0) ?? p) === P) return;
    const i = this._$AH, r = e === p && i !== p || e.capture !== i.capture || e.once !== i.once || e.passive !== i.passive, a = e !== p && (i === p || r);
    r && this.element.removeEventListener(this.name, this, i), a && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    var t;
    typeof this._$AH == "function" ? this._$AH.call(((t = this.options) == null ? void 0 : t.host) ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class Oe {
  constructor(e, t, i) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = t, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    k(this, e);
  }
}
const B = O.litHtmlPolyfillSupport;
B == null || B(H, M), (O.litHtmlVersions ?? (O.litHtmlVersions = [])).push("3.3.1");
const Le = (s, e, t) => {
  const i = (t == null ? void 0 : t.renderBefore) ?? e;
  let r = i._$litPart$;
  if (r === void 0) {
    const a = (t == null ? void 0 : t.renderBefore) ?? null;
    i._$litPart$ = r = new M(e.insertBefore(C(), a), a, void 0, t ?? {});
  }
  return r._$AI(s), r;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const x = globalThis;
class L extends E {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var t;
    const e = super.createRenderRoot();
    return (t = this.renderOptions).renderBefore ?? (t.renderBefore = e.firstChild), e;
  }
  update(e) {
    const t = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(e), this._$Do = Le(t, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    var e;
    super.connectedCallback(), (e = this._$Do) == null || e.setConnected(!0);
  }
  disconnectedCallback() {
    var e;
    super.disconnectedCallback(), (e = this._$Do) == null || e.setConnected(!1);
  }
  render() {
    return P;
  }
}
var ne;
L._$litElement$ = !0, L.finalized = !0, (ne = x.litElementHydrateSupport) == null || ne.call(x, { LitElement: L });
const F = x.litElementPolyfillSupport;
F == null || F({ LitElement: L });
(x.litElementVersions ?? (x.litElementVersions = [])).push("4.2.1");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ce = (s) => (e, t) => {
  t !== void 0 ? t.addInitializer(() => {
    customElements.define(s, e);
  }) : customElements.define(s, e);
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ie = { attribute: !0, type: String, converter: W, reflect: !1, hasChanged: G }, He = (s = Ie, e, t) => {
  const { kind: i, metadata: r } = t;
  let a = globalThis.litPropertyMetadata.get(r);
  if (a === void 0 && globalThis.litPropertyMetadata.set(r, a = /* @__PURE__ */ new Map()), i === "setter" && ((s = Object.create(s)).wrapped = !0), a.set(t.name, s), i === "accessor") {
    const { name: n } = t;
    return { set(d) {
      const o = e.get.call(this);
      e.set.call(this, d), this.requestUpdate(n, o, s);
    }, init(d) {
      return d !== void 0 && this.C(n, void 0, s, d), d;
    } };
  }
  if (i === "setter") {
    const { name: n } = t;
    return function(d) {
      const o = this[n];
      e.call(this, d), this.requestUpdate(n, o, s);
    };
  }
  throw Error("Unsupported decorator location: " + i);
};
function U(s) {
  return (e, t) => typeof t == "object" ? He(s, e, t) : ((i, r, a) => {
    const n = r.hasOwnProperty(a);
    return r.constructor.createProperty(a, i), n ? Object.getOwnPropertyDescriptor(r, a) : void 0;
  })(s, e, t);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function _(s) {
  return U({ ...s, state: !0, attribute: !1 });
}
var Me = Object.defineProperty, Ue = Object.getOwnPropertyDescriptor, v = (s, e, t, i) => {
  for (var r = i > 1 ? void 0 : i ? Ue(e, t) : e, a = s.length - 1, n; a >= 0; a--)
    (n = s[a]) && (r = (i ? n(e, t, r) : n(r)) || r);
  return i && r && Me(e, t, r), r;
};
function Te(s, e) {
  let t;
  return (...i) => {
    clearTimeout(t), t = setTimeout(() => s(...i), e);
  };
}
let g = class extends L {
  constructor() {
    super(...arguments), this.narrow = !1, this._page = "views", this._config = null, this._views = [], this._devices = [], this._editingView = null, this._previewImage = null, this._previewLoading = !1, this._loading = !0, this._saving = !1, this._expandedItems = /* @__PURE__ */ new Set(), this._refreshPreview = Te(async () => {
      if (this._editingView) {
        this._previewLoading = !0;
        try {
          const s = await this.hass.connection.sendMessagePromise({
            type: "geekmagic/preview/render",
            view_config: {
              layout: this._editingView.layout,
              theme: this._editingView.theme,
              widgets: this._editingView.widgets
            }
          });
          this._previewImage = s.image;
        } catch (s) {
          console.error("Failed to render preview:", s);
        } finally {
          this._previewLoading = !1;
        }
      }
    }, 500);
  }
  firstUpdated() {
    this._loadData();
  }
  async _loadData() {
    this._loading = !0;
    try {
      const [s, e, t] = await Promise.all([
        this.hass.connection.sendMessagePromise({
          type: "geekmagic/config"
        }),
        this.hass.connection.sendMessagePromise({
          type: "geekmagic/views/list"
        }),
        this.hass.connection.sendMessagePromise({
          type: "geekmagic/devices/list"
        })
      ]);
      this._config = s, this._views = e.views, this._devices = t.devices;
    } catch (s) {
      console.error("Failed to load GeekMagic config:", s);
    } finally {
      this._loading = !1;
    }
  }
  async _createView() {
    const s = prompt("Enter view name:", "New View");
    if (s)
      try {
        const e = await this.hass.connection.sendMessagePromise({
          type: "geekmagic/views/create",
          name: s,
          layout: "grid_2x2",
          theme: "classic",
          widgets: []
        });
        this._views = [...this._views, e.view], this._editView(e.view);
      } catch (e) {
        console.error("Failed to create view:", e);
      }
  }
  _editView(s) {
    this._editingView = { ...s, widgets: [...s.widgets] }, this._page = "editor", this._refreshPreview();
  }
  async _saveView() {
    if (this._editingView) {
      this._saving = !0;
      try {
        await this.hass.connection.sendMessagePromise({
          type: "geekmagic/views/update",
          view_id: this._editingView.id,
          name: this._editingView.name,
          layout: this._editingView.layout,
          theme: this._editingView.theme,
          widgets: this._editingView.widgets
        }), this._views = this._views.map(
          (s) => s.id === this._editingView.id ? this._editingView : s
        ), this._page = "views", this._editingView = null;
      } catch (s) {
        console.error("Failed to save view:", s);
      } finally {
        this._saving = !1;
      }
    }
  }
  async _deleteView(s) {
    if (confirm(`Delete view "${s.name}"?`))
      try {
        await this.hass.connection.sendMessagePromise({
          type: "geekmagic/views/delete",
          view_id: s.id
        }), this._views = this._views.filter((e) => e.id !== s.id);
      } catch (e) {
        console.error("Failed to delete view:", e);
      }
  }
  _updateEditingView(s) {
    this._editingView && (this._editingView = { ...this._editingView, ...s }, this._refreshPreview());
  }
  _updateWidget(s, e) {
    if (!this._editingView) return;
    const t = [...this._editingView.widgets], i = t.findIndex((r) => r.slot === s);
    i >= 0 ? t[i] = { ...t[i], ...e } : t.push({ slot: s, type: "", ...e }), this._editingView = { ...this._editingView, widgets: [...t] }, this.requestUpdate(), this._refreshPreview();
  }
  async _toggleDeviceView(s, e, t) {
    const i = t ? [...s.assigned_views, e] : s.assigned_views.filter((r) => r !== e);
    try {
      await this.hass.connection.sendMessagePromise({
        type: "geekmagic/devices/assign_views",
        entry_id: s.entry_id,
        view_ids: i
      }), this._devices = this._devices.map(
        (r) => r.entry_id === s.entry_id ? { ...r, assigned_views: i } : r
      );
    } catch (r) {
      console.error("Failed to update device views:", r);
    }
  }
  render() {
    return this._loading ? l`
        <div class="loading">
          <ha-circular-progress indeterminate></ha-circular-progress>
        </div>
      ` : l`
      <div class="header">
        <ha-icon icon="mdi:monitor-dashboard"></ha-icon>
        <span class="header-title">GeekMagic</span>
      </div>
      ${this._page !== "editor" ? l`
            <ha-tab-group @wa-tab-show=${this._handleTabChange}>
              <ha-tab-group-tab
                slot="nav"
                panel="views"
                .active=${this._page === "views"}
              >
                Views
              </ha-tab-group-tab>
              <ha-tab-group-tab
                slot="nav"
                panel="devices"
                .active=${this._page === "devices"}
              >
                Devices
              </ha-tab-group-tab>
            </ha-tab-group>
          ` : p}
      <div class="content">${this._renderPage()}</div>
    `;
  }
  _renderPage() {
    switch (this._page) {
      case "views":
        return this._renderViewsList();
      case "devices":
        return this._renderDevicesList();
      case "editor":
        return this._renderEditor();
    }
  }
  _handleTabChange(s) {
    const t = s.target.getAttribute("panel");
    (t === "views" || t === "devices") && (this._page = t);
  }
  _renderViewsList() {
    return l`
      <div class="views-grid">
        ${this._views.map(
      (s) => {
        var e, t, i;
        return l`
            <ha-card class="view-card" @click=${() => this._editView(s)}>
              <div class="card-header">
                <h3>${s.name}</h3>
                <ha-icon-button
                  .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                  @click=${(r) => {
          r.stopPropagation(), this._deleteView(s);
        }}
                ></ha-icon-button>
              </div>
              <div class="card-content">
                <div class="card-meta">
                  ${((t = (e = this._config) == null ? void 0 : e.layout_types[s.layout]) == null ? void 0 : t.name) || s.layout}
                  &bull; ${((i = this._config) == null ? void 0 : i.themes[s.theme]) || s.theme}
                  &bull; ${s.widgets.length} widgets
                </div>
              </div>
            </ha-card>
          `;
      }
    )}
        <div class="add-card" @click=${this._createView}>
          <ha-icon icon="mdi:plus"></ha-icon>
          <span style="margin-left: 8px">Add View</span>
        </div>
      </div>
    `;
  }
  _renderDevicesList() {
    return this._devices.length === 0 ? l`
        <div class="empty-state">
          <ha-icon icon="mdi:monitor-off"></ha-icon>
          <p>No GeekMagic devices configured.</p>
          <p>Add a device through Settings → Devices & Services.</p>
        </div>
      ` : l`
      <div class="devices-list">
        ${this._devices.map(
      (s) => l`
            <ha-card>
              <div class="card-content" style="padding-top: 16px;">
                <div class="device-header">
                  <span class="device-name">${s.name}</span>
                  <span class="device-status ${s.online ? "online" : "offline"}">
                    ${s.online ? "Online" : "Offline"}
                  </span>
                </div>
                <div class="views-checkboxes">
                  <div class="section-title" style="margin-top: 8px;">Assigned Views</div>
                  ${this._views.length === 0 ? l`<p style="color: var(--secondary-text-color)">
                        No views available. Create a view first.
                      </p>` : this._views.map(
        (e) => l`
                          <label class="view-checkbox">
                            <ha-checkbox
                              .checked=${s.assigned_views.includes(e.id)}
                              @change=${(t) => this._toggleDeviceView(
          s,
          e.id,
          t.target.checked
        )}
                            ></ha-checkbox>
                            ${e.name}
                          </label>
                        `
      )}
                </div>
              </div>
            </ha-card>
          `
    )}
      </div>
    `;
  }
  _renderEditor() {
    var e;
    if (!this._editingView || !this._config) return p;
    const s = ((e = this._config.layout_types[this._editingView.layout]) == null ? void 0 : e.slots) || 4;
    return l`
      <div class="editor-header">
        <ha-icon-button
          .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
          @click=${() => this._page = "views"}
        ></ha-icon-button>
        <ha-textfield
          .value=${this._editingView.name}
          @input=${(t) => this._updateEditingView({
      name: t.target.value
    })}
          placeholder="View name"
        ></ha-textfield>
        <ha-button raised ?disabled=${this._saving} @click=${this._saveView}>
          ${this._saving ? "Saving..." : "Save"}
        </ha-button>
      </div>

      <div class="editor-form">
        <!-- Preview at top -->
        <div class="preview-section">
          <ha-card class="preview-card">
            <div class="card-header">
              <h3>Preview</h3>
              <ha-icon-button
                .path=${"M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"}
                @click=${() => this._refreshPreview()}
              ></ha-icon-button>
            </div>
            <div class="card-content">
              ${this._previewLoading ? l`<div class="preview-placeholder">
                    <ha-circular-progress indeterminate></ha-circular-progress>
                  </div>` : this._previewImage ? l`<img
                      class="preview-image"
                      src="data:image/png;base64,${this._previewImage}"
                      alt="Preview"
                    />` : l`<div class="preview-placeholder">No preview</div>`}
            </div>
          </ha-card>
        </div>

        <!-- Layout and theme selectors -->
        <div class="form-row">
          <ha-select
            label="Layout"
            .value=${this._editingView.layout}
            @selected=${(t) => {
      const i = t.detail.index, a = Object.keys(this._config.layout_types)[i];
      a && this._updateEditingView({ layout: a });
    }}
            @closed=${(t) => t.stopPropagation()}
          >
            ${Object.entries(this._config.layout_types).map(
      ([t, i]) => l`
                <mwc-list-item value=${t}>
                  ${i.name} (${i.slots} slots)
                </mwc-list-item>
              `
    )}
          </ha-select>
          <ha-select
            label="Theme"
            .value=${this._editingView.theme}
            @selected=${(t) => {
      const i = t.detail.index, a = Object.keys(this._config.themes)[i];
      a && this._updateEditingView({ theme: a });
    }}
            @closed=${(t) => t.stopPropagation()}
          >
            ${Object.entries(this._config.themes).map(
      ([t, i]) => l`
                <mwc-list-item value=${t}>${i}</mwc-list-item>
              `
    )}
          </ha-select>
        </div>

        <!-- Widget slots -->
        <div class="section-title">Widgets</div>
        <div class="slots-grid">
          ${Array.from(
      { length: s },
      (t, i) => this._renderSlotEditor(i, s)
    )}
        </div>
      </div>
    `;
  }
  _renderSlotEditor(s, e) {
    var n;
    if (!this._config || !this._editingView) return p;
    const t = this._editingView.widgets.find((d) => d.slot === s), i = (t == null ? void 0 : t.type) || "", r = this._config.widget_types[i], a = this._editingView.layout;
    return l`
      <ha-card class="slot-card">
        <div class="card-content">
          <div class="slot-header">
            ${this._renderPositionGrid(s, e, a)}
            <span style="flex: 1;">Slot ${s + 1}</span>
          </div>

          <div class="slot-field">
            <ha-select
              label="Widget Type"
              .value=${i}
              @selected=${(d) => {
      const o = d.detail.index, u = ["", ...Object.keys(this._config.widget_types)][o] || "";
      this._updateWidget(s, { type: u });
    }}
              @closed=${(d) => d.stopPropagation()}
            >
              <mwc-list-item value="">-- Empty --</mwc-list-item>
              ${Object.entries(this._config.widget_types).map(
      ([d, o]) => l`
                  <mwc-list-item value=${d}>${o.name}</mwc-list-item>
                `
    )}
            </ha-select>
          </div>

          ${r != null && r.needs_entity ? l`
                <div class="slot-field">
                  <ha-selector
                    .hass=${this.hass}
                    .selector=${{
      entity: r.entity_domains ? { domain: r.entity_domains } : {}
    }}
                    .value=${(t == null ? void 0 : t.entity_id) || ""}
                    .label=${"Entity"}
                    @value-changed=${(d) => this._updateWidget(s, {
      entity_id: d.detail.value
    })}
                  ></ha-selector>
                </div>
              ` : p}

          <div class="slot-field">
            <ha-textfield
              label="Label (optional)"
              .value=${(t == null ? void 0 : t.label) || ""}
              @input=${(d) => this._updateWidget(s, {
      label: d.target.value
    })}
            ></ha-textfield>
          </div>

          ${(n = r == null ? void 0 : r.options) != null && n.length ? l`
                <div class="widget-options">
                  ${r.options.map(
      (d) => this._renderOptionField(s, t, d)
    )}
                </div>
              ` : p}
        </div>
      </ha-card>
    `;
  }
  _renderOptionField(s, e, t) {
    var r, a;
    const i = ((r = e == null ? void 0 : e.options) == null ? void 0 : r[t.key]) ?? t.default;
    switch (t.type) {
      case "boolean":
        return l`
          <div class="option-row">
            <label>${t.label}</label>
            <ha-switch
              .checked=${!!i}
              @change=${(n) => this._updateWidgetOption(
          s,
          t.key,
          n.target.checked
        )}
            ></ha-switch>
          </div>
        `;
      case "select":
        return l`
          <div class="option-field">
            <ha-select
              .label=${t.label}
              .value=${i || t.default || ""}
              @selected=${(n) => {
          var c;
          const d = n.detail.index, o = (c = t.options) == null ? void 0 : c[d];
          o !== void 0 && this._updateWidgetOption(s, t.key, o);
        }}
              @closed=${(n) => n.stopPropagation()}
            >
              ${(a = t.options) == null ? void 0 : a.map(
          (n) => l`<mwc-list-item value=${n}>${n}</mwc-list-item>`
        )}
            </ha-select>
          </div>
        `;
      case "number":
        return l`
          <div class="option-field">
            <ha-textfield
              type="number"
              .label=${t.label}
              .value=${i !== void 0 ? String(i) : ""}
              .min=${t.min !== void 0 ? String(t.min) : ""}
              .max=${t.max !== void 0 ? String(t.max) : ""}
              @input=${(n) => {
          const d = n.target.value;
          this._updateWidgetOption(
            s,
            t.key,
            d ? parseFloat(d) : void 0
          );
        }}
            ></ha-textfield>
          </div>
        `;
      case "text":
        return l`
          <div class="option-field">
            <ha-textfield
              .label=${t.label}
              .value=${i || ""}
              .placeholder=${t.placeholder || ""}
              @input=${(n) => this._updateWidgetOption(
          s,
          t.key,
          n.target.value
        )}
            ></ha-textfield>
          </div>
        `;
      case "icon":
        return l`
          <div class="option-field">
            <ha-icon-picker
              .hass=${this.hass}
              .label=${t.label}
              .value=${i || ""}
              @value-changed=${(n) => this._updateWidgetOption(s, t.key, n.detail.value)}
            ></ha-icon-picker>
          </div>
        `;
      case "color":
        return l`
          <div class="option-field">
            <ha-selector
              .hass=${this.hass}
              .selector=${{ color_rgb: {} }}
              .value=${i}
              .label=${t.label}
              @value-changed=${(n) => this._updateWidgetOption(s, t.key, n.detail.value)}
            ></ha-selector>
          </div>
        `;
      case "entity":
        return l`
          <div class="option-field">
            <ha-selector
              .hass=${this.hass}
              .selector=${{ entity: {} }}
              .value=${i || ""}
              .label=${t.label}
              @value-changed=${(n) => this._updateWidgetOption(s, t.key, n.detail.value)}
            ></ha-selector>
          </div>
        `;
      case "thresholds":
        return this._renderThresholdsEditor(s, t.key, i);
      case "progress_items":
        return this._renderProgressItemsEditor(s, t.key, i);
      case "status_entities":
        return this._renderStatusEntitiesEditor(s, t.key, i);
      default:
        return p;
    }
  }
  _updateWidgetOption(s, e, t) {
    if (!this._editingView) return;
    const i = [...this._editingView.widgets], r = i.findIndex((a) => a.slot === s);
    if (r >= 0) {
      const a = i[r];
      i[r] = {
        ...a,
        options: { ...a.options || {}, [e]: t }
      };
    } else
      i.push({
        slot: s,
        type: "",
        options: { [e]: t }
      });
    this._editingView = { ...this._editingView, widgets: [...i] }, this.requestUpdate(), this._refreshPreview();
  }
  _renderThresholdsEditor(s, e, t) {
    const i = t || [];
    return l`
      <div class="option-field">
        <div class="array-editor">
          <div class="array-editor-header">
            <span>Color Thresholds</span>
          </div>
          <div class="array-items">
            ${i.map(
      (r, a) => l`
                <div class="threshold-item">
                  <ha-textfield
                    class="threshold-value"
                    type="number"
                    label="Value"
                    .value=${String(r.value)}
                    @input=${(n) => {
        const d = [...i];
        d[a] = {
          ...r,
          value: parseFloat(n.target.value) || 0
        }, this._updateWidgetOption(s, e, d);
      }}
                  ></ha-textfield>
                  <ha-selector
                    .hass=${this.hass}
                    .selector=${{ color_rgb: {} }}
                    .value=${r.color}
                    @value-changed=${(n) => {
        const d = [...i];
        d[a] = { ...r, color: n.detail.value }, this._updateWidgetOption(s, e, d);
      }}
                  ></ha-selector>
                  <ha-icon-button
                    .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                    @click=${() => {
        const n = i.filter((d, o) => o !== a);
        this._updateWidgetOption(s, e, n);
      }}
                  ></ha-icon-button>
                </div>
              `
    )}
            <div
              class="add-item-button"
              @click=${() => {
      const r = [...i, { value: 0, color: [255, 255, 0] }];
      this._updateWidgetOption(s, e, r);
    }}
            >
              <ha-icon icon="mdi:plus"></ha-icon>
              Add Threshold
            </div>
          </div>
        </div>
      </div>
    `;
  }
  _renderProgressItemsEditor(s, e, t) {
    const i = t || [];
    return l`
      <div class="option-field">
        <div class="array-editor">
          <div class="array-editor-header">
            <span>Progress Items (${i.length})</span>
          </div>
          <div class="array-items">
            ${i.map((r, a) => {
      const n = `${s}-progress-${a}`, d = this._expandedItems.has(n);
      return l`
                <div class="array-item">
                  <div
                    class="array-item-header"
                    @click=${() => this._toggleItemExpanded(n)}
                  >
                    <span class="array-item-title">
                      ${r.label || r.entity_id || `Item ${a + 1}`}
                    </span>
                    <div class="array-item-actions">
                      <ha-icon-button
                        .path=${a > 0 ? "M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z" : ""}
                        @click=${(o) => {
        o.stopPropagation(), a > 0 && this._moveArrayItem(s, e, i, a, -1);
      }}
                      ></ha-icon-button>
                      <ha-icon-button
                        .path=${a < i.length - 1 ? "M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" : ""}
                        @click=${(o) => {
        o.stopPropagation(), a < i.length - 1 && this._moveArrayItem(s, e, i, a, 1);
      }}
                      ></ha-icon-button>
                      <ha-icon-button
                        .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                        @click=${(o) => {
        o.stopPropagation();
        const c = i.filter((u, h) => h !== a);
        this._updateWidgetOption(s, e, c);
      }}
                      ></ha-icon-button>
                    </div>
                  </div>
                  <div class="array-item-content ${d ? "" : "collapsed"}">
                    <ha-selector
                      .hass=${this.hass}
                      .selector=${{ entity: {} }}
                      .value=${r.entity_id || ""}
                      .label=${"Entity"}
                      @value-changed=${(o) => this._updateArrayItem(s, e, i, a, {
        entity_id: o.detail.value
      })}
                    ></ha-selector>
                    <ha-textfield
                      label="Label"
                      .value=${r.label || ""}
                      @input=${(o) => this._updateArrayItem(s, e, i, a, {
        label: o.target.value
      })}
                    ></ha-textfield>
                    <ha-textfield
                      type="number"
                      label="Target"
                      .value=${r.target !== void 0 ? String(r.target) : "100"}
                      @input=${(o) => this._updateArrayItem(s, e, i, a, {
        target: parseFloat(o.target.value) || 100
      })}
                    ></ha-textfield>
                    <ha-icon-picker
                      .hass=${this.hass}
                      label="Icon"
                      .value=${r.icon || ""}
                      @value-changed=${(o) => this._updateArrayItem(s, e, i, a, {
        icon: o.detail.value
      })}
                    ></ha-icon-picker>
                    <ha-selector
                      .hass=${this.hass}
                      .selector=${{ color_rgb: {} }}
                      .value=${r.color}
                      .label=${"Color"}
                      @value-changed=${(o) => this._updateArrayItem(s, e, i, a, {
        color: o.detail.value
      })}
                    ></ha-selector>
                  </div>
                </div>
              `;
    })}
            <div
              class="add-item-button"
              @click=${() => {
      const r = [...i, { entity_id: "", target: 100 }];
      this._updateWidgetOption(s, e, r), this._expandedItems.add(`${s}-progress-${r.length - 1}`), this.requestUpdate();
    }}
            >
              <ha-icon icon="mdi:plus"></ha-icon>
              Add Progress Item
            </div>
          </div>
        </div>
      </div>
    `;
  }
  _renderStatusEntitiesEditor(s, e, t) {
    const i = t || [];
    return l`
      <div class="option-field">
        <div class="array-editor">
          <div class="array-editor-header">
            <span>Status Entities (${i.length})</span>
          </div>
          <div class="array-items">
            ${i.map((r, a) => {
      const n = `${s}-status-${a}`, d = this._expandedItems.has(n);
      return l`
                <div class="array-item">
                  <div
                    class="array-item-header"
                    @click=${() => this._toggleItemExpanded(n)}
                  >
                    <span class="array-item-title">
                      ${r.label || r.entity_id || `Entity ${a + 1}`}
                    </span>
                    <div class="array-item-actions">
                      <ha-icon-button
                        .path=${a > 0 ? "M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z" : ""}
                        @click=${(o) => {
        o.stopPropagation(), a > 0 && this._moveArrayItem(s, e, i, a, -1);
      }}
                      ></ha-icon-button>
                      <ha-icon-button
                        .path=${a < i.length - 1 ? "M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" : ""}
                        @click=${(o) => {
        o.stopPropagation(), a < i.length - 1 && this._moveArrayItem(s, e, i, a, 1);
      }}
                      ></ha-icon-button>
                      <ha-icon-button
                        .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                        @click=${(o) => {
        o.stopPropagation();
        const c = i.filter((u, h) => h !== a);
        this._updateWidgetOption(s, e, c);
      }}
                      ></ha-icon-button>
                    </div>
                  </div>
                  <div class="array-item-content ${d ? "" : "collapsed"}">
                    <ha-selector
                      .hass=${this.hass}
                      .selector=${{ entity: {} }}
                      .value=${r.entity_id || ""}
                      .label=${"Entity"}
                      @value-changed=${(o) => this._updateArrayItem(s, e, i, a, {
        entity_id: o.detail.value
      })}
                    ></ha-selector>
                    <ha-textfield
                      label="Label"
                      .value=${r.label || ""}
                      @input=${(o) => this._updateArrayItem(s, e, i, a, {
        label: o.target.value
      })}
                    ></ha-textfield>
                    <ha-icon-picker
                      .hass=${this.hass}
                      label="Icon"
                      .value=${r.icon || ""}
                      @value-changed=${(o) => this._updateArrayItem(s, e, i, a, {
        icon: o.detail.value
      })}
                    ></ha-icon-picker>
                  </div>
                </div>
              `;
    })}
            <div
              class="add-item-button"
              @click=${() => {
      const r = [...i, { entity_id: "" }];
      this._updateWidgetOption(s, e, r), this._expandedItems.add(`${s}-status-${r.length - 1}`), this.requestUpdate();
    }}
            >
              <ha-icon icon="mdi:plus"></ha-icon>
              Add Status Entity
            </div>
          </div>
        </div>
      </div>
    `;
  }
  _toggleItemExpanded(s) {
    this._expandedItems.has(s) ? this._expandedItems.delete(s) : this._expandedItems.add(s), this._expandedItems = new Set(this._expandedItems);
  }
  _updateArrayItem(s, e, t, i, r) {
    const a = [...t];
    a[i] = { ...a[i], ...r }, this._updateWidgetOption(s, e, a);
  }
  _moveArrayItem(s, e, t, i, r) {
    const a = i + r;
    if (a < 0 || a >= t.length) return;
    const n = [...t];
    [n[i], n[a]] = [n[a], n[i]], this._updateWidgetOption(s, e, n);
  }
  _renderPositionGrid(s, e, t) {
    let i = 2, r = !1;
    switch (t) {
      case "grid_2x2":
        i = 2;
        break;
      case "grid_2x3":
        i = 3;
        break;
      case "grid_3x2":
        i = 2;
        break;
      case "hero":
        i = 3, r = !0;
        break;
      case "split":
        i = 2;
        break;
      case "three_column":
        i = 3;
        break;
      default:
        i = 2;
    }
    const a = [];
    if (r) {
      a.push(l`
        <div
          class="position-cell hero-main ${s === 0 ? "active" : ""}"
          @click=${() => this._swapSlots(s, 0)}
          title="Hero (main)"
        ></div>
      `);
      for (let n = 1; n <= 3; n++)
        a.push(l`
          <div
            class="position-cell ${s === n ? "active" : ""}"
            @click=${() => this._swapSlots(s, n)}
            title="Footer ${n}"
          ></div>
        `);
    } else
      for (let n = 0; n < e; n++)
        a.push(l`
          <div
            class="position-cell ${s === n ? "active" : ""}"
            @click=${() => this._swapSlots(s, n)}
            title="Slot ${n + 1}"
          ></div>
        `);
    return l`
      <div class="position-grid cols-${i}">${a}</div>
    `;
  }
  _swapSlots(s, e) {
    if (s === e || !this._editingView) return;
    const t = [...this._editingView.widgets], i = t.find((a) => a.slot === s), r = t.find((a) => a.slot === e);
    i && (i.slot = e), r && (r.slot = s), this._editingView = { ...this._editingView, widgets: [...t] }, this.requestUpdate(), this._refreshPreview();
  }
};
g.styles = ue`
    :host {
      display: flex;
      flex-direction: column;
      height: 100%;
      --mdc-theme-primary: var(--primary-color);
      --mdc-theme-on-primary: var(--text-primary-color);
    }

    /* Header */
    .header {
      display: flex;
      align-items: center;
      padding: 0 16px;
      height: 56px;
      border-bottom: 1px solid var(--divider-color);
      background: var(--app-header-background-color);
    }

    .header-title {
      font-size: 20px;
      font-weight: 400;
      margin-left: 8px;
    }

    .content {
      flex: 1;
      overflow: auto;
      padding: 16px;
      background: var(--primary-background-color);
    }

    .loading {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
    }

    /* Views Grid */
    .views-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 16px;
    }

    ha-card {
      --ha-card-border-radius: 12px;
    }

    .view-card {
      cursor: pointer;
    }

    .view-card:hover {
      --ha-card-background: var(--secondary-background-color);
    }

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px;
    }

    .card-header h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 500;
    }

    .card-content {
      padding: 0 16px 16px;
    }

    .card-meta {
      font-size: 14px;
      color: var(--secondary-text-color);
    }

    .add-card {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 120px;
      border: 2px dashed var(--divider-color);
      border-radius: 12px;
      cursor: pointer;
      color: var(--secondary-text-color);
      transition: all 0.2s;
    }

    .add-card:hover {
      border-color: var(--primary-color);
      color: var(--primary-color);
    }

    /* Editor */
    .editor-header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
    }

    .editor-header ha-textfield {
      flex: 1;
    }

    .editor-form {
      width: 100%;
    }

    /* Preview section - above widgets */
    .preview-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 24px;
    }

    .preview-card {
      width: 100%;
      max-width: 300px;
    }

    .preview-card .card-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
    }

    .preview-image {
      width: 200px;
      height: 200px;
      border-radius: 8px;
      background: #000;
      object-fit: contain;
    }

    .preview-placeholder {
      width: 200px;
      height: 200px;
      border-radius: 8px;
      background: var(--secondary-background-color);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--secondary-text-color);
    }

    /* Form Layout */
    .form-row {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
    }

    .form-row > * {
      flex: 1;
    }

    .section-title {
      font-size: 14px;
      font-weight: 500;
      color: var(--primary-text-color);
      margin: 24px 0 16px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .section-title:first-child {
      margin-top: 0;
    }

    /* Slots list - fluid responsive grid */
    .slots-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      width: 100%;
    }

    /* Single column on mobile */
    @media (max-width: 600px) {
      .slots-grid {
        grid-template-columns: 1fr;
      }
    }

    .slot-card {
      --ha-card-border-radius: 8px;
    }

    .slot-card .card-content {
      padding: 16px;
    }

    .slot-header {
      display: flex;
      align-items: center;
      font-weight: 500;
      margin-bottom: 16px;
      color: var(--primary-text-color);
    }

    /* Tiny position grid */
    .position-grid {
      display: inline-grid;
      gap: 2px;
      margin-right: 12px;
      padding: 4px;
      background: var(--secondary-background-color);
      border-radius: 4px;
    }

    .position-grid.cols-2 {
      grid-template-columns: repeat(2, 16px);
    }

    .position-grid.cols-3 {
      grid-template-columns: repeat(3, 16px);
    }

    .position-cell {
      width: 16px;
      height: 16px;
      background: var(--divider-color);
      border-radius: 2px;
      cursor: pointer;
      transition: all 0.15s;
    }

    .position-cell:hover {
      background: var(--primary-color);
      opacity: 0.7;
    }

    .position-cell.active {
      background: var(--primary-color);
    }

    .position-cell.hero-main {
      grid-column: 1 / -1;
      width: auto;
      height: 24px;
    }

    .slot-field {
      margin-bottom: 16px;
    }

    .slot-field:last-child {
      margin-bottom: 0;
    }

    ha-select,
    ha-textfield {
      display: block;
      width: 100%;
    }

    ha-entity-picker {
      display: block;
      width: 100%;
    }

    /* Widget options */
    .widget-options {
      border-top: 1px solid var(--divider-color);
      padding-top: 16px;
      margin-top: 16px;
    }

    .option-field {
      margin-bottom: 12px;
    }

    .option-field:last-child {
      margin-bottom: 0;
    }

    .option-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 0;
    }

    .option-row label {
      font-size: 14px;
      color: var(--primary-text-color);
    }

    /* Array editors */
    .array-editor {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      padding: 12px;
      margin-top: 8px;
    }

    .array-editor-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .array-editor-header span {
      font-size: 14px;
      font-weight: 500;
    }

    .array-items {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .array-item {
      border: 1px solid var(--divider-color);
      border-radius: 6px;
      overflow: hidden;
    }

    .array-item-header {
      display: flex;
      align-items: center;
      padding: 8px 12px;
      background: var(--secondary-background-color);
      cursor: pointer;
    }

    .array-item-header:hover {
      background: var(--divider-color);
    }

    .array-item-title {
      flex: 1;
      font-size: 14px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .array-item-actions {
      display: flex;
      gap: 4px;
    }

    .array-item-content {
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .array-item-content.collapsed {
      display: none;
    }

    .add-item-button {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 8px;
      border: 1px dashed var(--divider-color);
      border-radius: 6px;
      cursor: pointer;
      color: var(--secondary-text-color);
      font-size: 14px;
      transition: all 0.2s;
    }

    .add-item-button:hover {
      border-color: var(--primary-color);
      color: var(--primary-color);
    }

    /* Color thresholds editor */
    .threshold-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .threshold-value {
      width: 80px;
    }

    .threshold-color {
      width: 60px;
      height: 32px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    /* Devices */
    .devices-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
      max-width: 800px;
    }

    .device-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .device-name {
      font-size: 16px;
      font-weight: 500;
    }

    .device-status {
      font-size: 12px;
      padding: 4px 12px;
      border-radius: 12px;
      font-weight: 500;
    }

    .device-status.online {
      background: var(--success-color, #4caf50);
      color: white;
    }

    .device-status.offline {
      background: var(--error-color, #f44336);
      color: white;
    }

    .views-checkboxes {
      margin-top: 16px;
    }

    .view-checkbox {
      display: flex;
      align-items: center;
      padding: 8px 0;
    }

    .view-checkbox ha-checkbox {
      margin-right: 8px;
    }

    /* Empty states */
    .empty-state {
      text-align: center;
      padding: 48px 16px;
      color: var(--secondary-text-color);
    }

    .empty-state ha-icon {
      --mdc-icon-size: 48px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
  `;
v([
  U({ attribute: !1 })
], g.prototype, "hass", 2);
v([
  U({ type: Boolean })
], g.prototype, "narrow", 2);
v([
  U({ attribute: !1 })
], g.prototype, "route", 2);
v([
  U({ attribute: !1 })
], g.prototype, "panel", 2);
v([
  _()
], g.prototype, "_page", 2);
v([
  _()
], g.prototype, "_config", 2);
v([
  _()
], g.prototype, "_views", 2);
v([
  _()
], g.prototype, "_devices", 2);
v([
  _()
], g.prototype, "_editingView", 2);
v([
  _()
], g.prototype, "_previewImage", 2);
v([
  _()
], g.prototype, "_previewLoading", 2);
v([
  _()
], g.prototype, "_loading", 2);
v([
  _()
], g.prototype, "_saving", 2);
v([
  _()
], g.prototype, "_expandedItems", 2);
g = v([
  Ce("geekmagic-panel")
], g);
export {
  g as GeekMagicPanel
};
