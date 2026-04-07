using System.Diagnostics;

public class QgisAtlasService
{
    public async Task<string> GenerateAtlas(string geojsonPath)
    {
        var outputPdf = Path.Combine("output", $"atlas_{Guid.NewGuid()}.pdf");

        Directory.CreateDirectory("output");

        var psi = new ProcessStartInfo
        {
            FileName = @"C:\OSGeo4W\bin\python-qgis.bat",
            Arguments = $"GIS/export_atlas.py \"{geojsonPath}\" \"{outputPdf}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false
        };

        var process = Process.Start(psi);

        await process.WaitForExitAsync();

        return outputPdf;
    }
}