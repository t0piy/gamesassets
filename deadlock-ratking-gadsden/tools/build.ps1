[CmdletBinding()]
param(
    [ValidateSet('modern-clean','modern-worn','join-or-die-clean','join-or-die-worn')]
    [string]$Variant = 'modern-worn',
    [Parameter(Mandatory=$true)][string]$DeadlockDir,
    [Parameter(Mandatory=$true)][string]$Source2ViewerCli,
    [Parameter(Mandatory=$true)][string]$CsdkDir,
    [string]$TexturePath = '',
    [switch]$NoPack
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Work = Join-Path $Root ".build\$Variant"
$Dist = Join-Path $Root 'dist'
New-Item -ItemType Directory -Force -Path $Work,$Dist | Out-Null

function Find-Vpk {
    $candidates = @(
      (Join-Path $DeadlockDir 'game\citadel\pak01_dir.vpk'),
      (Join-Path $DeadlockDir 'game\citadel\pak01_000.vpk')
    )
    foreach ($p in $candidates) { if (Test-Path $p) { return $p } }
    throw "Could not find Deadlock pak01 VPK below $DeadlockDir"
}

$Vpk = Find-Vpk
$ListFile = Join-Path $Work 'ratking-vpk-list.txt'
& $Source2ViewerCli -i $Vpk --vpk_list --vpk_filepath 'models/heroes_wip/ratking/' | Out-File -Encoding utf8 $ListFile

if (-not $TexturePath) {
    $all = Get-Content $ListFile | Where-Object { $_ -match 'materials/.+\.vtex_c' }
    $likely = $all | Where-Object { $_ -match '(banner|flag|ultimate|ult)' }
    if ($likely.Count -eq 1) { $TexturePath = $likely[0].Trim() }
    elseif ($all.Count -eq 1) { $TexturePath = $all[0].Trim() }
    else {
        Write-Host "Could not safely choose a single banner texture. Candidates:" -ForegroundColor Yellow
        $all | ForEach-Object { Write-Host "  $_" }
        throw "Re-run with -TexturePath '<exact path from the list above>'. This guard avoids overwriting the wrong Rat King material."
    }
}

if ($TexturePath -notmatch '^models/heroes_wip/ratking/' -or $TexturePath -notmatch '\.vtex_c$') {
    throw "TexturePath must be a Rat King .vtex_c path. Got: $TexturePath"
}

$BasePng = Join-Path $Work 'base-banner.png'
& $Source2ViewerCli -i $Vpk --vpk_filepath $TexturePath -o $BasePng -d
if (-not (Test-Path $BasePng)) { throw "Source2Viewer did not export $BasePng" }

$ArtPng = Join-Path $Root "assets\source\$Variant-4096.png"
if (-not (Test-Path $ArtPng)) {
    Write-Host "Preparing verified raster source..." -ForegroundColor Cyan
    python (Join-Path $PSScriptRoot 'fetch_source.py')
    if ($LASTEXITCODE -ne 0) { throw "Raster source download/check failed." }
    python (Join-Path $PSScriptRoot 'prepare_rasters.py')
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $ArtPng)) {
        throw "Raster preparation failed. Install Pillow with: python -m pip install pillow"
    }
}

$Composed = Join-Path $Work 'banner.png'
python (Join-Path $PSScriptRoot 'compose_texture.py') --base $BasePng --art $ArtPng --output $Composed
if ($LASTEXITCODE -ne 0) { throw 'Texture composition failed.' }

$RelativeUncompiled = $TexturePath -replace '\.vtex_c$','.vtex'
$RelativePng = $TexturePath -replace '\.vtex_c$','.png'
$AddonContent = Join-Path $Work 'content\citadel_addons\ratking_gadsden'
$VtexPath = Join-Path $AddonContent $RelativeUncompiled
$PngPath = Join-Path $AddonContent $RelativePng
New-Item -ItemType Directory -Force -Path (Split-Path $VtexPath),(Split-Path $PngPath) | Out-Null
Copy-Item $Composed $PngPath -Force

$relPngForVtex = ($RelativePng -replace '\\','/')
$vtex = @"
<!-- dmx encoding keyvalues2_noids 1 format vtex 1 -->
"CDmeVtex"
{
  "m_inputTextureArray" "element_array"
  [
    "CDmeInputTexture"
    {
      "m_name" "string" "InputTexture0"
      "m_fileName" "string" "$relPngForVtex"
      "m_colorSpace" "string" "srgb"
      "m_typeString" "string" "2D"
      "m_imageProcessorArray" "element_array" [ ]
    }
  ]
  "m_outputTypeString" "string" "2D"
  "m_outputFormat" "string" "BC7"
  "m_outputClearColor" "vector4" "0 0 0 0"
  "m_nOutputMinDimension" "int" "0"
  "m_nOutputMaxDimension" "int" "0"
  "m_textureOutputChannelArray" "element_array"
  [
    "CDmeTextureOutputChannel"
    {
      "m_inputTextureArray" "string_array" [ "InputTexture0" ]
      "m_srcChannels" "string" "rgba"
      "m_dstChannels" "string" "rgba"
      "m_mipAlgorithm" "CDmeImageProcessor"
      {
        "m_algorithm" "string" "Box"
        "m_stringArg" "string" ""
        "m_vFloat4Arg" "vector4" "0 0 0 0"
      }
      "m_outputColorSpace" "string" "srgb"
    }
  ]
}
"@
Set-Content -Encoding utf8 $VtexPath $vtex

$ResourceCompiler = Get-ChildItem -Path $CsdkDir -Filter resourcecompiler.exe -Recurse -File | Select-Object -First 1
if (-not $ResourceCompiler) { throw "resourcecompiler.exe not found below $CsdkDir" }
$GameRoot = Join-Path $Work 'game\citadel_addons\ratking_gadsden'
New-Item -ItemType Directory -Force -Path $GameRoot | Out-Null

& $ResourceCompiler.FullName -game $GameRoot $VtexPath
if ($LASTEXITCODE -ne 0) { throw "resourcecompiler failed ($LASTEXITCODE)" }

$CompiledName = $TexturePath
$compiledCandidates = Get-ChildItem -Path $Work -Recurse -Filter ([IO.Path]::GetFileName($CompiledName)) -File
if (-not $compiledCandidates) {
    throw "Compilation completed but the expected $(Split-Path $CompiledName -Leaf) was not found. See CSDK output above."
}
$Compiled = $compiledCandidates[0]
$LooseRoot = Join-Path $Work 'loose'
$LooseDest = Join-Path $LooseRoot $TexturePath
New-Item -ItemType Directory -Force -Path (Split-Path $LooseDest) | Out-Null
Copy-Item $Compiled.FullName $LooseDest -Force

$LooseZip = Join-Path $Dist "ratking-banner-$Variant-loose.zip"
if (Test-Path $LooseZip) { Remove-Item $LooseZip -Force }
Compress-Archive -Path (Join-Path $LooseRoot '*') -DestinationPath $LooseZip
Write-Host "Built loose replacement: $LooseZip" -ForegroundColor Green

if (-not $NoPack) {
    $VpkExe = Get-ChildItem -Path $CsdkDir -Filter vpk.exe -Recurse -File | Select-Object -First 1
    if ($VpkExe) {
        $PackRoot = Join-Path $Work 'pack'
        New-Item -ItemType Directory -Force -Path $PackRoot | Out-Null
        Copy-Item -Recurse -Force (Join-Path $LooseRoot '*') $PackRoot
        & $VpkExe.FullName $PackRoot
        $packed = "$PackRoot.vpk"
        if (Test-Path $packed) {
            $FinalVpk = Join-Path $Dist "ratking-banner-$Variant.vpk"
            Move-Item -Force $packed $FinalVpk
            Write-Host "Built VPK: $FinalVpk" -ForegroundColor Green
        } else {
            Write-Warning 'vpk.exe ran, but no VPK was found at the expected output path. Loose ZIP is still valid for inspection.'
        }
    } else {
        Write-Warning 'vpk.exe was not found in the CSDK. Skipping VPK; loose ZIP was created.'
    }
}

Set-Content -Encoding utf8 (Join-Path $Dist "ratking-banner-$Variant-target.txt") $TexturePath
