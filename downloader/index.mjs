import { Octokit } from 'octokit'
import { spawnSync } from 'child_process'

const gh = new Octokit()

async function main() {
  const rel = await gh.rest.repos.getReleaseByTag({
    owner: 'nguyenvukhang',
    repo: 'backblaze',
    tag: 'v0.1',
  })
  // console.log(rel.data.assets)
  for (let i = 0; i < rel.data.assets.length; i++) {
    const asset = rel.data.assets[i]

    // spawnSync()
    let cmd = `curl -o ${asset.name} -L`
    cmd += ' -H "Accept: application/octet-stream"'
    cmd += ` https://api.github.com/repos/nguyenvukhang/backblaze/releases/assets/${asset.id}`
    console.log(`Downloading [${asset.name}] ...`)
    console.log(cmd)
    spawnSync(cmd, { stdio: 'inherit', shell: true })
  }
}

main().finally(() => process.exit())