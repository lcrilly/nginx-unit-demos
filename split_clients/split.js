function clients(proportion, param) {
    var c = require('crypto');
    var i = c.createHash('md5').update(param).digest().readInt16BE() + 32768;
    return (proportion * 65536) > i ? 'green' : 'blue';
}

export default { clients }
