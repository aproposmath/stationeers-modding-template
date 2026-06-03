using System;
using System.IO;

internal static class ModUtils
{
    public static bool IsLoadedByScriptEngine(Type type)
    {
        L.Debug($"Assembly path: {type.Assembly.Location}");
        return string.IsNullOrEmpty(type.Assembly.Location);
    }
}
