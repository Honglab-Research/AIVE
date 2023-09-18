class CommonMath {
    constructor() {
    }
    // sort array ascending
    //오름차순 정렬
    asc(arr) { return arr.sort((a, b) => a - b); }
    //총합
    sum(arr) { return arr.reduce((a, b) => a + b, 0); }
    //평균
    mean(arr) { return sum(arr) / arr.length; }
    // sample standard deviation
    std(arr) {
        const mu = this.mean(arr);
        const diffArr = arr.map(a => (a - mu) ** 2);
        return Math.sqrt(this.sum(diffArr) / (arr.length - 1));
    }
    //사분위수 계산
    quantile(arr, q) {
        const sorted = this.asc(arr);
        const pos = (sorted.length - 1) * q;
        const base = Math.floor(pos);
        const rest = pos - base;
        if (sorted[base + 1] !== undefined) {
            return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
        } else {
            return sorted[base];
        }
    }
    q1(arr) { return this.quantile(arr, .25); }
    q2(arr) { return this.quantile(arr, .50); }
    q3(arr) { return this.quantile(arr, .75); }
    median(arr) { return this.q2(arr); }
}