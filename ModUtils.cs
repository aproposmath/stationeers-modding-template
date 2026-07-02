using System;
using System.IO;
using System.Runtime.CompilerServices;

internal static class ModUtils
{
    public static bool IsLoadedByScriptEngine(Type type)
    {
        L.Debug($"Assembly path: {type.Assembly.Location}");
        return string.IsNullOrEmpty(type.Assembly.Location);
    }
}

#if DEBUG
public readonly struct ScopedMemoryTracker(string file = null, int line = -1) : IDisposable
{
    private readonly long StartMemory = GC.GetTotalMemory(false);

    private readonly string _file = file;
    private readonly int _line = line;

    public static ScopedMemoryTracker Track(
        [CallerFilePath] string file = "",
        [CallerLineNumber] int line = 0)
    {
        return new ScopedMemoryTracker(file, line);
    }
    public void Dispose()
    {
        var endMemory = GC.GetTotalMemory(false);
        var delta = endMemory - StartMemory;
        if (delta != 0)
        {
            var Name = $"{Path.GetFileName(_file)}:{_line}";
            L.Debug($"\t{Name}\t{delta} bytes ({delta / 1024.0:F2} KB)");
        }
    }
}
#else
public readonly struct ScopedMemoryTracker : IDisposable
{
    public static ScopedMemoryTracker Track() => new ScopedMemoryTracker();
    public void Dispose() { }
}
#endif
