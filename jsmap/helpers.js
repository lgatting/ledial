helpers = {
    /**
     * Removes leading zeroes in a int-like string.
     * @param {string} s String from which the zeroes will be removed.
     */
    removeLeadingZeroes: function (s) {
        return s.replace(/^0+/, "");
    },

    /**
     * Whether given point is in given polygon.
     * @param {*} nvert Number of vertices in the polygon.
     * @param {*} vertx Array of X coordinates of the vertices.
     * @param {*} verty Array of Y coordinates of the vertices.
     * @param {*} testx X coordinate of the point to test.
     * @param {*} testy Y coordinate of the point to test.
     */
    inPolygon: function (nvert, vertx, verty, testx, testy) {
      var i, j, c = 0;
      for (i = 0, j = nvert-1; i < nvert; j = i++) {
        if ( ((verty[i]>testy) != (verty[j]>testy)) &&
         (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
           c = !c;
      }
      return c;
    },

    /**
     * Calculates centroid of given polygon and returns the result as 2-element array.
     * @param {array} pts Points of the polygon.
     */
    centroid: function (pts) {
        var first = pts[0], last = pts[pts.length-1];
        if (first.x != last.x || first.y != last.y) pts.push(first);
        var twicearea=0,
        x=0, y=0,
        nPts = pts.length,
        p1, p2, f;
        for ( var i=0, j=nPts-1 ; i<nPts ; j=i++ ) {
           p1 = pts[i]; p2 = pts[j];
           f = p1[0]*p2[1] - p2[0]*p1[1];
           twicearea += f;          
           x += ( p1[0] + p2[0] ) * f;
           y += ( p1[1] + p2[1] ) * f;
        }
        f = twicearea * 3;
        return [x/f, y/f];
    },

    /**
     * Returns a random rgba color string, e.g. rgba(124,155,42,0.4).
     * @param {float} alpha Alpha value of the color.
     */
    randomRGBAColor: function (alpha) {
        var s = "rgba(";
        
        for (var i = 0; i < 3; i++)
            s += helpers.randomInt(255) + ",";

        s += alpha + ")";

        return s;
    },

    /**
     * Returns a random integer that is not greater than the maximum value provided.
     * @param {int} max Maximum value.
     */
    randomInt: function (max) {
        return Math.round(Math.random()*max);
    }
}