~workingDirectory = File.getcwd ++ "/SuperCollider/Extensions/CuaimaSC";
~synthdefsToAdd = ["biast"];

s.waitForBoot {
    var pathsToAdd;

    pathsToAdd = Array.fill(~synthdefsToAdd.size, {
        arg i;
        ~workingDirectory ++ "/" ++ ~synthdefsToAdd[i];
    });
    pathsToAdd.loadPaths;
}
