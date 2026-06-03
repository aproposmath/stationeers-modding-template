using System;
using System.IO;

internal static class ModUtils
{
    public static bool IsLoadedByScriptEngine(Type type)
    {
        string assemblyPath = Path.GetFullPath(type.Assembly.Location);
        string scriptsPath = Path.GetFullPath(Path.Combine(BepInEx.Paths.BepInExRootPath, "scripts"));
        L.Debug($"Assembly path: {assemblyPath}");
        L.Debug($"Scripts path: {scriptsPath}");
        var result = assemblyPath.StartsWith(scriptsPath, StringComparison.OrdinalIgnoreCase);
        L.Debug($"Is loaded by script engine: {result}");
        return result;
    }
}
