using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/atlas")]
public class AtlasController : ControllerBase
{
    private readonly QgisAtlasService _atlasService;

    public AtlasController(QgisAtlasService atlasService)
    {
        _atlasService = atlasService;
    }

    [HttpPost("export")]
    public async Task<IActionResult> ExportAtlas(IFormFile geojson)
    {
        if (geojson == null || geojson.Length == 0)
            return BadRequest("GeoJSON file missing");

        var filePath = Path.Combine("uploads", geojson.FileName);

        Directory.CreateDirectory("uploads");

        using (var stream = new FileStream(filePath, FileMode.Create))
        {
            await geojson.CopyToAsync(stream);
        }

        var pdfPath = await _atlasService.GenerateAtlas(filePath);

        return PhysicalFile(pdfPath, "application/pdf", "atlas.pdf");
    }
}