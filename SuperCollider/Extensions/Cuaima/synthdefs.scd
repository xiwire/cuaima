~workingDirectory = "SuperCollider/Extensions/Cuaima";
~synthdefsToAdd = ["biast/biast.scd", "utils/utils.scd", "fx/fx.scd", "basic/oscs.scd"];

s.waitForBoot {
    var pathsToAdd;

    for(0, ~synthdefsToAdd.size - 1, {
        arg i;
        var synthDefName, pathToLoad;

        synthDefName = ~synthdefsToAdd[i];
        pathToLoad = ~workingDirectory ++ "/" ++ synthDefName;

        pathToLoad.loadPaths;
    });
}
