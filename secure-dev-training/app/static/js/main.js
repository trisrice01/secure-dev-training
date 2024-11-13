
const defaultErrorMessage = "There was an error submitting the flag, please try again";

async function submitChallengeFlag(challengeId, flagAttempt) {
    const data = { challenge_id: challengeId, challenge_flag: flagAttempt};
    let responseJson;
    try {
        const response = await fetch("/developer/challenge/complete", {
            "method": "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            }
        });
        responseJson = await response.json();
    } catch {
        return {error: true, message: defaultErrorMessage};
    }

    return responseJson;
}


function registerInteractiveElement(el) {
    // because Apache Guacamole intercepts all key commands
    // we need to de-register this functionality whenever an
    // interactive element is focused
    
    el.addEventListener("focus", () => {
        if (!window.guacKeyboard) {
            return;
        }

        window.guacKeyboard.onkeydown = null;
        window.guacKeyboard.oneyup = null;
    });
    
    el.addEventListener("blur", () => {
        if (!window.guacKeyboard) {
            return;
        }


        window.guacKeyboard.onkeydown = initialGuacKeyDownFunction
        window.guacKeyboard.onkeyup = initialGuacKeyUpFunction
    })
}


function createSVGElement(elementName, attributes={}) {
    let el = document.createElementNS("http://www.w3.org/2000/svg", elementName);
    for (const [attrName, attrValue] of Object.entries(attributes)) {
        el.setAttribute(attrName, attrValue);
    }
    return el;
}
class SVGIcon {
    constructor(rowSpace, colSpace, theme, row, column, isCompleted) {
        this.rowSpace = rowSpace;
        this.colSpace = colSpace;
        this.color = theme.bg || "#d9d9d9";
        this.fgColor = theme.fg || "red";
        this.row = row;
        this.column = column;
        this.isCompleted = isCompleted;
        this.maskingEl = null;
    }

    _createSVGElement(elementName, attributes={}) {
        let el = document.createElementNS("http://www.w3.org/2000/svg", elementName);
        for (const [attrName, attrValue] of Object.entries(attributes)) {
            el.setAttribute(attrName, attrValue);
        }
        return el;
    }

    render() {
        throw new Error("Not implemented");
    }

    animate(keyFrames) {
        return new Promise((resolve, reject) => {
            let animation = this.maskingEl.animate(keyFrames, {fill: "forwards", duration: 200})
            animation.onfinish = () => {
                resolve()
            }
        })
    }
}

class Flag extends SVGIcon {
    constructor(rowSpace, colSpace, color, row, column, isCompleted) {
        super(rowSpace, colSpace, color, row, column, isCompleted);
        this.width = 60;
    }

    animate() {
        return super.animate([
            { "width": "0" },
            { "width": "60px" }
        ])
    }

    render() {
        let flagGroup = document.createDocumentFragment();

        let col1 = 86 + (this.colSpace * (this.column - 1));
        let row1 = 19.5 + (this.rowSpace * (this.row - 1));
        let col2 = 119 + (this.colSpace * (this.column - 1));
        let row2 = 3 + (this.rowSpace * (this.row - 1));
        let row3 = 36 + (this.rowSpace * (this.row - 1));
        let col3 = col1
        let row4 = row1
        let pathValue = `M${col1} ${row1}L${col2} ${row2}V${row3}L${col3} ${row4}Z`;
        let flagPath = this._createSVGElement("path", {"d": pathValue, "fill": this.color});

        // rect element
        let rectX = 119 + (this.colSpace * (this.column - 1))
        let rectY = 3 + (this.rowSpace * (this.row - 1));
        let rect = this._createSVGElement("rect", 
            {"x": rectX, "y": rectY, "width": 9, "height": 90, "fill": this.color});

        // ellipse element 
        let ellipseX = 123.5 + (this.colSpace * (this.column - 1));
        let ellipseY = 102 + (this.rowSpace * (this.row - 1));
        let ellipse = this._createSVGElement("ellipse", 
            { "cx": ellipseX, "cy": ellipseY, "rx": 15.5, "ry": 15.5, "fill": this.color})

        let mask = this._createSVGElement("mask", {
            "id": `${this.column}-${this.row}`
        });

        mask.appendChild(flagPath);
        mask.appendChild(rect);
        mask.appendChild(ellipse);

        let maskingRectX = this.rowSpace * (this.row - 1)
        let maskingRectY = this.colSpace * (this.column - 1);
        let maskingRectWidth = this.rowSpace;
        let maskingRectCol = this.colSpace;

        let baseRect = this._createSVGElement("rect", 
            { x: col1, y: maskingRectX, width: 60, height: this.rowSpace, fill: "#d9d9d9", mask: `url(#${this.column}-${this.row})`} 
        )
        let completedRectWidth = this.isCompleted ? 60: 0;
        this.maskingEl = this._createSVGElement("rect",
            { x: col1, y: maskingRectX, width: completedRectWidth, height: this.rowSpace, fill: this.fgColor, mask: `url(#${this.column}-${this.row})`}
        )
        flagGroup.appendChild(mask);
        flagGroup.appendChild(baseRect)
        flagGroup.appendChild(this.maskingEl);

        return flagGroup;

    }
}

class StraightLine extends SVGIcon {
    constructor(rowSpace, colSpace, color, row, column, isCompleted, direction) {
        super(rowSpace, colSpace, color, row, column, isCompleted);
        this.direction = direction;
        this.rectLength = this.colSpace - 41;
    }

    animate() {
        return super.animate([
            { "strokeDashoffset": 320 },
            { "strokeDashoffset": 180 }
        ]);
    }

    render() {
        let base = document.createDocumentFragment();

        let rectX = 144 + (this.colSpace * (this.column - 1));
        let rectY = 97 + (this.rowSpace * (this.row - 1));

        let descriptor = this.direction === "left"
            ? `M${rectX - 41},${rectY + 5} L${rectX - 41 - this.rectLength},${rectY + 5}`
            : `M${rectX},${rectY + 5} L${rectX + this.rectLength},${rectY + 5}`
        
        let baseAttrs = { "d": descriptor, "stroke-width": 10, "stroke-dasharray": 320 }

        base.appendChild(this._createSVGElement("path", { ...baseAttrs, "stroke": this.color }));

        let dashOffset = this.isCompleted ? 180: 320;
        this.maskingEl = this._createSVGElement("path", 
            { ...baseAttrs, stroke: this.fgColor, "stroke-dashoffset": dashOffset }
        )

        base.appendChild(this.maskingEl);
        return base;
    }
}

class CurvedLine extends SVGIcon {
    constructor(rowSpace, colSpace, color, row, column, isCompleted, direction) {
        super(rowSpace, colSpace, color, row, column, isCompleted);
        this.direction = direction;
    }

    animate() {
        super.animate([
            { "strokeDashoffset": 320 },
            { "strokeDashoffset": 0 }
        ])
    }

    render() {
        let base = document.createDocumentFragment();
        let xOffset = this.direction === "left" ? 0: 40;
        // calculate starting x/y (M{startX} {startY})
        let startX = (103.25 + (this.colSpace * (this.column -1))) + xOffset;
        let startY = 103.25 + (this.rowSpace * (this.row - 1));

        // calculate control points (C{ctrlX} {ctrlY1} {ctrlX} {ctrlY2})
        let ctrlOffset = this.direction === "left" ? -131 : 131
        let ctrlX = startX + ctrlOffset;
        
        let ctrlY1 = startY;
        let ctrlY2 = startY + this.rowSpace;

        // Calculate end point ({endX} {endY})
        let endX = startX;
        let endY = startY + this.rowSpace;

        let path = `M${startX} ${startY}C${ctrlX} ${ctrlY1} ${ctrlX} ${ctrlY2} ${endX} ${endY}`;

        base.appendChild(this._createSVGElement("path", {d: path, stroke: this.color, "stroke-width": 10}));
        let dashOffset = this.isCompleted ? 0: 320;
        this.maskingEl = this._createSVGElement("path", 
            { d: path, fill: "transparent", "stroke-dasharray": 320, "stroke-dashoffset": dashOffset, "stroke": this.fgColor, "stroke-width": 10 }
        )
        base.appendChild(this.maskingEl);
        return base;
    }
}


// M263 341.5L296 324.613V358.387L263 341.5Z
// M{COLUMN_1} {row_1}L{COLUMN_2} {ROW_2}V{ROW_3}L{COLUMN_3} {ROW_4}Z
class AbstractIconFactory {
    // theme - string hex color, colSpace - Space between each flag, rowSpace - space between each row
    constructor(theme, colSpace, rowSpace) {
        this.theme = theme;
        this.colSpace = colSpace;
        this.rowSpace = rowSpace;
    }

    getBaseSVGFactory() {
        return ((colSpace, rowSpace) => 
            (totalRows, colsPerRow) => {
                let width = (colsPerRow * colSpace) + 70;
                let height = totalRows * (rowSpace + 5);
                let viewBox = `0 0 ${width} ${height}`;

                return createSVGElement("svg", {
                    viewBox: viewBox,
                    width: width,
                    height: height,
                    fill: "none"
                })
            }
        )(this.colSpace, this.rowSpace)
    }

    getFlagFactory() {
        return ((theme, colSpace, rowSpace) => 
            (row, column, isCompleted) => new Flag(rowSpace, colSpace, theme, row, column, isCompleted)
        )(this.theme, this.colSpace, this.rowSpace);
    }

    getStraightLineFactory() {
        return ((theme, colSpace, rowSpace) => 
            (row, column, direction, isCompleted) => new StraightLine(rowSpace, colSpace, theme, row, column, isCompleted, direction)
        )(this.theme, this.colSpace, this.rowSpace);
    }

    getCurvedLineFactory() {
        return ((theme, colSpace, rowSpace) => 
            (row, column, direction, isCompleted) => new CurvedLine(rowSpace, colSpace, theme, row, column, isCompleted, direction)
        )(this.theme, this.colSpace, this.rowSpace);
    }
}

class FlagProgressBar {
    constructor(totalFlags, iconFactory, totalCompletedFlags, numFlagsPerRow=3) {
        this.stages = []
        this.totalFlags = totalFlags;
        this.numFlagsPerRow = numFlagsPerRow;
        this.iconFactory = iconFactory;
        this.baseEl = this._generateBaseEl();
        this.totalCompletedFlags = totalCompletedFlags;

        if (this.totalCompletedFlags > this.totalFlags) {
            throw new Error("Total completed flags cannot be more than the total number of flags");
        }
    }

    _getNextStageElements() {
        return this.stages[this.totalCompletedFlags]
    }

    completeFlag() {
        if (this.totalCompletedFlags >= this.totalFlags) return;
        let elements = this._getNextStageElements();
        elements[0].animate().then(() => {
            if (elements.length > 1) elements[1].animate();
        })
        this.totalCompletedFlags++;
    }

    _generateBaseEl() {
        let svgFactory = iconFactory.getBaseSVGFactory();
        let totalRows = Math.ceil(this.totalFlags / this.numFlagsPerRow);
        let totalCols = this.numFlagsPerRow;
        return svgFactory(totalRows, totalCols);
    }

    generate() {
        let createFlag = this.iconFactory.getFlagFactory();
        let createStraightLine = this.iconFactory.getStraightLineFactory();
        let createCurvedLine = this.iconFactory.getCurvedLineFactory();

        let row = 1;
        let column = 1;
        let index = 0;

        while (index < this.totalFlags) {
            if (column > this.numFlagsPerRow) {
                row += 1
                column = 1
            } 
            let isRight = row % 2 == 1;
            let logicalCol = isRight ? column: (this.numFlagsPerRow - (column - 1));
            let currDirection = isRight ? "right": "left";
            let isCompleted = this.totalCompletedFlags > index;
            let line = column < this.numFlagsPerRow
                ? createStraightLine(row, logicalCol, currDirection, isCompleted)
                : createCurvedLine(row, logicalCol, currDirection, isCompleted)
            let flag = createFlag(row, logicalCol, isCompleted);
            this.baseEl.appendChild(flag.render());
            index++;
            if (index < this.totalFlags) {
                this.baseEl.appendChild(line.render());
                this.stages.push([flag, line]);
            } else {
                this.stages.push([flag]);
            }
            column += 1
        }
    }
}

class Pagination {
    constructor(element, startingPage) {
        this.element = element;
        this.element.style.display = "block";
        this.currentPage = startingPage;
        this.renderProgressCounter();
        this.renderHiddenElements();
    }
   
    nextPage() {
        if (this.currentPage < this.getTotalPages() - 1) {
            this.currentPage++;
            this.renderProgressCounter();
            this.renderHiddenElements();
        }
    }

    previousPage() {
        if (this.currentPage > 0) {
            this.currentPage--;
            this.renderProgressCounter();
            this.renderHiddenElements();
        }
    }
    
    renderHiddenElements() {
        let children = this.getChildElements();
        [...children].forEach((element, index) => {
            let displayValue = index === this.currentPage ? "flex": "none";
            element.style.display = displayValue;

        })
    }

    renderProgressCounter() {
        let text = `${this.currentPage+1} / ${this.getTotalPages()}`
        let progressCounterEl = this.element.parentElement.querySelector("p[data-role=\"flag-progress\"]");
        progressCounterEl.textContent = text;
    }

    getChildElements() {
        return this.element.children;
    }

    getTotalPages() {
        return this.getChildElements().length;
    }
}

async function getCurrentFlagsProgress() {
    let responseJson;
    try {
        const response = await fetch("/developer/challenges", {
            "method": "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        responseJson = await response.json();
    } catch {
        return {error: true, message: defaultErrorMessage};
    }

    return responseJson;
}

function copyIpAddress(ipAddr) {
    let cb = navigator.clipboard;
    const type = "text/plain";
    const blob = new Blob([ipAddr], { type });  
    const data = [new ClipboardItem({ [type]: blob })];
    cb.write(data).then(() => {
        console.log("Text copied");
    })
}

function createChallengeElement(challenge) {
    let template = document.getElementById("flag-submission-template");
    let clone = template.content.cloneNode(true).querySelector("div.developer-home__current-flags");
    clone.querySelector("h2 span:first-child").textContent = challenge.name;
    clone.querySelector("h2 span:last-child").textContent = challenge.ip;
    clone.querySelector("p.developer-home__flag-description").textContent = challenge.description;
    clone.querySelector("input[name=\"flag-id\"]").setAttribute("value", challenge.id)
    if (challenge.is_complete) {
        clone.querySelector("form").classList.add("hidden");
        clone.querySelector(".completed-notification-container").classList.remove("hidden");
    }
    return clone;
}

async function renderInitialPage() {
    const flags = await getCurrentFlagsProgress();
    if (flags.error || !flags.challenges) {
        alert("There was an error, please inform your instructor");
        return;
    }
    let totalCompletedFlags = 0;
    flags.challenges?.forEach((challenge) => {
        if (challenge.is_complete) totalCompletedFlags++;
        let clone = createChallengeElement(challenge);
        document.getElementById("paginated-flags").appendChild(clone.cloneNode(true));
    });

    let totalFlags = flags.total || flags.challenges.length || totalCompletedFlags;

    flagProgressBarTheme = {
        "bg": "#d9d9d9",
        "fg": "#9fef00"
    }
    iconFactory = new AbstractIconFactory(flagProgressBarTheme, 177, 161)
    window.flagProgressBar = new FlagProgressBar(totalFlags, iconFactory, totalCompletedFlags, 2);
    window.flagProgressBar.generate();
    document.getElementById("progress-bar-animated").appendChild(window.flagProgressBar.baseEl);


    document.querySelectorAll("input").forEach((el) => {
        registerInteractiveElement(el);
    });
}

async function submitFlagListener(e) {
    e.preventDefault();
    let f = new FormData(e.target);
    let flagValueAttempt = f.get("flag-value");
    if (!flagValueAttempt) return;
    let response = await submitChallengeFlag(f.get("flag-id"), flagValueAttempt);
    if (response.error) {
        console.log(response.message); 
    } else {
        alert("Challenge completed");
        e.target.parentElement.querySelector(".completed-notification-container").classList.remove("hidden");
        e.target.classList.add("hidden");
        window.flagProgressBar.completeFlag()
    }
}

async function setupPage() {
    await renderInitialPage()
    p = new Pagination(document.getElementById("paginated-flags", 0), 0);
    document.getElementById("caret-left").addEventListener("click", () => p.previousPage())
    document.getElementById("caret-right").addEventListener("click", () =>  p.nextPage());

}

(function() {
    document.querySelector("form[name=submitFlagForm]")?.addEventListener("submit", (e) => {
        e.preventDefault();
        let form = new FormData(e.target);
        const flagValue = form.get("flagValue");
        const challengeId = e.target.closest("tr").dataset.chalId;
        submitChallengeFlag(challengeId, flagValue)
    });

    document.addEventListener("click", (event) => {
        if (event.target.matches("span.ip-addr")) {
            copyIpAddress(event.target.textContent);
        } else if (event.target.matches(".developer-home__flag-submission-portal")) {

        }
    });

    document.addEventListener("submit", async (event) => {
        if (event.target.matches(".developer-home__flag-submission-portal")) {
            await submitFlagListener(event);
        }
    })

    setupPage();
})()

