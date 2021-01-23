~workingDirectory = File.getcwd ++ "/SuperCollider/Extensions/CuaimaSC";
~synthdefsToAdd = ["biast"];

s.waitForBoot {
    var pathsToAdd;

    for(0, ~synthdefsToAdd.size - 1, {
        arg i;
        var synthDefName, pathToLoad;

        synthDefName = ~synthdefsToAdd[i];
        pathToLoad = ~workingDirectory ++ "/" ++ synthDefName ++ "/" ++ synthDefName ++ ".scd";

        pathToLoad.loadPaths;
    });
}
