const fs=require('node:fs'),net=require('node:net');
const result={};
for(const [name,path] of Object.entries({private_credentials:'/Users/kishore/.contentos/secrets',private_home:'/Users/kishore/git/creative-engineering-hub/README.md'})){
 try {const fd=fs.openSync(path,'r');fs.closeSync(fd);result[name]='UNEXPECTED_READ';}
 catch(e){result[name]=e.code;}
}
try {fs.writeFileSync('/tmp/ceh-outside-benchmark-canary','should be denied');result.outside_write='UNEXPECTED_WRITE';}
catch(e){result.outside_write=e.code;}
const server=net.createServer(s=>s.end('local'));
server.listen(0,'127.0.0.1',()=>{
 const client=net.connect(server.address().port,'127.0.0.1');
 client.once('data',()=>{result.loopback='allowed';client.end();server.close();});
 client.once('close',()=>{
  const external=net.connect(443,'1.1.1.1');
  external.setTimeout(1500,()=>{result.external_network='TIMEOUT';external.destroy();});
  external.on('error',e=>{result.external_network=e.code;});
  external.once('close',()=>console.log(JSON.stringify(result,null,2)));
 });
});
